# 📚 模块 3：教育工具

---

#### 3.1 知识查询

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, urllib.parse, json, socket, re

def _wiki_fallback(query: str) -> list[dict]:
    url = f"https://baike.deno.dev/item/{urllib.parse.quote(query)}?encode=json"
    req = urllib.request.Request(url, headers={"User-Agent":"dgngjx/3.5"})
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    results = []
    if isinstance(data, list):
        for item in data:
            title = item.get("title", "")
            abstract = item.get("abstract", "").replace("\n", " ").strip()
            if title: results.append({"title": title, "snippet": abstract[:200]})
    elif isinstance(data, dict):
        title = data.get("title", query)
        abstract = data.get("abstract", data.get("description", ""))
        results = [{"title": title, "snippet": str(abstract)[:200]}]
    return results

try:
    q = input("关键词:") or "勾股定理"
    if not q.strip():
        print("❌ 关键词不能为空")
    else:
        results = []
        try:
            url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&format=json&srlimit=3"
            req = urllib.request.Request(url, headers={"User-Agent":"dgngjx/3.5"})
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            results = data.get("query",{}).get("search",[])
        except Exception as e:
            print(f"⚠️ Wikipedia 失败（{type(e).__name__}），切换到百度百科...")
        if not results:
            try: results = _wiki_fallback(q)
            except Exception as e2: print(f"⚠️ 百度百科也失败: {e2}")
        if not results:
            print(f"❌ 没有找到关于「{q}」的内容")
            print(f"   百度搜索: https://www.baidu.com/s?wd={urllib.parse.quote(q)}")
        else:
            for r in results:
                t = r.get('title','')
                s = re.sub(r'<[^>]+>', '', r.get('snippet',''))[:200]
                print(f"\n📖 {t}\n   {s}...")
except Exception as e:
    print(f"❌ 意外错误: {e}")
```

</details>
