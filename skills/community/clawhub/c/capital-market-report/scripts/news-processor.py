# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///

"""
智能新闻处理器 v2 - 均衡中外新闻源
修复: CLS API失效、中文源不足、shell脚本依赖
"""

import json
import hashlib
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import requests

# ==========================================
# 配置
# ==========================================
CACHE_DIR = Path(os.path.expanduser("~/.openclaw/workspace-group/market-monitor/news_cache"))
CACHE_DURATION_HOURS = 24
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 中文新闻源 (10个)
# ==========================================
CHINESE_SOURCES = [
    {
        "name": "新浪财经",
        "url": "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50",
        "parser": "sina"
    },
    {
        "name": "华尔街见闻",
        "url": "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=40",
        "parser": "wallstreetcn"
    },
    {
        "name": "东方财富快讯",
        "url": "https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&columnId=102&pageSize=10&pageIndex=1",
        "parser": "eastmoney"
    },
    {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "parser": "rss"
    },
    {
        "name": "界面新闻",
        "url": "https://a.jiemian.com/index.php?m=article&a=rss",
        "parser": "rss"
    },
]

# ==========================================
# 英文新闻源 (12个)
# ==========================================
FOREIGN_RSS_SOURCES = [
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/news/rssindex", "language": "en"},
    {"name": "BBC Business", "url": "https://feeds.bbci.co.uk/news/business/rss.xml", "language": "en"},
    {"name": "WSJ Markets", "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "language": "en"},
    {"name": "Investing.com", "url": "https://www.investing.com/rss/news.rss", "language": "en"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "language": "en"},
    {"name": "Ars Technica", "url": "https://arstechnica.com/feed/", "language": "en"},
    {"name": "Reuters Business", "url": "https://www.rss-bridge.org/rss/?action=display&bridge=FilterBridge&url=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F&content_filter=Reuters", "language": "en"},
    {"name": "CNBC", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147", "language": "en"},
    {"name": "Bloomberg", "url": "https://feeds.bloomberg.com/markets/news.rss", "language": "en"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "language": "en"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "language": "en"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "language": "en"},
]


# ==========================================
# 工具函数
# ==========================================
def get_news_hash(title: str) -> str:
    return hashlib.md5(title.strip().encode()).hexdigest()[:12]


def get_topic_key(title: str) -> str:
    patterns_to_remove = [
        r'\d{1,2}日', r'\d{1,2}月', r'\d{4}年',
        r'\d+\.?\d*%', r'\d+亿', r'\d+万', r'\d+元',
        r'涨\d+%', r'跌\d+%', r'超\d+%', r'近\d+%',
        r'目标价\d+', r'评级.*', r'维持.*评级',
    ]
    topic = title
    for pattern in patterns_to_remove:
        topic = re.sub(pattern, '', topic)
    topic = re.sub(r'[，。？！、：""''（）【】]', '', topic)
    return topic.strip()[:30]


def fetcher_get(url: str, timeout: int = 15) -> requests.Response:
    """统一HTTP GET，带伪装头"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    return requests.get(url, headers=headers, timeout=timeout)


# ==========================================
# 中文新闻采集
# ==========================================
def fetch_chinese_sina() -> List[Dict]:
    """新浪财经要闻"""
    news = []
    try:
        resp = fetcher_get("https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50")
        data = resp.json()
        items = data.get('result', {}).get('data', [])
        for item in items:
            title = item.get('title', '').strip()
            if not title:
                continue
            url = item.get('url', '')
            ctime = item.get('ctime', '')
            ts = int(ctime) if ctime.isdigit() else int(datetime.now().timestamp())
            news.append({
                'title': title,
                'source': '新浪财经',
                'source_type': 'chinese',
                'language': 'zh',
                'url': url,
                'timestamp': ts,
                'pub_date': datetime.fromtimestamp(ts).isoformat() if ctime.isdigit() else '',
                'fetched_at': datetime.now().isoformat()
            })
        print(f"    新浪财经: {len(news)} 条")
    except Exception as e:
        print(f"    新浪财经失败: {e}")
    return news


def fetch_chinese_wallstreetcn() -> List[Dict]:
    """华尔街见闻快讯"""
    news = []
    try:
        resp = fetcher_get("https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=40")
        data = resp.json()
        items = data.get('data', {}).get('items', [])
        for item in items:
            title = item.get('title', '').strip()
            content = item.get('content_text', '')
            if not title and content:
                title = content[:120]
            if not title:
                continue
            uri = item.get('uri', '')
            url = f"https://wallstreetcn.com/livenews/{uri}" if uri and not uri.startswith('http') else uri
            display_time = item.get('display_time', 0)
            ts = int(display_time) if display_time else int(datetime.now().timestamp())
            news.append({
                'title': title,
                'source': '华尔街见闻',
                'source_type': 'chinese',
                'language': 'zh',
                'url': url,
                'timestamp': ts,
                'pub_date': datetime.fromtimestamp(ts).isoformat(),
                'fetched_at': datetime.now().isoformat()
            })
        print(f"    华尔街见闻: {len(news)} 条")
    except Exception as e:
        print(f"    华尔街见闻失败: {e}")
    return news


def fetch_chinese_eastmoney() -> List[Dict]:
    """东方财富7x24快讯（改用HTML页面解析）"""
    news = []
    try:
        # 使用 push2 接口获取快讯
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get?np=1&fltt=2&invt=2&fields=f3,f12,f14,f2,f15,f16&secids=1.000001,0.399001,1.000300,0.399006"
        resp = fetcher_get(url)
        data = resp.json()
        # 这个接口返回行情数据，不是新闻。改为使用其他接口
    except Exception:
        pass

    # 使用东方财富公告API作为A股公司新闻源
    try:
        url = "https://np-anotice-stock.eastmoney.com/api/security/ann?page_size=20&page_index=1&ann_type=SHA,SZA"
        resp = fetcher_get(url)
        data = resp.json()
        items = data.get('data', {}).get('list', [])
        for item in items:
            title = item.get('title', '').strip()
            if not title:
                continue
            code = item.get('art_code', '')
            url = f"https://data.eastmoney.com/notices/detail/{code}.html"
            notice_date = item.get('notice_date', '')
            ts = int(datetime.strptime(notice_date[:10], '%Y-%m-%d').timestamp()) if notice_date else int(datetime.now().timestamp())
            news.append({
                'title': title,
                'source': '东方财富公告',
                'source_type': 'chinese',
                'language': 'zh',
                'url': url,
                'timestamp': ts,
                'pub_date': notice_date,
                'fetched_at': datetime.now().isoformat()
            })
        print(f"    东方财富公告: {len(news)} 条")
    except Exception as e:
        print(f"    东方财富公告失败: {e}")

    return news


def fetch_chinese_cls() -> List[Dict]:
    """财联社电报 - 从HTML JSON中提取（API已失效，改用HTML解析）"""
    news = []
    try:
        resp = fetcher_get("https://www.cls.cn/telegraph")
        html = resp.text
        
        # 查找 __NEXT_DATA__ JSON
        match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not match:
            print("    财联社: 未找到 __NEXT_DATA__")
            return news
        
        data = json.loads(match.group(1))
        telegraph_list = (
            data.get('props', {})
            .get('initialState', {})
            .get('telegraph', {})
            .get('telegraphList', [])
        )
        
        for item in telegraph_list:
            content = item.get('content', '').strip()
            title = item.get('title', '').strip()
            ctime = item.get('ctime', 0)
            article_id = item.get('id', '')
            brief = item.get('brief', '')
            
            # 用标题或摘要作为显示内容
            display = title or brief or content[:120]
            if not display:
                continue
            
            ts = int(ctime) if ctime else int(datetime.now().timestamp())
            url = f"https://www.cls.cn/detail/{article_id}" if article_id else ""
            
            news.append({
                'title': display,
                'source': '财联社',
                'source_type': 'chinese',
                'language': 'zh',
                'url': url,
                'timestamp': ts,
                'pub_date': datetime.fromtimestamp(ts).isoformat(),
                'fetched_at': datetime.now().isoformat()
            })
        print(f"    财联社: {len(news)} 条")
    except Exception as e:
        print(f"    财联社失败: {e}")
    return news


def fetch_all_chinese_news() -> List[Dict]:
    """抓取所有中文新闻源"""
    print("\n🔄 正在抓取中文新闻...")
    all_news = []
    
    # 专用解析器
    all_news.extend(fetch_chinese_sina())
    all_news.extend(fetch_chinese_wallstreetcn())
    all_news.extend(fetch_chinese_eastmoney())
    all_news.extend(fetch_chinese_cls())
    
    # RSS 源（36氪、界面等）通过通用 RSS 抓取
    rss_sources = [s for s in CHINESE_SOURCES if s.get('parser') == 'rss']
    for src in rss_sources:
        src["language"] = "zh"
        all_news.extend(fetch_rss_news(src))
    
    print(f"  ✅ 中文新闻共 {len(all_news)} 条")
    return all_news


# ==========================================
# 英文新闻采集
# ==========================================
def fetch_rss_news(source: Dict) -> List[Dict]:
    """抓取RSS源的新闻"""
    news_list = []
    try:
        resp = fetcher_get(source['url'], timeout=15)
        root = ET.fromstring(resp.content)
        
        # RSS 2.0
        channel = root.find('.//channel')
        items = channel.findall('.//item')[:15] if channel is not None else []
        
        # Atom
        if not items:
            ns = 'http://www.w3.org/2005/Atom'
            entries = root.findall(f'.//{{{ns}}}entry')
            if not entries:
                entries = root.findall('.//entry')
            
            for entry in entries[:15]:
                title_elem = entry.find(f'{{{ns}}}title') or entry.find('title')
                link_elem = entry.find(f'{{{ns}}}link') or entry.find('link')
                
                if title_elem is not None and title_elem.text:
                    title = title_elem.text.strip()
                    link = ''
                    if link_elem is not None:
                        link = link_elem.attrib.get('href', link_elem.text or '')
                    
                    news_list.append({
                        'title': f"[EN] {title}",
                        'title_original': title,
                        'source': source['name'],
                        'source_type': 'foreign',
                        'language': source['language'],
                        'url': link,
                        'timestamp': int(datetime.now().timestamp()),
                        'fetched_at': datetime.now().isoformat()
                    })
            return news_list
        
        for item in items:
            title_elem = item.find('title')
            link_elem = item.find('link')
            
            if title_elem is not None and title_elem.text:
                title = title_elem.text.strip()
                if title.startswith('<![CDATA['):
                    title = title[9:-3]
                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ''
                
                news_list.append({
                    'title': f"[EN] {title}",
                    'title_original': title,
                    'source': source['name'],
                    'source_type': 'foreign',
                    'language': source['language'],
                    'url': link,
                    'timestamp': int(datetime.now().timestamp()),
                    'fetched_at': datetime.now().isoformat()
                })
    except Exception as e:
        print(f"    抓取 {source['name']} 失败: {e}")
    
    return news_list


def fetch_all_foreign_news() -> List[Dict]:
    """抓取所有英文新闻源"""
    print("\n🔄 正在抓取英文新闻...")
    all_news = []
    for source in FOREIGN_RSS_SOURCES:
        items = fetch_rss_news(source)
        all_news.extend(items)
        print(f"    {source['name']}: {len(items)} 条")
    print(f"  ✅ 英文新闻共 {len(all_news)} 条")
    return all_news


# ==========================================
# 缓存 & 去重
# ==========================================
def load_cached_news() -> List[Dict]:
    cached_news = []
    cutoff_time = datetime.now() - timedelta(hours=CACHE_DURATION_HOURS)
    for cache_file in CACHE_DIR.glob("*.json"):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                item = json.load(f)
                cached_time = datetime.fromisoformat(item.get('cached_at', '2000-01-01'))
                if cached_time > cutoff_time:
                    cached_news.append(item)
                else:
                    cache_file.unlink()
        except Exception:
            continue
    return cached_news


def save_news_to_cache(news_list: List[Dict]):
    for news in news_list:
        title_for_hash = news.get('title_original', news['title'])
        news_hash = get_news_hash(title_for_hash)
        cache_file = CACHE_DIR / f"{news_hash}.json"
        news['cached_at'] = datetime.now().isoformat()
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)


def deduplicate_and_merge(news_list: List[Dict]) -> List[Dict]:
    """去重合并"""
    # Step 1: 标题hash去重
    unique = {}
    for news in news_list:
        h = get_news_hash(news.get('title_original', news['title']))
        if h not in unique or news.get('timestamp', 0) > unique[h].get('timestamp', 0):
            unique[h] = news
    
    # Step 2: 话题合并
    topics = {}
    for news in unique.values():
        k = get_topic_key(news.get('title_original', news['title']))
        if k not in topics or news.get('timestamp', 0) > topics[k].get('timestamp', 0):
            topics[k] = news
    
    return sorted(topics.values(), key=lambda x: x.get('timestamp', 0), reverse=True)


# ==========================================
# 情感分析
# ==========================================
def analyze_sentiment(title: str) -> str:
    title_lower = title.lower()
    
    bullish = ['上涨', '涨', '反弹', '创新高', '突破', '利好', '强劲', '增长', '超预期',
               '买入', '增持', '涨停', '飙升', '暴涨', '牛市', '资金流入',
               'rises', 'surges', 'jumps', 'gains', 'rally', 'bullish', 'upgrade', 'beats']
    bearish = ['下跌', '跌', '跳水', '崩盘', '创新低', '跌破', '利空', '疲软', '亏损', '不及预期',
               '卖出', '减持', '跌停', '暴跌', '熊市', '资金流出',
               'falls', 'plunges', 'drops', 'crash', 'bearish', 'downgrade', 'misses']
    
    b_score = sum(1 for kw in bullish if kw in title_lower)
    br_score = sum(1 for kw in bearish if kw in title_lower)
    
    if '涨停' in title or 'surges' in title_lower:
        return '利好'
    if '跌停' in title or 'plunges' in title_lower:
        return '利空'
    if '战争' in title or 'conflict' in title_lower:
        return '利空'
    if b_score > br_score:
        return '利好'
    elif br_score > b_score:
        return '利空'
    return '中性'


# ==========================================
# 报告生成
# ==========================================
def generate_raw_report(all_news: List[Dict]) -> str:
    """生成原始数据报告（供模型进一步加工）"""
    cn_news = [n for n in all_news if n.get('source_type') == 'chinese']
    en_news = [n for n in all_news if n.get('source_type') == 'foreign']
    
    bullish = [n for n in all_news if n.get('sentiment') == '利好']
    bearish = [n for n in all_news if n.get('sentiment') == '利空']
    neutral = [n for n in all_news if n.get('sentiment') == '中性']
    
    report = f"# 原始新闻数据 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
    report += f"**统计**: 🇨🇳中文 {len(cn_news)}条 | 🇬🇧英文 {len(en_news)}条 | 利好 {len(bullish)} | 利空 {len(bearish)} | 中性 {len(neutral)}\n\n"
    report += "---\n\n"
    
    def write_section(label, emoji, items, max_items=20):
        nonlocal report
        report += f"## {emoji} {label}（共{len(items)}条）\n\n"
        for i, news in enumerate(items[:max_items]):
            tag = "🇨🇳" if news.get('source_type') == 'chinese' else "🇬🇧"
            url = news.get('url', '')
            link = f"([原文]({url}))" if url else ""
            report += f"{i+1}. {news['title']}\n"
            report += f"   来源: {tag} {news['source']} {link}\n\n"
        if len(items) > max_items:
            report += f"... 还有 {len(items) - max_items} 条\n\n"
    
    write_section("利好因素", "📈", bullish)
    write_section("利空因素", "📉", bearish)
    write_section("中性/其他", "📋", neutral)
    
    report += "---\n"
    report += f"数据来源: 🇨🇳 新浪财经 / 华尔街见闻 / 东方财富 / 财联社 | 🇬🇧 {', '.join(s['name'] for s in FOREIGN_RSS_SOURCES)}\n"
    report += f"生成时间: {datetime.now().isoformat()}\n"
    
    return report


# ==========================================
# 主入口
# ==========================================
def main():
    print("=" * 50)
    print(f"📊 Capital Market News Processor v2")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 抓取中文新闻（Python 直连，不依赖 shell）
    cn_news = fetch_all_chinese_news()
    
    # 2. 抓取英文新闻
    en_news = fetch_all_foreign_news()
    
    # 3. 合并
    all_news = cn_news + en_news
    print(f"\n📦 本次共抓取 {len(all_news)} 条新闻")
    
    # 4. 加载缓存并合并
    cached = load_cached_news()
    all_news = cached + all_news
    print(f"📦 含缓存共 {len(all_news)} 条")
    
    # 5. 保存到缓存
    save_news_to_cache(cn_news + en_news)
    
    # 6. 去重
    all_news = deduplicate_and_merge(all_news)
    print(f"✅ 去重后剩余 {len(all_news)} 条 (🇨🇳{sum(1 for n in all_news if n.get('source_type')=='chinese')} / 🇬🇧{sum(1 for n in all_news if n.get('source_type')=='foreign')})")
    
    # 7. 情感分析
    print("📊 正在分析每条新闻的影响...")
    for news in all_news:
        news['sentiment'] = analyze_sentiment(news.get('title_original', news['title']))
    
    # 8. 生成原始报告
    report = generate_raw_report(all_news)
    
    # 9. 输出
    report_dir = Path(os.path.expanduser("~/.openclaw/workspace-group/market-monitor"))
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    report_file = report_dir / f"news_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 原始报告已保存: {report_file}")
    print(report[:500])
    print("...")
    
    # 10. 输出JSON统计给调用者
    stats = {
        'total': len(all_news),
        'chinese': len(cn_news),
        'foreign': len(en_news),
        'bullish': sum(1 for n in all_news if n.get('sentiment') == '利好'),
        'bearish': sum(1 for n in all_news if n.get('sentiment') == '利空'),
        'neutral': sum(1 for n in all_news if n.get('sentiment') == '中性'),
        'report_file': str(report_file),
        'timestamp': datetime.now().isoformat()
    }
    print(f"\n📊 JSON统计: {json.dumps(stats, ensure_ascii=False)}")


if __name__ == '__main__':
    main()
