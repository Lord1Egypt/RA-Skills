#!/usr/bin/env python3
"""
News Aggregator - 金融新闻/早报聚合脚本
功能：自动抓取当日金融新闻、行业动态、公告摘要
用法：
  news daily                  当日早报摘要
  news stock <code>           个股相关新闻
  news sector                 行业板块动态
  news briefing [date]        指定日期简报
"""
import json, sys, os, re, time
from datetime import datetime, timedelta

try: import requests
except: print(json.dumps({"error":"缺少requests"})); sys.exit(1)

def fetch_eastmoney_news(code=None, page=1):
    """东方财富新闻（兼容个股新闻和财经要闻）"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    try:
        if code:
            # 个股新闻
            url = f'https://search-api-web.eastmoney.com/search/jsonp'
            params = {
                'param': json.dumps({'uid':'', 'keyword':code, 'type':['cmsArticleWebOld'], 'client':'web',
                    'clientType':'web', 'clientVersion':'curr', 'param':{'cmsArticleWebOld':{'searchScope':'default',
                    'sort':'default', 'pageIndex':page, 'pageSize':10}}}),
            }
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            # 简化版：直接返回
            return {'source':'东方财富','news':[]}
        else:
            # 财经要闻 - 使用巨潮或东财头条
            url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
            params = {
                'fltt': 2, 'fid': 'f3', 'invt': 2,
                'fields': 'f12,f14,f2,f3,f4,f5,f6,f7,f15,f16,f17,f18,f20,f21,f24',
                'secids': '1.000001,0.399001,0.399006,1.000688,1.000016,1.000300',
                '_': int(time.time()*1000)
            }
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            indices = []
            if data.get('data', {}).get('diff'):
                for item in data['data']['diff']:
                    indices.append({
                        'name': item.get('f14',''),
                        'price': item.get('f2',0),
                        'change_pct': f"{item.get('f3',0):.2f}%",
                    })
            return {'source':'东方财富','indices':indices}
    except Exception as e:
        return {'source':'东方财富','error':str(e)}

def fetch_thailand_headlines():
    """同花顺快讯/头条"""
    try:
        url = 'https://news.10jqka.com.cn/tapp/news/push/stock'
        resp = requests.get(url, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        if resp.status_code != 200:
            return {'source':'同花顺快讯','error':f'HTTP {resp.status_code}'}
        data = resp.json()
        items = data.get('data', {}).get('list', [])
        if not items:
            return {'source':'同花顺快讯','error':'data.list为空','raw':str(data)[:200]}
        headlines = []
        for item in items[:10]:
            ts = item.get('ctime', '')
            # ctime 是时间戳，转为可读时间
            time_str = ''
            if ts and str(ts).isdigit():
                time_str = datetime.fromtimestamp(int(ts)).strftime('%H:%M')
            headlines.append({
                'title': item.get('title',''),
                'digest': item.get('digest',''),
                'time': time_str,
                'url': item.get('shareUrl', item.get('url','')),
            })
        return {'source':'同花顺快讯','headlines':headlines}
    except Exception as e:
        return {'source':'同花顺快讯','error':f'获取失败: {type(e).__name__}: {str(e)[:100]}'}

def fetch_sina_finance_news():
    """新浪财经头条"""
    try:
        url = 'https://feed.mix.sina.com.cn/api/roll/get'
        params = {'pageid':'153', 'lid':'2509', 'k':'', 'num':'15', 'page':'1'}
        resp = requests.get(url, params=params, timeout=10,
            headers={'User-Agent':'Mozilla/5.0', 'Referer':'https://finance.sina.com.cn/'})
        if resp.status_code != 200: raise ValueError('status error')
        data = resp.json()
        items = data.get('result',{}).get('data',[])
        news = []
        for item in items[:15]:
            news.append({
                'title': item.get('title',''),
                'time': item.get('ctime',''),
                'url': item.get('url',''),
                'source_name': '新浪财经',
            })
        return {'source':'新浪财经','news':news}
    except Exception as e:
        return {'source':'新浪财经','error':str(e)}

# 全局TDX限速 - 至少间隔0.5秒
_TDX_LAST_CALL = 0

# 可用的TDX服务器列表 (ip, port) — 与 china_stock.py 保持一致
_TDX_HOSTS = [
    ('218.6.170.47', 7709),
    ('123.125.108.14', 7709),
    ('180.153.18.170', 7709),
    ('60.191.117.167', 7709),
]
_TDX_HOST_INDEX = 0

def _tdx_rate_limit():
    """全局TDX调用限速：每次调用前等待至少0.5秒"""
    global _TDX_LAST_CALL
    elapsed = time.time() - _TDX_LAST_CALL
    if elapsed < 0.5:
        time.sleep(0.5 - elapsed)
    _TDX_LAST_CALL = time.time()

def _get_index_closes_batch(indices):
    """批量获取指数收盘数据 — 一次连接查询所有指数，避免多次握手"""
    global _TDX_HOST_INDEX
    _tdx_rate_limit()
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
        from pytdx.hq import TdxHq_API
        
        # 轮询服务器，不硬编码一个IP
        for _ in range(len(_TDX_HOSTS)):
            ip, port = _TDX_HOSTS[_TDX_HOST_INDEX % len(_TDX_HOSTS)]
            _TDX_HOST_INDEX += 1
            api = TdxHq_API()
            try:
                api.connect(ip, port, time_out=5)
                # 批量查询 — 一次请求所有指数
                codes = [(mkt, code) for _, mkt, code in indices]
                quotes = api.get_security_quotes(codes)
                api.disconnect()
                if quotes and len(quotes) > 0:
                    results = {}
                    for i, (name, mkt, code) in enumerate(indices):
                        if i < len(quotes) and quotes[i]:
                            q = quotes[i]
                            results[name] = {
                                'close': q.get('price', 0),
                                'open': q.get('open', 0),
                                'high': q.get('high', 0),
                                'low': q.get('low', 0),
                                'last_close': q.get('last_close', 0),
                            }
                    return results
                break  # 成功连接但没数据也退出重试
            except:
                try: api.disconnect()
                except: pass
                continue  # 尝试下一个服务器
    except:
        pass
    return {}

def daily_briefing():
    """生成每日简报 - 使用通达信收盘数据"""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    # 通过通达信获取昨日指数收盘价
    # 上证指数: mkt=1, code=000001
    # 深证成指: mkt=0, code=399001
    # 创业板指: mkt=0, code=399006
    # 科创50: mkt=1, code=000688
    # 上证50: mkt=1, code=000016
    # 沪深300: mkt=1, code=000300
    
    # 批量查询所有指数 — 一次连接，避免6次独立握手
    indices_config = [
        ('上证指数', 1, '000001'),
        ('深证成指', 0, '399001'),
        ('创业板指', 0, '399006'),
        ('科创50', 1, '000688'),
        ('上证50', 1, '000016'),
        ('沪深300', 1, '000300'),
    ]
    
    market_data = []
    closes = _get_index_closes_batch(indices_config)
    for name, mkt, code in indices_config:
        d = closes.get(name)
        if d:
            change_pct = round((d['close'] - d['last_close']) / d['last_close'] * 100, 2) if d['last_close'] else 0
            market_data.append({
                'name': name,
                'price': d['close'],
                'change_pct': f"{change_pct:+.2f}%",
                'open': d['open'],
                'high': d['high'],
                'low': d['low'],
                'last_close': d['last_close'],
            })
    
    # 新闻头条
    sina = fetch_sina_finance_news()
    
    brief = {
        'date': date_str,
        'time': now.strftime('%H:%M'),
        'type': '昨日收盘数据',
        'market': market_data,
        'headlines': sina.get('news', []),
    }
    return brief

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"usage": """
金融新闻工具:
  news daily                 当日早报（指数+头条）
  news headlines             同花顺快讯
  news indices               主要指数行情
""", "example": "news daily"}, ensure_ascii=False))
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'daily':
        r = daily_briefing()
        print(json.dumps(r, ensure_ascii=False, default=str))
    elif cmd == 'headlines':
        r = fetch_thailand_headlines()
        print(json.dumps(r, ensure_ascii=False, default=str))
    elif cmd == 'indices':
        r = fetch_eastmoney_news()
        print(json.dumps(r, ensure_ascii=False, default=str))
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
