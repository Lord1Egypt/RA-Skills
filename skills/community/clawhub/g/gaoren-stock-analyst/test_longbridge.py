import os
import requests

token = os.environ.get('LONGBRIDGE_ACCESS_TOKEN')
if not token:
    print("NO TOKEN")
    exit()

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 尝试获取京东物流行情
symbols = ['02618.HK', '2618.HK', '01826.HK']

for sym in symbols:
    url = f'https://api.longbridgeapp.com/v1/quote/quotes?symbol={sym}'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"=== {sym} ===")
        print(r.status_code)
        print(r.text[:500])
        print()
    except Exception as e:
        print(f"{sym}: Error - {e}")
