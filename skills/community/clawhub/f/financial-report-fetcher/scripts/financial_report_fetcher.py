#!/usr/bin/env python3
"""
金融报告抓取脚本 - 巨潮资讯首选
用法:
  python3 financial_report_fetcher.py --stock 600519 --year 2024
  python3 financial_report_fetcher.py --stocks "600519,000858" --years "2023,2024"
  python3 financial_report_fetcher.py --stock 600519 --year 2024 --dry-run
  python3 financial_report_fetcher.py --stock 600519 --year 2024 --parse-pdf
  python3 financial_report_fetcher.py --research --stock 600519 --months 3
"""

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta
from typing import Optional

import requests

# ============================================================
# 配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
META_FILE = os.path.join(DOWNLOAD_DIR, "metadata.json")

# 巨潮资讯 API
CNINFO_SEARCH_URL = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_PDF_BASE = "http://static.cninfo.com.cn/"

# User-Agent 池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
]

# 报告类型 → 巨潮 category 映射
CATEGORY_MAP = {
    "annual": "category_ndbg_szsh",       # 年报
    "semi-annual": "category_bndbg_szsh",   # 半年报
    "quarterly": "category_jdbg_szsh",      # 季报
    "prospectus": "category_first_szsh",     # 招股书
}

CATEGORY_NAMES = {
    "annual": "年度报告",
    "semi-annual": "半年度报告",
    "quarterly": "季度报告",
    "prospectus": "招股意向书",
}


def random_delay(low=1.0, high=3.0):
    """随机延迟，模拟人类行为"""
    delay = random.uniform(low, high)
    time.sleep(delay)


