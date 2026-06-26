#!/usr/bin/env python3
"""
fetch_data.py - 从同花顺问财获取 A 股市场数据

自动获取：
- 三大指数（上证指数、深证成指、创业板指）点位和涨跌幅
- 涨跌家数（上涨家数、下跌家数）

手动补充：
- 成交量数据（今日量能、昨日量能）
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# 缓存配置
CACHE_DIR = Path(__file__).parent.parent / "cache"
MANUAL_DIR = Path(__file__).parent.parent / "manual"
CACHE_TTL_HOURS = 24

# 占位符
PLACEHOLDER = None
PLACEHOLDER_STR = "待补充"

# 问财 URL 配置
IWENCAI_BASE_URL = "https://www.iwencai.com/unifiedwap/result"

INDEX_QUERIES = {
    'shanghai': '上证指数',
    'shenzhen': '深证成指',
    'chinext': '创业板指',
}

SENTIMENT_QUERIES = {
    'up': 'A 股上涨数量',
    'down': 'A 股下跌数量',
}


def get_cache_path(date: str) -> Path:
    """获取缓存文件路径"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{date}.json"


def get_manual_path(date: str) -> Path:
    """获取手动补充数据文件路径"""
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    return MANUAL_DIR / f"{date}.json"


def load_cache(date: str) -> Optional[Dict[str, Any]]:
    """加载缓存数据"""
    cache_path = get_cache_path(date)
    if not cache_path.exists():
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查缓存是否过期（24 小时）
        cached_at = datetime.fromisoformat(data.get('_cached_at', ''))
        if datetime.now() - cached_at > timedelta(hours=CACHE_TTL_HOURS):
            print(f"[INFO] 缓存已过期：{cache_path}")
            return None
        
        print(f"[INFO] 加载缓存：{cache_path}")
        return data
    except Exception as e:
        print(f"[WARN] 缓存读取失败：{e}", file=sys.stderr)
        return None


