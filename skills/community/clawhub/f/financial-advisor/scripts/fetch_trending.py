#!/usr/bin/env python3
"""
全网热点趋势采集脚本
===========================
优先通过 DailyHotApi 统一接口采集热榜数据，失败时自动回退到各平台公开接口直采。

采集策略（两级 fallback）：
  Level 1 — DailyHotApi（聚合 API，覆盖 40+ 平台，响应快）
  Level 2 — 各平台原生接口/页面（直采兜底，无需外部服务）

支持数据源（13个）：
  基础源（7个，默认采集）：
    1. 百度热搜 — 国家政策、社会事件、全球时事、经济动态
    2. 微博热搜 — 时事热点、政策发布、舆情风向
    3. 知乎热榜 — 深度讨论、政策解读、行业分析
    4. 今日头条 — 时政、社会、国际、科技
    5. 雪球财经 — 股票投资、财经新闻、市场分析
    6. 36氪     — 创业、商业、投融资、科技资讯
    7. 澎湃新闻 — 时政、社会、国际

  扩展源（6个，按行业选用）：
    8. IT之家   — 科技产业新闻
    9. 虎扑     — 体育/消费品
   10. 少数派   — 数码/效率
   11. 哔哩哔哩 — 视频/文化/年轻消费
   12. 抖音     — 消费趋势/社会舆情
   13. 豆瓣     — 文化/消费

输出格式：兼容 macro_analysis.py 的 load_trending_data() 函数

用法：
  # 采集基础 7 个源
  python fetch_trending.py --output trending.json

  # 采集全部源
  python fetch_trending.py --output trending.json --all

  # 指定源
  python fetch_trending.py --output trending.json --sources baidu,weibo,xueqiu

  # 按行业扩展
  python fetch_trending.py --output trending.json --industry 科技

  # 指定每个源获取的条目数
  python fetch_trending.py --output trending.json --limit 20

  # 指定自定义 DailyHotApi 实例（默认使用公共实例）
  python fetch_trending.py --output trending.json --api-base https://my-dailyhot.example.com

  # 跳过 DailyHotApi，仅使用直采
  python fetch_trending.py --output trending.json --no-api

依赖：requests（已在 requirements.txt 中）
"""

import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print('Error: requests 未安装，请运行 pip install requests', file=sys.stderr)
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('fetch_trending')

# ---------------------------------------------------------------------------
# 通用请求工具
# ---------------------------------------------------------------------------

DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

REQUEST_TIMEOUT = 15


def _safe_request(url, headers=None, timeout=REQUEST_TIMEOUT, **kwargs):
    """安全的 HTTP 请求，带重试。"""
    hdrs = {**DEFAULT_HEADERS, **(headers or {})}
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=hdrs, timeout=timeout, **kwargs)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt == 2:
                logger.warning(f'请求失败 ({url}): {e}')
                return None
            time.sleep(1 * (attempt + 1))
    return None


# ---------------------------------------------------------------------------
# DailyHotApi 公共实例（优先采集层）
# ---------------------------------------------------------------------------

# 默认公共实例地址（imsyy/DailyHotApi 项目）
DAILYHOT_API_BASE = 'https://api-hot.imsyy.top'

# DailyHotApi 路由名称 ↔ 本脚本源名称 的映射
DAILYHOT_ROUTE_MAP = {
    'baidu': 'baidu',
    'weibo': 'weibo',
    'zhihu': 'zhihu',
    'toutiao': 'toutiao',
    # 雪球在 DailyHotApi 中无直接路由，使用直采
    '36kr': '36kr',
    'thepaper': 'thepaper',
    'ithome': 'ithome',
    'hupu': 'hupu',
    'sspai': 'sspai',
    'bilibili': 'bilibili',
    'douyin': 'douyin',
    'douban-movie': 'douban',
}

# 反向映射：本脚本源名称 → DailyHotApi 路由
SOURCE_TO_ROUTE = {v: k for k, v in DAILYHOT_ROUTE_MAP.items()}