def get_headers(referer: str = None) -> dict:
    """生成请求头"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    if referer:
        headers["Referer"] = referer
    return headers


# ============================================================
# 巨潮资讯核心逻辑
# ============================================================
def search_cninfo(
    stock_code: str,
    year: int,
    report_type: str = "annual",
    page_size: int = 30,
) -> list:
    """
    搜索巨潮资讯公告
    返回: 公告列表
    """
    category = CATEGORY_MAP.get(report_type, CATEGORY_MAP["annual"])
    search_key = CATEGORY_NAMES.get(report_type, "报告")

    # 判断交易所（简单规则：6开头=沪，0/3开头=深）
    if stock_code.startswith("6"):
        column = "sse"
        org_id = f"gssh{stock_code}"  # 上交所 orgId 格式
    else:
        column = "szse"
        org_id = f"gssz{stock_code}"  # 深交所 orgId 格式

    # 关键：巨潮需要 seDate 覆盖发布窗口期（年报可能在次年4月发布）
    # 搜索时使用 searchkey 精准匹配，不依赖 category（category 可能筛选过度）
    payload = {
        "stock": f"{stock_code},{org_id}",
        "tabName": "fulltext",
        "pageSize": str(page_size),
        "pageNum": "1",
        "column": column,
        "seDate": f"{year}-01-01~{year+1}-06-30",  # 覆盖次年发布窗口
        "searchkey": f"{year}年年度报告",
    }

    headers = get_headers("http://www.cninfo.com.cn/new/disclosure")

    try:
        resp = requests.post(CNINFO_SEARCH_URL, data=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        anns = data.get("announcements") or []
        return anns
    except requests.RequestException as e:
        print(f"[ERROR] 巨潮请求失败: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] 巨潮响应解析失败: {e}", file=sys.stderr)
        return []


def download_pdf(
    announcement: dict,
    output_dir: str,
    dry_run: bool = False,
) -> Optional[str]:
    """
    下载 PDF 文件
    返回: 文件路径
    """
    adjunct_url = announcement.get("adjunctUrl", "")
    if not adjunct_url:
        return None

    pdf_url = f"{CNINFO_PDF_BASE}{adjunct_url}"
    title = announcement.get("announcementTitle", "unknown")
    sec_code = announcement.get("secCode", "unknown")
    sec_name = announcement.get("secName", "unknown")

    # 清理文件名
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    safe_name = re.sub(r'[\\/*?:"<>|]', "", sec_name)
    filename = f"{sec_code}_{safe_name}_{safe_title}.pdf"

    # 按公司代码创建目录
    company_dir = os.path.join(output_dir, sec_code)
    os.makedirs(company_dir, exist_ok=True)
    filepath = os.path.join(company_dir, filename)

    if dry_run:
        print(f"[DRY RUN] 将下载: {filename}")
        print(f"  URL: {pdf_url}")
        return filepath

    try:
        headers = get_headers("http://www.cninfo.com.cn/new/disclosure")
        resp = requests.get(pdf_url, headers=headers, timeout=30, stream=True)
        resp.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = os.path.getsize(filepath) / (1024 * 1024)
        print(f"[OK] 已下载: {filename} ({file_size:.1f} MB)")
        return filepath

    except requests.RequestException as e:
        print(f"[ERROR] PDF 下载失败: {filename}: {e}", file=sys.stderr)
        return None


# ============================================================
# PDF 解析
# ============================================================
def parse_pdf_financial_data(pdf_path: str) -> dict:
    """从年报PDF中提取关键财务数据"""
    try:
        import fitz
    except ImportError:
        print("[WARN] PyMuPDF 未安装，跳过 PDF 解析", file=sys.stderr)
        return {}

    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[ERROR] PDF 解析失败: {e}", file=sys.stderr)
        return {}

    # 常见财务指标模式
    patterns = {
        "营收": r"营业收入[：:]\s*([\d,\.]+)\s*(?:亿)?元",
        "净利润": r"归属于.*?净利润[：:]\s*([\d,\.]+)\s*(?:亿)?元",
        "总资产": r"资产总计[：:]\s*([\d,\.]+)\s*(?:亿)?元",
        "每股收益": r"基本每股收益[：:]\s*([\d,\.]+)\s*元",
        "ROE": r"加权平均净资产收益率[：:]\s*([\d,\.]+)\s*%",
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)

    print(f"[INFO] 提取到 {len(data)} 个财务指标: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return data


# ============================================================
# 元数据管理
# ============================================================
def save_metadata(downloads: list):
    """保存下载元数据"""
    meta = {}
    if os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)

    if "downloads" not in meta:
        meta["downloads"] = []

    for d in downloads:
        d["download_time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        meta["downloads"].append(d)

    os.makedirs(os.path.dirname(META_FILE), exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 元数据已保存到 {META_FILE}")


# ============================================================
# 主流程
# ============================================================
def run_fetch(
    stock_code: str,
    years: list,
    report_type: str = "annual",
    dry_run: bool = False,
    parse_pdf: bool = False,
):
    """执行抓取流程"""
    print(f"=" * 60)
    print(f"📊 金融报告抓取")
    print(f"   股票代码: {stock_code}")
    print(f"   年份: {years}")
    print(f"   报告类型: {report_type} ({CATEGORY_NAMES.get(report_type, '')})")
    print(f"   数据源: 巨潮资讯 (cninfo.com.cn)")
    print(f"   模式: {'DRY RUN' if dry_run else '实际下载'}")
    print(f"=" * 60)

    all_downloads = []

    for year in years:
        print(f"\n--- 搜索 {year} 年 {CATEGORY_NAMES.get(report_type, '报告')} ---")
        announcements = search_cninfo(stock_code, year, report_type)

        if not announcements:
            print(f"[WARN] {year} 年未找到相关报告")
            continue

        print(f"[INFO] 找到 {len(announcements)} 条公告")

        # 过滤：只取年报/报告类（排除董事会决议等）
        keywords = CATEGORY_NAMES.get(report_type, "报告")
        filtered = [
            a for a in announcements
            if keywords in a.get("announcementTitle", "")
        ]

        if not filtered:
            filtered = announcements[:3]  # 取前3条
            print(f"[INFO] 无精确匹配，取前 {len(filtered)} 条")

        for ann in filtered:
            random_delay()
            filepath = download_pdf(ann, DOWNLOAD_DIR, dry_run=dry_run)

            if filepath:
                download_record = {
                    "stock_code": ann.get("secCode", stock_code),
                    "stock_name": ann.get("secName", ""),
                    "report_type": report_type,
                    "year": str(year),
                    "source": "cninfo",
                    "title": ann.get("announcementTitle", ""),
                    "announcement_id": ann.get("announcementId", ""),
                    "file_path": filepath,
                }
                all_downloads.append(download_record)

                if parse_pdf and not dry_run and os.path.exists(filepath):
                    print(f"\n--- 解析 PDF: {os.path.basename(filepath)} ---")
                    parse_pdf_financial_data(filepath)

    if all_downloads:
        save_metadata(all_downloads)

    print(f"\n{'=' * 60}")
    print(f"✅ 完成! 共{'将' if dry_run else '已'}下载 {len(all_downloads)} 份文件")
    print(f"📁 输出目录: {DOWNLOAD_DIR}")
    print(f"{'=' * 60}")


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="上市公司年报/研报抓取工具")
    parser.add_argument("--stock", type=str, help="股票代码 (如 600519)")
    parser.add_argument("--stocks", type=str, help="多个股票代码，逗号分隔")
    parser.add_argument("--year", type=int, help="年份")
    parser.add_argument("--years", type=str, help="多个年份，逗号分隔")
    parser.add_argument("--type", type=str, default="annual",
                        choices=["annual", "semi-annual", "quarterly", "prospectus"],
                        help="报告类型")
    parser.add_argument("--dry-run", action="store_true", help="仅搜索，不下载")
    parser.add_argument("--parse-pdf", action="store_true", help="下载后解析PDF")
    parser.add_argument("--research", action="store_true", help="研报模式（预留）")
    parser.add_argument("--months", type=int, default=3, help="研报时间范围（月）")

    args = parser.parse_args()

    # 解析参数
    stock_codes = []
    if args.stocks:
        stock_codes = [s.strip() for s in args.stocks.split(",")]
    elif args.stock:
        stock_codes = [args.stock]
    else:
        print("[ERROR] 请指定 --stock 或 --stocks", file=sys.stderr)
        sys.exit(1)

    years = []
    if args.years:
        years = [int(y.strip()) for y in args.years.split(",")]
    elif args.year:
        years = [args.year]
    else:
        years = [datetime.now().year - 1]  # 默认去年

    for stock in stock_codes:
        if len(stock_codes) > 1:
            print(f"\n{'#' * 60}")
            print(f"# 处理: {stock}")
            print(f"{'#' * 60}\n")

        run_fetch(
            stock_code=stock,
            years=years,
            report_type=args.type,
            dry_run=args.dry_run,
            parse_pdf=args.parse_pdf,
        )

        if len(stock_codes) > 1:
            random_delay(2, 5)  # 公司间延迟更长


if __name__ == "__main__":
    main()