def save_cache(date: str, data: Dict[str, Any]) -> None:
    """保存缓存数据"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = get_cache_path(date)
    
    data['_cached_at'] = datetime.now().isoformat()
    data['_date'] = date
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 缓存已保存：{cache_path}")


def load_manual_data(date: str) -> Dict[str, Any]:
    """加载手动补充数据"""
    manual_path = get_manual_path(date)
    if not manual_path.exists():
        return {}
    
    try:
        with open(manual_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] 手动数据读取失败：{e}", file=sys.stderr)
        return {}


def save_manual_data(date: str, data: Dict[str, Any]) -> None:
    """保存手动补充数据"""
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    manual_path = get_manual_path(date)
    
    with open(manual_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 手动数据已保存：{manual_path}")


def is_trading_day(date_str: str) -> bool:
    """
    检查是否为交易日
    简单规则：排除周末（暂不处理节假日）
    """
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # 排除周末（周六=5, 周日=6）
        return date.weekday() < 5
    except ValueError:
        return False


def get_previous_trading_day(date_str: str, max_days: int = 7) -> str:
    """
    获取前一个交易日
    如为非交易日，往前推直到找到交易日
    """
    date = datetime.strptime(date_str, '%Y-%m-%d')
    
    for i in range(1, max_days + 1):
        prev_date = date - timedelta(days=i)
        prev_date_str = prev_date.strftime('%Y-%m-%d')
        if is_trading_day(prev_date_str):
            return prev_date_str
    
    # 超过最大天数，返回原日期
    print(f"[WARN] 往前推{max_days}天未找到交易日，使用原日期：{date_str}")
    return date_str


def build_iwencai_url(query: str) -> str:
    """构建同花顺问财 URL"""
    return f"{IWENCAI_BASE_URL}?w={query}&querytype=zhishu"


def parse_index_snapshot(snapshot_text: str, index_name: str) -> Dict[str, Any]:
    """
    解析指数数据 snapshot
    
    期望格式（aria snapshot）：
    heading "上证指数 (000001)" [level=4]
    generic [ref=e116]: 3957.05-49.50/-1.24%
    
    返回：
    {'point': 3957.05, 'change': -1.24}
    """
    # 模式 1：标准格式 - 点位 + 涨跌额/涨跌幅
    # 示例：3957.05-49.50/-1.24% 或 3957.05 -49.50 /-1.24%
    pattern1 = r'(\d{4}\.\d{2})\s*([+-]?\d+\.?\d*)\s*/\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern1, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(3))  # 涨跌幅
        return {'point': point, 'change': change}
    
    # 模式 2：宽松格式 - 只提取点位和涨跌幅
    pattern2 = r'(\d{4}\.\d{2}).*?([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern2, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    return {'point': PLACEHOLDER, 'change': PLACEHOLDER, 'error': '解析失败'}


def parse_sentiment_from_conditions(snapshot_text: str) -> Dict[str, Any]:
    """
    从条件筛选结果解析涨跌家数
    
    期望格式：
    generic "涨跌幅>0%" [ref=e126]: 涨跌幅>0% (662 个)
    generic "涨跌幅<0%" [ref=e127]: 涨跌幅<0% (4786 个)
    
    返回：
    {'up': 662, 'down': 4786}
    """
    result = {'up': PLACEHOLDER, 'down': PLACEHOLDER}
    
    # 解析上涨家数：涨跌幅>0% (XXX 个)
    up_match = re.search(r'涨跌幅\s*>\s*0%.*?\((\d+)\s*个\)', snapshot_text)
    if up_match:
        result['up'] = int(up_match.group(1))
    
    # 解析下跌家数：涨跌幅<0% (XXX 个)
    down_match = re.search(r'涨跌幅\s*<\s*0%.*?\((\d+)\s*个\)', snapshot_text)
    if down_match:
        result['down'] = int(down_match.group(1))
    
    return result


def parse_sentiment_snapshot(snapshot_text: str, data_type: str) -> Dict[str, Any]:
    """
    解析涨跌家数 snapshot
    
    期望格式：
    下跌家数为 4785 家
    上涨家数：1234
    
    返回：
    {'count': 4785}
    """
    # 模式 1：标准格式 - "XX 家数为 XXXX 家"
    pattern1 = rf'{data_type}.*?为\s*(\d+)\s*家'
    match = re.search(pattern1, snapshot_text, re.IGNORECASE)
    if match:
        return {'count': int(match.group(1))}
    
    # 模式 2：宽松格式 - 提取数字
    pattern2 = r'(\d+)\s*家'
    matches = re.findall(pattern2, snapshot_text)
    if matches:
        return {'count': int(matches[0])}
    
    # 模式 3：纯数字提取
    numbers = re.findall(r'\d+', snapshot_text)
    if numbers:
        return {'count': int(numbers[0])}
    
    return {'count': PLACEHOLDER, 'error': '解析失败'}


def fetch_with_browser(url: str, timeout_ms: int = 30000) -> str:
    """
    使用 OpenClaw browser 工具获取数据
    
    这是伪代码框架，实际由外部调用
    """
    print(f"[INFO] 访问：{url}")
    # 实际调用：
    # browser.navigate(url)
    # snapshot = browser.snapshot(refs="aria")
    # return snapshot
    return ""


def fetch_index_data(index_key: str, index_name: str) -> Dict[str, Any]:
    """获取指数数据"""
    query = INDEX_QUERIES.get(index_key, index_name)
    url = build_iwencai_url(query)
    print(f"[INFO] 获取 {index_name} 数据...")
    
    # TODO: 实际调用 browser 工具
    # snapshot = fetch_with_browser(url)
    # result = parse_index_snapshot(snapshot, index_name)
    
    # 临时返回占位符
    return {'point': PLACEHOLDER, 'change': PLACEHOLDER, 'error': '待实现浏览器调用'}


def fetch_sentiment_data(data_type: str, query: str) -> Dict[str, Any]:
    """获取涨跌家数数据"""
    url = build_iwencai_url(query)
    print(f"[INFO] 获取 {data_type} 数据...")
    
    # TODO: 实际调用 browser 工具
    # snapshot = fetch_with_browser(url)
    # result = parse_sentiment_snapshot(snapshot, data_type)
    
    # 临时返回占位符
    return {'count': PLACEHOLDER, 'error': '待实现浏览器调用'}


def fetch_all_data(date: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    获取所有数据
    
    Args:
        date: 日期字符串 (YYYY-MM-DD)
        force_refresh: 是否强制刷新（忽略缓存）
    
    Returns:
        完整数据字典
    """
    # 处理非交易日
    actual_date = date
    if not is_trading_day(date):
        actual_date = get_previous_trading_day(date)
        print(f"[INFO] {date} 为非交易日，使用最近交易日：{actual_date}")
    
    # 检查缓存
    if not force_refresh:
        cached = load_cache(actual_date)
        if cached:
            print(f"[INFO] 使用缓存数据：{actual_date}")
            cached['_from_cache'] = True
            return cached
    
    print(f"[INFO] 重新获取数据：{actual_date}")
    
    # 获取指数数据
    indices = {}
    for key, name in INDEX_QUERIES.items():
        indices[key] = fetch_index_data(key, name)
    
    # 获取涨跌家数
    sentiment = {}
    for key, query in SENTIMENT_QUERIES.items():
        result = fetch_sentiment_data(key, query)
        sentiment[key] = result.get('count', PLACEHOLDER)
    
    # 计算涨跌比
    up = sentiment.get('up')
    down = sentiment.get('down')
    if up is not PLACEHOLDER and down is not PLACEHOLDER and down > 0:
        ratio_value = down / up if up > 0 else 0
        ratio = f"1:{ratio_value:.1f}"
        
        if up > down * 2:
            desc = "上涨显著多于下跌"
        elif down > up * 2:
            desc = "下跌显著多于上涨"
        else:
            desc = "涨跌相当"
    else:
        ratio = PLACEHOLDER_STR
        desc = PLACEHOLDER_STR
    
    sentiment['ratio'] = ratio
    sentiment['description'] = desc
    
    # 加载手动补充数据
    manual_data = load_manual_data(actual_date)
    
    # 构建完整数据
    data = {
        'date': actual_date,
        'query_date': date,
        'indices': indices,
        'sentiment': sentiment,
        'volume': {
            'today': manual_data.get('volume', {}).get('today', PLACEHOLDER),
            'previous': manual_data.get('volume', {}).get('previous', PLACEHOLDER),
        },
        '_from_cache': False,
        'dataSource': 'iwencai',
        'manualDataRequired': [
            'volume.today',
            'volume.previous',
        ],
    }
    
    # 保存缓存
    save_cache(actual_date, data)
    
    return data


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='获取 A 股市场数据')
    parser.add_argument('date', nargs='?', default=None, help='日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--force', action='store_true', help='强制刷新，忽略缓存')
    parser.add_argument('--json', action='store_true', help='仅输出 JSON')
    
    args = parser.parse_args()
    
    # 确定日期
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 获取数据
    data = fetch_all_data(date, force_refresh=args.force)
    
    # 输出
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