def _fetch_from_dailyhot_api(source_name, api_base=DAILYHOT_API_BASE, limit=20):
    """
    通过 DailyHotApi 统一接口获取热榜数据。

    Args:
        source_name: 本脚本的源名称（如 'baidu'、'weibo'）
        api_base: DailyHotApi 实例地址
        limit: 获取条目数

    Returns:
        dict: 统一格式的源数据，失败返回 None
    """
    route = SOURCE_TO_ROUTE.get(source_name)
    if not route:
        return None

    url = f'{api_base}/{route}'
    resp = _safe_request(url, timeout=10)
    if not resp:
        return None

    try:
        data = resp.json()
        # DailyHotApi 标准返回格式：{ code: 200, data: [...], title: "...", ... }
        if data.get('code') != 200:
            logger.debug(f'DailyHotApi {route} 返回非200: {data.get("code")}')
            return None

        items_raw = data.get('data', [])
        if not items_raw:
            return None

        source_desc = SOURCE_REGISTRY.get(source_name, {}).get('desc', source_name)
        items = []
        for v in items_raw[:limit]:
            title = v.get('title', '')
            if not title:
                continue
            items.append({
                'title': title,
                'url': v.get('url', v.get('mobileUrl', '')),
                'hot': int(v.get('hot', 0) or 0),
            })

        if not items:
            return None

        return {
            'source': source_name,
            'source_name': source_desc,
            'items': items,
            'via': 'DailyHotApi',
        }
    except Exception as e:
        logger.debug(f'DailyHotApi {route} 解析失败: {e}')
        return None


# ---------------------------------------------------------------------------
# 各平台热榜采集器
# ---------------------------------------------------------------------------

def fetch_baidu(limit=20):
    """百度热搜。"""
    url = 'https://top.baidu.com/board?tab=realtime'
    resp = _safe_request(url)
    if not resp:
        return None
    try:
        match = re.search(r'<!--s-data:(.*?)-->', resp.text, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group(1))
        cards = data.get('data', {}).get('cards', [])
        if not cards:
            return None
        content = cards[0].get('content', [])
        items = []
        for i, v in enumerate(content[:limit]):
            items.append({
                'title': v.get('word', v.get('title', '')),
                'url': f"https://www.baidu.com/s?wd={requests.utils.quote(v.get('word', v.get('title', '')))}",
                'hot': int(v.get('hotScore', 0) or 0),
            })
        return {
            'source': 'baidu',
            'source_name': '百度热搜',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'百度热搜解析失败: {e}')
        return None


def fetch_weibo(limit=20):
    """微博热搜。"""
    url = 'https://weibo.com/ajax/side/hotSearch'
    resp = _safe_request(url, headers={**DEFAULT_HEADERS, 'Referer': 'https://weibo.com/'})
    if not resp:
        return None
    try:
        data = resp.json()
        realtime = data.get('data', {}).get('realtime', [])
        items = []
        for v in realtime[:limit]:
            word = v.get('word', '')
            items.append({
                'title': word,
                'url': f'https://s.weibo.com/weibo?q=%23{requests.utils.quote(word)}%23',
                'hot': int(v.get('num', 0) or 0),
            })
        return {
            'source': 'weibo',
            'source_name': '微博热搜',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'微博热搜解析失败: {e}')
        return None


def fetch_zhihu(limit=20):
    """知乎热榜。"""
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://www.zhihu.com/hot',
    })
    if not resp:
        return None
    try:
        data = resp.json()
        items = []
        for v in data.get('data', [])[:limit]:
            target = v.get('target', {})
            items.append({
                'title': target.get('title', ''),
                'url': f"https://www.zhihu.com/question/{target.get('id', '')}",
                'hot': int(v.get('detail_text', '0').replace(' 万热度', '0000').replace(' 热度', '').replace(',', '') or 0),
            })
        return {
            'source': 'zhihu',
            'source_name': '知乎热榜',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'知乎热榜解析失败: {e}')
        return None


