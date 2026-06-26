import requests

# 腾讯港股代码规则: 
# 港股代码转换为6位: 代码前加0，然后根据上市板块加不同前缀
# 京东物流 02618 -> 000618 (创业板?) 或者直接用完整代码

# 尝试多种格式
test_codes = [
    ('hk000618', '京东物流'),  # 原始6位
    ('hk001826', '京东物流-2'), # 另一种
    ('hk01826', '京东物流-3'),
    ('hk2618', '京东物流-4'),
    ('hk000618', '京东物流-5'),
]

for code, name in test_codes:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' not in text:
            print(f"{name} ({code}): {text[:150]}")
        else:
            print(f"{name} ({code}): 无匹配")
    except Exception as e:
        print(f"{name}: {e}")
