import requests

# 根据常见基金代码直接查询
funds_to_check = [
    ("000171", "华泰柏瑞沪深 300ETF 联接 A"),
    ("270042", "广发纳斯达克 100ETF 联接 A"),
    ("110020", "易方达沪深 300ETF 联接 A"),
    ("008887", "华夏国证半导体芯片 ETF 联接 C"),
    ("000051", "华夏沪深 300ETF 联接 A"),
]

for code, name in funds_to_check:
    try:
        url = f"https://fund.eastmoney.com/{code}.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            # 检查页面是否包含基金名称
            if name[:4] in r.text:
                print(f"FOUND: {code} - {name}")
    except Exception as e:
        print(f"Error {code}: {e}")
