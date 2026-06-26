import sys
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def get_stock_news(stock_code, count=5):
    """获取股票最新消息"""
    # 直接使用东方财富
    return get_stock_news_from_eastmoney(stock_code, count)

def get_stock_news_from_eastmoney(stock_code, count=5):
    """从东方财富获取股票新闻"""
    # 同花顺财经接口
    url = f"https://news.10jqka.com.cn/api/stock/news?code={stock_code}&limit={count}"
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': f'https://news.10jqka.com.cn/stock/{stock_code}/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get('data', {}).get('list', [])[:count]:
            news = {
                'title': item.get('title', ''),
                'time': item.get('public_time', ''),
                'url': item.get('url', ''),
                'source': item.get('source', '')
            }
            news_list.append(news)
        return news_list
    except Exception as e:
        print(f"同花顺获取{stock_code}新闻失败: {e}")
        
        # 备用：百度股市通
        try:
            url = f"https://gupiao.baidu.com/stock/{stock_code}.html"
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': 'https://gupiao.baidu.com/'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            news_list = []
            items = soup.select('.news-list .item')[:count]
            for item in items:
                title = item.select_one('.title').get_text(strip=True) if item.select_one('.title') else ''
                time = item.select_one('.time').get_text(strip=True) if item.select_one('.time') else ''
                url = item.select_one('a')['href'] if item.select_one('a') else ''
                
                news_list.append({
                    'title': title,
                    'time': time,
                    'url': url,
                    'source': '百度股市通'
                })
            return news_list
        except Exception as e2:
            print(f"百度股市通获取{stock_code}新闻失败: {e2}")
            return []

def get_stock_name(stock_code):
    """获取股票名称"""
    url = f"https://qt.gtimg.cn/q={stock_code}"
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.text
        if '~' in data:
            parts = data.split('~')
            if len(parts) > 1:
                return parts[1]
    except Exception as e:
        print(f"获取{stock_code}名称失败: {e}")
    
    # 股票名称映射
    stock_map = {
        '601899': '紫金矿业',
        '603259': '药明康德',
        '688012': '中微公司',
        '688333': '铂力特',
        '688676': '金盘科技',
        '000977': '浪潮信息',
        '002273': '水晶光电',
        '002409': '雅克科技',
        '300019': '硅宝科技',
        '300502': '新易盛',
        '300724': '捷佳伟创'
    }
    return stock_map.get(stock_code, stock_code)

def main():
    if len(sys.argv) < 2:
        print("用法: python fetch_news.py 股票代码1,股票代码2,...")
        sys.exit(1)
    
    stock_codes = sys.argv[1].split(',')
    print("📰 自选股最新消息汇总\n")
    
    for code in stock_codes:
        code = code.strip()
        if not code:
            continue
            
        name = get_stock_name(code)
        print(f"{'='*60}")
        print(f"📌 {name}({code})")
        print(f"{'='*60}")
        
        news = get_stock_news(code, count=3)
        if news:
            for i, item in enumerate(news, 1):
                print(f"{i}. 【{item['time']}】{item['title']}")
                if item['source']:
                    print(f"   来源: {item['source']}")
                print()
        else:
            print("   暂无最新消息\n")
        
        time.sleep(random.uniform(1, 3))  # 避免请求过快

if __name__ == "__main__":
    main()
