from DrissionPage import Chromium, SessionPage, ChromiumOptions
import json
import time
import csv
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# ========== 日志配置 ==========
logger = logging.getLogger(__name__)

# ========== 常量 ==========
URL_MAPPING = {
    "A股": "https://np-tjxg-g.eastmoney.com/api/smart-tag/stock/v3/pw/search-code" ,
    "港股": "https://np-tjxg-b.eastmoney.com/api/smart-tag/hk/v3/pw/search-code" ,
    "板块": "https://np-tjxg-b.eastmoney.com/api/smart-tag/bkc/v3/pw/search-code" ,
    "ETF": "https://np-tjxg-b.eastmoney.com/api/smart-tag/etf/v3/pw/search-code" ,
    "可转债": "https://np-tjxg-b.eastmoney.com/api/smart-tag/cb/v3/pw/search-code" ,
}
REFERER = 'https://xuangu.eastmoney.com/'
OUTPUT_DIR = Path("workspace")

POST_DATA_TEMPLATE = {
    'gids': [],
    'matchWord': '',
    'timestamp': '',
    'shareToGuba': False,
    'needAmbiguousSuggest': True,
    'requestId': '',
    'product': '',
    'needCorrect': True,
    'removedConditionIdList': [],
    'client': 'WEB',
    'ownSelectAll': False,
    'dxInfo': [],
    'biz': 'web_ai_select_stocks',
    'customData': ''
}

