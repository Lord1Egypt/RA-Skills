import requests

# 尝试腾讯财经API (免费，无需API key)
symbol = '02618'

# 腾讯财经港股接口
urls = [
    # 腾讯港股行情
    f'https://qt.gtimg.cn/q=sh{symbol}',
    f'https://qt.gtimg.cn/q=sz{symbol}',
    # 新浪财经
    f'https://hq.sinajs.cn/list=sh{symbol}',
    f'https://hq.sinajs.cn/list=sz{symbol}',
]

for url in urls:
    try:
        r = requests.get(url, timeout=5)
        print(f"=== {url.split('/')[-1]} ===")
        print(r.text[:300])
        print()
    except Exception as e:
        print(f"{url}: {e}")
