import requests

# 腾讯财经港股代码格式: 0 + 股票代码 (5位)
# 京东物流 02618 -> 001826
# 京东集团 09618 -> 009618
# 美团 03690 -> 003690

symbols_hk = {
    '01826': '京东物流',
    '009618': '京东集团',
    '003690': '美团',
    '00700': '腾讯',
    '09988': '阿里巴巴'
}

base_url = 'https://qt.gtimg.cn/q='

for code, name in symbols_hk.items():
    url = base_url + 'hk' + code
    try:
        r = requests.get(url, timeout=8)
        if r.text and 'none_match' not in r.text:
            print(f"=== {name} ({code}) ===")
            print(r.text[:200])
            print()
        else:
            print(f"{name}: 无数据")
    except Exception as e:
        print(f"{name}: Error - {e}")

print("\n尝试其他格式...")

# 另一种格式
for code, name in symbols_hk.items():
    url = base_url + code
    try:
        r = requests.get(url, timeout=8)
        if r.text and 'none_match' not in r.text:
            print(f"=== {name} ({code}) raw===")
            print(r.text[:200])
            print()
    except Exception as e:
        pass