def fetch_toutiao(limit=20):
    """今日头条热榜。"""
    url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://www.toutiao.com/',
    })
    if not resp:
        return None
    try:
        data = resp.json()
        items = []
        for v in data.get('data', [])[:limit]:
            items.append({
                'title': v.get('Title', ''),
                'url': v.get('Url', ''),
                'hot': int(v.get('HotValue', 0) or 0),
            })
        return {
            'source': 'toutiao',
            'source_name': '今日头条',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'今日头条解析失败: {e}')
        return None


def fetch_xueqiu(limit=20):
    """雪球财经热帖。"""
    # 先获取 cookie
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    try:
        session.get('https://xueqiu.com/', timeout=REQUEST_TIMEOUT)
    except Exception:
        pass
    url = f'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size={limit}&_type=10&type=10'
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        items = []
        for v in data.get('data', {}).get('items', []):
            code = v.get('code', '')
            name = v.get('name', '')
            items.append({
                'title': f"{name}({code})" if code else name,
                'url': f'https://xueqiu.com/S/{code}' if code else '',
                'hot': int(v.get('value', 0) or 0),
            })
        return {
            'source': 'xueqiu',
            'source_name': '雪球财经',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'雪球财经解析失败: {e}')
        return None


def fetch_36kr(limit=20):
    """36氪热榜。"""
    url = 'https://36kr.com/api/newsflash'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://36kr.com/',
    }, params={'per_page': limit})
    if not resp:
        # 备选：36kr 热门文章
        url2 = 'https://gateway.36kr.com/api/mis/nav/home/nav/rank/hot'
        resp = _safe_request(url2, headers={
            **DEFAULT_HEADERS,
            'Referer': 'https://36kr.com/',
            'Content-Type': 'application/json',
        })
        if not resp:
            return None
    try:
        data = resp.json()
        items_raw = data.get('data', {}).get('items', data.get('data', {}).get('hotRankList', []))
        if not items_raw and isinstance(data.get('data'), list):
            items_raw = data['data']
        items = []
        for v in items_raw[:limit]:
            if isinstance(v, dict):
                title = v.get('title', v.get('templateMaterial', {}).get('widgetTitle', ''))
                item_id = v.get('id', v.get('itemId', ''))
                items.append({
                    'title': title,
                    'url': f'https://36kr.com/p/{item_id}' if item_id else '',
                    'hot': int(v.get('hot', v.get('popularity', 0)) or 0),
                })
        return {
            'source': '36kr',
            'source_name': '36氪',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'36氪解析失败: {e}')
        return None


def fetch_thepaper(limit=20):
    """澎湃新闻热榜。"""
    url = 'https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar'
    resp = _safe_request(url)
    if not resp:
        return None
    try:
        data = resp.json()
        hot_news = data.get('data', {}).get('hotNews', [])
        items = []
        for v in hot_news[:limit]:
            items.append({
                'title': v.get('name', ''),
                'url': f"https://www.thepaper.cn/newsDetail_forward_{v.get('contId', '')}",
                'hot': int(v.get('praiseTimes', 0) or 0),
            })
        return {
            'source': 'thepaper',
            'source_name': '澎湃新闻',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'澎湃新闻解析失败: {e}')
        return None


def fetch_ithome(limit=20):
    """IT之家热榜。"""
    url = 'https://m.ithome.com/api/news/newslistpageget?categoryid=0&amppage=0&pagesize=30'
    resp = _safe_request(url)
    if not resp:
        return None
    try:
        data = resp.json()
        items_raw = data.get('Result', [])
        items = []
        for v in items_raw[:limit]:
            items.append({
                'title': v.get('Title', ''),
                'url': v.get('Url', v.get('NewsUrl', '')),
                'hot': int(v.get('CommentCount', 0) or 0),
            })
        return {
            'source': 'ithome',
            'source_name': 'IT之家',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'IT之家解析失败: {e}')
        return None


