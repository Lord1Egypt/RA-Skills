"""
AIBuy 水贝产品查询
用法: python search.py <关键词> [limit] [offset]
"""
import sys
import io
import json
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

API = "https://wjxggrbemnbuhpmbyyws.supabase.co/functions/v1/query-jewelry"

def search(keyword: str, limit: int = 5, offset: int = 0) -> dict:
    params = urllib.parse.urlencode({"q": keyword, "limit": limit, "offset": offset})
    req = urllib.request.Request(f"{API}?{params}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python search.py <关键词> [limit] [offset]"}))
        sys.exit(1)

    keyword = sys.argv[1]
    limit   = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    offset  = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    result  = search(keyword, limit, offset)
    print(json.dumps(result, ensure_ascii=False, indent=2))
