import requests

# 让我检查更详细的原始数据
url = 'https://qt.gtimg.cn/q=hk01826'
r = requests.get(url, timeout=10)
raw = r.text

print("原始数据:")
print(raw)
print()

# 解析
import re
match = re.search(r'"([^"]+)"', raw)
if match:
    parts = match.group(1).split('~')
    print("解析后的字段:")
    for i, p in enumerate(parts):
        print(f"  [{i}]: {p}")