def fetch_hupu(limit=20):
    """虎扑步行街热帖。"""
    url = 'https://bbs.hupu.com/all-gambia'
    resp = _safe_request(url)
    if not resp:
        return None
    try:
        # 从页面提取热帖
        items = []
        # 尝试 JSON 嵌入数据
        match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            threads = (
                data.get('props', {}).get('pageProps', {}).get('threads', [])
                or data.get('props', {}).get('pageProps', {}).get('hotThreads', [])
            )
            for v in threads[:limit]:
                items.append({
                    'title': v.get('title', ''),
                    'url': f"https://bbs.hupu.com/{v.get('tid', '')}",
                    'hot': int(v.get('replies', 0) or 0),
                })
        return {
            'source': 'hupu',
            'source_name': '虎扑',
            'items': items,
        } if items else None
    except Exception as e:
        logger.warning(f'虎扑解析失败: {e}')
        return None


def fetch_sspai(limit=20):
    """少数派热榜。"""
    url = 'https://sspai.com/api/v1/article/tag/page/get?limit=20&offset=0&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0'
    resp = _safe_request(url)
    if not resp:
        return None
    try:
        data = resp.json()
        items_raw = data.get('data', [])
        items = []
        for v in items_raw[:limit]:
            items.append({
                'title': v.get('title', ''),
                'url': f"https://sspai.com/post/{v.get('id', '')}",
                'hot': int(v.get('like_count', 0) or 0),
            })
        return {
            'source': 'sspai',
            'source_name': '少数派',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'少数派解析失败: {e}')
        return None


def fetch_bilibili(limit=20):
    """哔哩哔哩热门。"""
    url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://www.bilibili.com/',
    })
    if not resp:
        return None
    try:
        data = resp.json()
        items_raw = data.get('data', {}).get('list', [])
        items = []
        for v in items_raw[:limit]:
            items.append({
                'title': v.get('title', ''),
                'url': f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                'hot': int(v.get('stat', {}).get('view', 0) or 0),
            })
        return {
            'source': 'bilibili',
            'source_name': '哔哩哔哩',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'哔哩哔哩解析失败: {e}')
        return None


def fetch_douyin(limit=20):
    """抖音热榜。"""
    url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://www.douyin.com/',
    })
    if not resp:
        return None
    try:
        data = resp.json()
        word_list = data.get('data', {}).get('word_list', [])
        items = []
        for v in word_list[:limit]:
            word = v.get('word', '')
            items.append({
                'title': word,
                'url': f'https://www.douyin.com/search/{requests.utils.quote(word)}',
                'hot': int(v.get('hot_value', 0) or 0),
            })
        return {
            'source': 'douyin',
            'source_name': '抖音',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'抖音解析失败: {e}')
        return None


def fetch_douban(limit=20):
    """豆瓣讨论精选/电影。"""
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=20&page_start=0'
    resp = _safe_request(url, headers={
        **DEFAULT_HEADERS,
        'Referer': 'https://movie.douban.com/',
    })
    if not resp:
        return None
    try:
        data = resp.json()
        subjects = data.get('subjects', [])
        items = []
        for v in subjects[:limit]:
            items.append({
                'title': v.get('title', ''),
                'url': v.get('url', ''),
                'hot': int(float(v.get('rate', 0) or 0) * 10000),
            })
        return {
            'source': 'douban',
            'source_name': '豆瓣',
            'items': items,
        }
    except Exception as e:
        logger.warning(f'豆瓣解析失败: {e}')
        return None


# ---------------------------------------------------------------------------
# 数据源注册表
# ---------------------------------------------------------------------------

SOURCE_REGISTRY = {
    # 基础源
    'baidu': {'fn': fetch_baidu, 'group': 'base', 'desc': '百度热搜'},
    'weibo': {'fn': fetch_weibo, 'group': 'base', 'desc': '微博热搜'},
    'zhihu': {'fn': fetch_zhihu, 'group': 'base', 'desc': '知乎热榜'},
    'toutiao': {'fn': fetch_toutiao, 'group': 'base', 'desc': '今日头条'},
    'xueqiu': {'fn': fetch_xueqiu, 'group': 'base', 'desc': '雪球财经'},
    '36kr': {'fn': fetch_36kr, 'group': 'base', 'desc': '36氪'},
    'thepaper': {'fn': fetch_thepaper, 'group': 'base', 'desc': '澎湃新闻'},
    # 扩展源
    'ithome': {'fn': fetch_ithome, 'group': 'extra', 'desc': 'IT之家'},
    'hupu': {'fn': fetch_hupu, 'group': 'extra', 'desc': '虎扑'},
    'sspai': {'fn': fetch_sspai, 'group': 'extra', 'desc': '少数派'},
    'bilibili': {'fn': fetch_bilibili, 'group': 'extra', 'desc': '哔哩哔哩'},
    'douyin': {'fn': fetch_douyin, 'group': 'extra', 'desc': '抖音'},
    'douban': {'fn': fetch_douban, 'group': 'extra', 'desc': '豆瓣'},
}