HEADERS = {
    'Content-Type': 'application/json',
    'Referer': REFERER,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# ========== Fingerprint 相关 ==========

def get_fingerprint():
    """访问东方财富选股页面，获取cookie中的qgqp_b_id值"""
    co = ChromiumOptions()
    co.headless(True)

    browser = None
    try:
        browser = Chromium(co)
        tab = browser.latest_tab
        tab.get('https://xuangu.eastmoney.com/', timeout=10)
        tab.wait.doc_loaded()

        # 轮询获取 cookie
        max_wait_time = 5
        start_time = time.time()
        fingerprint = None

        while time.time() - start_time < max_wait_time:
            fingerprint = next(
                (c.get('value') for c in tab.cookies() if c.get('name') == 'qgqp_b_id'),
                None
            )
            if fingerprint:
                break
            time.sleep(0.2)

        if not fingerprint:
            logger.warning("超时未找到 qgqp_b_id cookie")
            return None

        save_fingerprint(fingerprint)
        logger.info("获取到 fingerprint: %s", fingerprint)
        return fingerprint
    except Exception as e:
        logger.exception("获取 fingerprint 失败: %s", e)
        return None
    finally:
        if browser:
            browser.quit()


def save_fingerprint(fp: str):
    """保存到缓存"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / 'fingerprint_cache.json', 'w', encoding='utf-8') as f:
        json.dump({'fingerprint': fp}, f, indent=2)

def get_cached_fingerprint(cache_file: str = 'fingerprint_cache.json') -> Optional[str]:
    """读取缓存的 fingerprint"""
    try:
        with open(OUTPUT_DIR / cache_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('fingerprint')
    except (json.JSONDecodeError, OSError):
        return None


# ========== CSV 导出 ==========

def _save_to_csv(
    all_data: List[Dict[str, Any]],
    field_mapping: Dict[str, str],
    *,
    filename_prefix: str = "search_stocks"
) -> Optional[Path]:
    """将结果写入 CSV"""
    if not all_data or not field_mapping:
        logger.info("无数据或无字段映射，跳过生成 CSV。")
        return None

    # 表头顺序：field_mapping 的 key + 未映射的字段
    header = list(field_mapping.keys())
    unmapped_keys = sorted(set(all_data[0].keys()) - set(header))
    if unmapped_keys:
        header.extend(unmapped_keys)

    display_header = [field_mapping.get(k, k) for k in header]

    now_str = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{now_str}.csv"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / filename

    try:
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(display_header)
            for row in all_data:
                writer.writerow([str(row.get(k, "")) for k in header])
        logger.info("CSV 已保存：%s，共 %d 行（不含表头）。", csv_path, len(all_data))
        return csv_path
    except OSError as e:
        logger.error("写入 CSV 失败：%s", e)
        return None


# ========== 搜索主逻辑 ==========

def search_stocks(
    fingerprint: str,
    keyword: str,
    selectType: str="A股",
    page_size: int = 50,
    *,
    filename_prefix: str = "search_stocks",
    timeout: Optional[int] = 15,
    retry: Optional[int] = 2,
    interval: Optional[float] = 0.5,
) -> Dict[str, Any]:
    """根据条件搜索股票，分页拉取并导出为 CSV"""
    page = SessionPage()

    result: Dict[str, Any] = {
        "csv_path": None,
        "row_count": 0,
        "query": keyword,
        "total": None,
        "error": None,
    }

    all_data: List[Dict[str, Any]] = []
    field_mapping: Dict[str, str] = {}
    page_no = 1
    total = 0          
    max_page_no = 200
    
    BASE_URL = URL_MAPPING.get(selectType,URL_MAPPING["A股"])
    logger.info("当前搜索市场类型: %s, 接口: %s", selectType, BASE_URL)
    while page_no <= max_page_no:
        post_data = {
            **POST_DATA_TEMPLATE,
            'keyWord': keyword,
            'pageSize': page_size,
            'pageNo': page_no,
            'fingerprint': fingerprint,
        }

        try:
            success = page.post(BASE_URL, json=post_data, headers=HEADERS)
        except Exception as e:
            logger.exception("请求异常（第 %s 页）：%s", page_no, e)
            result["error"] = f"请求异常：{e}"
            break

        if not success:
            logger.warning("第 %s 页请求失败。", page_no)
            result["error"] = f"第 {page_no} 页请求失败"
            break

        # 解析 JSON
        raw = page.json if page.json else None
        if not raw:
            logger.error("第 %s 页：响应为空或非 JSON。", page_no)
            result["error"] = f"第 {page_no} 页：响应为空或非 JSON"
            break

        if raw.get('code') == '502':
            logger.error("收到 502 错误码（第 %s 页）。", page_no)
            result["error"] = "502 Error"
            break

        try:
            payload = raw['data']['result']
            data_list = payload['dataList']
            total = payload['total']
            columns = payload.get('columns', [])
        except (KeyError, TypeError) as e:
            logger.error("第 %s 页：接口字段结构异常 - %s", page_no, e)
            result["error"] = f"接口字段结构异常（第 {page_no} 页）"
            break

        # 只在第一页生成字段映射
        if page_no == 1 and columns:
            field_mapping = {col['key']: col.get('title', col['key']) for col in columns if 'key' in col}
            logger.info("字段映射数量：%d", len(field_mapping))

        if not data_list:
            logger.info("第 %s 页：无数据，结束分页。", page_no)
            break

        all_data.extend(data_list)
        logger.info("第 %s 页获取 %d 条，累计 %d/%d。", page_no, len(data_list), len(all_data), total)

        if len(all_data) >= total:
            break

        page_no += 1
        time.sleep(0.4)

    # 封装返回值
    result["total"] = total
    result["row_count"] = len(all_data)

    if all_data and field_mapping:
        csv_path = _save_to_csv(
            all_data, field_mapping,
            filename_prefix=filename_prefix,
        )
        result["csv_path"] = str(csv_path) if csv_path else None

    return result


# ========== 入口 ==========

def main():
    import argparse
    import sys
    """命令行入口：从参数或 stdin 读取查询文本，执行并打印结果路径。"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    parser = argparse.ArgumentParser(description='通过自然语言查询进行选股、选板块、选基金')

    # 添加位置参数
    parser.add_argument('--query', type=str, help='自然语言查询，如「股价大于1000元的股票」')

    # 添加可选参数
    parser.add_argument('--select-type', dest='selectType',
                        choices=['A股', '港股', 'ETF', '可转债', '板块'],
                        help='选股指定标的类型')
    args = parser.parse_args()

    logger.info(f"选股问句: {args.query}，选股类型: {args.selectType}")

    if not args.query:
        logger.info("用法: python em_stock_selector.py --query \"查询文本\" --select-type \"查询领域\"")
        logger.info("示例: 股价大于1000元的股票 | 港股")
        sys.exit(1)
    
    fingerprint = get_cached_fingerprint() or get_fingerprint()
    if not fingerprint:
        logger.error("无法获取 fingerprint，程序退出。")
        return

    res = search_stocks(fingerprint, args.query, args.selectType)
    if res.get("error") == "502 Error":
        new_fingerprint = get_fingerprint()
        if new_fingerprint:
            res = search_stocks(new_fingerprint, args.query, args.selectType)
        else:
            logger.error("刷新 fingerprint 失败，无法进行重试。")

    logger.info("搜索结果: %s", res)

if __name__ == '__main__':
    main()
