import requests
import re

# 港股在腾讯的代码规则:
# 主板: 0+原代码 (5位变6位)
# 创业板: 8+原代码后5位

# 京东物流 02618 (主板) -> 002618
# 让我搜索尝试

test_codes = [
    ('hk002618', '京东物流(主板)'),
    ('hk02618', '京东物流(直接)'),
    ('hk000618', '京东物流(备用)'),
]

for code, name in test_codes:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' not in text:
            # 提取股票名称
            match = re.search(r'~([^~]+)~', text)
            stock_name = match.group(1) if match else 'unknown'
            print(f"{name} ({code}): {stock_name} -> {text[:100]}")
        else:
            print(f"{name}: 无匹配")
    except Exception as e:
        print(f"{name}: Error")
        
print("\n尝试搜索京东物流...")

# 搜索包含"京东物流"的股票
# 腾讯支持模糊搜索
search_url = 'https://searchapi.eastmoney.com/api/suggest/get'
params = {
    'input': '京东物流',
    'type': 14,
    'count': 5
}

try:
    r = requests.get(search_url, params=params, timeout=10)
    print(r.text[:500])
except Exception as e:
    print(f"搜索失败: {e}")