# 行业 → 推荐扩展源映射
INDUSTRY_SOURCES = {
    '科技': ['ithome', 'bilibili'],
    '半导体': ['ithome'],
    'AI': ['ithome', 'bilibili'],
    '互联网': ['ithome', 'bilibili', 'douyin'],
    '消费': ['douyin', 'bilibili', 'douban'],
    '零售': ['douyin', 'bilibili'],
    '品牌': ['douyin', 'bilibili'],
    '汽车': ['ithome'],
    '新能源': ['ithome'],
    '传媒': ['ithome', 'bilibili', 'douyin'],
    '体育': ['hupu'],
    '运动品牌': ['hupu'],
    '文化': ['douban', 'bilibili'],
    '娱乐': ['douban', 'bilibili', 'douyin'],
    '数码': ['sspai', 'ithome'],
    '金融': [],
    '银行': [],
}

BASE_SOURCES = [k for k, v in SOURCE_REGISTRY.items() if v['group'] == 'base']


def resolve_sources(sources_str=None, industry=None, use_all=False):
    """根据参数解析需要采集的数据源列表。"""
    if use_all:
        return list(SOURCE_REGISTRY.keys())

    if sources_str:
        requested = [s.strip() for s in sources_str.split(',')]
        valid = [s for s in requested if s in SOURCE_REGISTRY]
        if not valid:
            logger.warning(f'未找到有效数据源: {sources_str}，使用基础源')
            return BASE_SOURCES
        return valid

    result = list(BASE_SOURCES)
    if industry:
        for key, extras in INDUSTRY_SOURCES.items():
            if key in industry:
                for src in extras:
                    if src not in result:
                        result.append(src)
    return result


# ---------------------------------------------------------------------------
# 主采集逻辑
# ---------------------------------------------------------------------------

def fetch_all_trending(sources, limit=20, max_workers=5, api_base=DAILYHOT_API_BASE, use_api=True):
    """
    并发采集多个平台的热榜数据（两级 fallback）。

    策略：
      1. 优先通过 DailyHotApi 统一接口获取
      2. DailyHotApi 失败的源，回退到各平台原生接口直采

    Args:
        sources: 数据源列表
        limit: 每个源获取的条目数
        max_workers: 最大并发数
        api_base: DailyHotApi 实例地址
        use_api: 是否使用 DailyHotApi（False 则跳过，直接使用直采）

    Returns:
        dict: 统一格式的热点数据
    """
    results = []
    failed = []
    api_success = []
    fallback_success = []

    def _fetch_one(source_name):
        info = SOURCE_REGISTRY[source_name]
        logger.info(f'采集中: {info["desc"]} ({source_name})...')

        # Level 1: DailyHotApi
        if use_api:
            result = _fetch_from_dailyhot_api(source_name, api_base=api_base, limit=limit)
            if result and result.get('items'):
                logger.info(f'  ✓ {info["desc"]}: {len(result["items"])} 条 (via DailyHotApi)')
                return result, 'api'

        # Level 2: 各平台原生接口直采
        try:
            result = info['fn'](limit=limit)
            if result and result.get('items'):
                result['via'] = 'direct'
                logger.info(f'  ✓ {info["desc"]}: {len(result["items"])} 条 (via 直采)')
                return result, 'fallback'
            else:
                logger.warning(f'  ✗ {info["desc"]}: 无数据')
                return None, 'none'
        except Exception as e:
            logger.warning(f'  ✗ {info["desc"]}: {e}')
            return None, 'none'

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_fetch_one, src): src for src in sources}
        for future in as_completed(future_map):
            src_name = future_map[future]
            try:
                result, method = future.result()
                if result:
                    results.append(result)
                    if method == 'api':
                        api_success.append(src_name)
                    else:
                        fallback_success.append(src_name)
                else:
                    failed.append(src_name)
            except Exception as e:
                logger.warning(f'{src_name} 异常: {e}')
                failed.append(src_name)

    total_items = sum(len(r['items']) for r in results)
    now_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    output = {
        'sources': results,
        'fetch_time': now_str,
        'metadata': {
            'total_sources': len(results),
            'total_items': total_items,
            'failed_sources': failed,
            'requested_sources': sources,
            'api_success': api_success,
            'fallback_success': fallback_success,
            'api_base': api_base if use_api else None,
        },
    }

    logger.info(f'\n采集完成: {len(results)}/{len(sources)} 个源成功，共 {total_items} 条热点')
    if api_success:
        logger.info(f'  DailyHotApi 成功: {", ".join(api_success)}')
    if fallback_success:
        logger.info(f'  直采兜底成功: {", ".join(fallback_success)}')
    if failed:
        logger.warning(f'  失败的源: {", ".join(failed)}')

    return output


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='全网热点趋势采集工具（DailyHotApi 优先 + 各平台直采兜底）'
    )
    parser.add_argument('--output', '-o', required=True, help='输出 JSON 文件路径')
    parser.add_argument('--sources', default='', help='指定数据源（逗号分隔），如: baidu,weibo,xueqiu')
    parser.add_argument('--industry', default='', help='行业名称，自动扩展相关数据源')
    parser.add_argument('--all', action='store_true', help='采集全部 13 个数据源')
    parser.add_argument('--limit', type=int, default=20, help='每个源获取的条目数（默认 20）')
    parser.add_argument('--list-sources', action='store_true', help='列出所有可用数据源')
    parser.add_argument('--api-base', default=DAILYHOT_API_BASE,
                        help=f'DailyHotApi 实例地址（默认: {DAILYHOT_API_BASE}）')
    parser.add_argument('--no-api', action='store_true',
                        help='跳过 DailyHotApi，仅使用各平台直采')

    args = parser.parse_args()

    if args.list_sources:
        print('\n可用数据源：')
        print(f'{"名称":<12} {"分组":<8} {"DailyHotApi":<14} {"说明"}')
        print('-' * 55)
        for name, info in SOURCE_REGISTRY.items():
            group_label = '基础' if info['group'] == 'base' else '扩展'
            api_label = '✓' if name in SOURCE_TO_ROUTE else '—（仅直采）'
            print(f'{name:<12} {group_label:<8} {api_label:<14} {info["desc"]}')
        print(f'\n基础源（默认采集）: {", ".join(BASE_SOURCES)}')
        print(f'\n采集策略: DailyHotApi 优先 → 失败自动回退到各平台直采')
        print(f'DailyHotApi 默认实例: {DAILYHOT_API_BASE}')
        print('\n行业扩展映射：')
        for industry, extras in INDUSTRY_SOURCES.items():
            if extras:
                print(f'  {industry}: +{", ".join(extras)}')
        return

    # 解析数据源
    sources = resolve_sources(
        sources_str=args.sources or None,
        industry=args.industry or None,
        use_all=args.all,
    )

    logger.info(f'计划采集 {len(sources)} 个源: {", ".join(sources)}')

    # 执行采集
    data = fetch_all_trending(
        sources, limit=args.limit,
        api_base=args.api_base, use_api=not args.no_api,
    )

    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    logger.info(f'结果已保存: {output_path}')

    # 打印摘要到 stdout（供 AI 读取）
    print(json.dumps({
        'status': 'success',
        'output_file': str(output_path),
        'sources_count': data['metadata']['total_sources'],
        'total_items': data['metadata']['total_items'],
        'failed_sources': data['metadata']['failed_sources'],
        'fetch_time': data['fetch_time'],
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
