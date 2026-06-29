import urllib.request
import json
import os
import sys
import time

BASE_URL = "https://api.firecrawl.dev"

def get_headers():
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers

def api_post(path, body, timeout=60):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=get_headers(), method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.read().decode()}"}
    except urllib.error.URLError:
        return {"success": False, "error": "Network error: unable to reach Firecrawl API. Check your internet connection."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def api_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers=get_headers(), method="GET")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"success": False, "error": f"HTTP {e.code}: {body}"}
    except urllib.error.URLError:
        return {"success": False, "error": "Network error: unable to reach Firecrawl API. Check your internet connection."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def cmd_scrape(args):
    url = args[0] if args else ""
    if not url or not url.startswith(("http://", "https://")):
        return {"success": False, "error": "请输入正确的网址，以 http:// 或 https:// 开头"}
    formats = ["markdown"]
    result = api_post("/v2/scrape", {"url": url, "formats": formats})
    if result.get("success"):
        data = result.get("data", {})
        return {
            "success": True,
            "url": url,
            "title": data.get("metadata", {}).get("title", ""),
            "description": data.get("metadata", {}).get("description", ""),
            "markdown": data.get("markdown", ""),
            "content_length": len(data.get("markdown", "")),
        }
    err = result.get("error", "unknown error")
    if "402" in str(err):
        return {"success": False, "error": "免费额度已用完。可以配置 API Key 继续使用（见 skill 说明），或等额度刷新。"}
    if "rate limit" in str(err).lower():
        return {"success": False, "error": "请求太快了，请稍后再试。"}
    return result

def cmd_search(args):
    query = args[0] if args else ""
    limit = int(args[1]) if len(args) > 1 else 5
    if not query:
        return {"success": False, "error": "请输入搜索关键词"}
    result = api_post("/v2/search", {"query": query, "limit": limit})
    if result.get("success"):
        results = result.get("data", {}).get("web", [])
        return {
            "success": True,
            "query": query,
            "total": len(results),
            "results": [{
                "title": r.get("title"),
                "url": r.get("url"),
                "description": r.get("description"),
            } for r in results],
        }
    return result

def cmd_map(args):
    url = args[0] if args else ""
    if not url or not url.startswith(("http://", "https://")):
        return {"success": False, "error": "请输入正确的网址，以 http:// 或 https:// 开头"}
    result = api_post("/v1/map", {"url": url})
    if result.get("success"):
        links = result.get("links", [])
        return {
            "success": True,
            "url": url,
            "total": len(links),
            "links": links[:500],
        }
    return result

def cmd_crawl(args):
    url = args[0] if args else ""
    max_pages = int(args[1]) if len(args) > 1 else 50
    if not url or not url.startswith(("http://", "https://")):
        return {"success": False, "error": "请输入正确的网址，以 http:// 或 https:// 开头"}
    result = api_post("/v1/crawl", {"url": url, "maxPages": max_pages, "scrapeOptions": {"formats": ["markdown"]}})
    if result.get("success"):
        job_id = result.get("id", "")
        returned_data = result.get("data", [])
        if returned_data:
            pages = []
            for item in returned_data:
                meta = item.get("metadata", {})
                pages.append({
                    "url": item.get("url") or meta.get("sourceURL", ""),
                    "title": meta.get("title", ""),
                    "markdown_preview": (item.get("markdown") or "")[:500],
                })
            return {
                "success": True,
                "job_id": job_id,
                "pages_collected": len(pages),
                "pages": pages,
                "crawl_complete": True,
            }
        else:
            return {
                "success": True,
                "job_id": job_id,
                "pages_collected": 0,
                "pages": [],
                "crawl_complete": False,
                "note": f"爬取任务正在后台进行。用 crawl-status {job_id} 查看进度，稍后就有结果了。",
            }
    return result

def cmd_crawl_status(args):
    job_id = args[0] if args else ""
    if not job_id:
        return {"success": False, "error": "请输入任务 ID"}
    result = api_get(f"/v1/crawl/{job_id}")
    if result.get("success"):
        data = result.get("data", [])
        pages = []
        for item in (data or []):
            meta = item.get("metadata", {})
            pages.append({
                "url": item.get("url") or meta.get("sourceURL", ""),
                "title": meta.get("title", ""),
                "markdown_preview": (item.get("markdown") or "")[:500],
            })
        return {
            "success": True,
            "job_id": job_id,
            "status": result.get("status", "completed"),
            "total_pages": len(pages),
            "pages": pages,
        }
    return result

def cmd_interact(args):
    url = args[0] if args else ""
    prompt = args[1] if len(args) > 1 else ""
    if not url or not url.startswith(("http://", "https://")):
        return {"success": False, "error": "请输入正确的网址"}
    if not prompt:
        return {"success": False, "error": "请输入操作说明，例如：search for mechanical keyboard"}
    scrape_result = api_post("/v2/scrape", {"url": url, "formats": ["markdown"]})
    if not scrape_result.get("success"):
        return scrape_result
    scrape_id = scrape_result.get("data", {}).get("metadata", {}).get("scrapeId", "")
    if not scrape_id:
        return {"success": False, "error": "无法获取页面交互 ID，该页面可能不支持交互操作。"}
    body = {"prompt": prompt}
    interact_result = api_post(f"/v2/scrape/{scrape_id}/interact", body, timeout=120)
    if interact_result.get("success"):
        return {
            "success": True,
            "url": url,
            "prompt": prompt,
            "output": interact_result.get("output", ""),
            "live_view_url": interact_result.get("interactiveLiveViewUrl", ""),
        }
    return interact_result

def cmd_extract(args):
    url = args[0] if args else ""
    prompt = args[1] if len(args) > 1 else ""
    if not url or not url.startswith(("http://", "https://")):
        return {"success": False, "error": "请输入正确的网址"}
    if not prompt:
        return {"success": False, "error": "请输入提取说明，例如：帮我找出所有产品的名称和价格"}
    body = {"url": url, "prompt": prompt}
    result = api_post("/v1/extract", body, timeout=120)
    if result.get("success"):
        return {
            "success": True,
            "url": url,
            "prompt": prompt,
            "data": result.get("data", {}),
            "llm_extraction": result.get("llm_extraction", ""),
        }
    return result

def print_help():
    print("Firecrawl Wrapper — Web data for everyone")
    print(f"API Key: {'✅ Set' if os.environ.get('FIRECRAWL_API_KEY') else '❌ Not set (free tier)'}")
    print()
    print("Commands:")
    print("  scrape <url>                 抓取页面内容")
    print("  search <query> [n]           搜索网络")
    print("  map <url>                    发现网站上的所有链接")
    print("  crawl <url> [pages]          爬取整个网站")
    print("  crawl-status <job_id>        查看爬取进度")
    print("  interact <url> <prompt>      在页面上执行操作（点/搜/填表）")
    print("  extract <url> <prompt>       用 AI 提取页面中的结构化数据")
    print()
    print("Examples:")
    print("  python3 scripts/firecrawl_wrapper.py scrape https://example.com")
    print("  python3 scripts/firecrawl_wrapper.py search 最新AI新闻 3")
    print("  python3 scripts/firecrawl_wrapper.py map https://example.com")
    print("  python3 scripts/firecrawl_wrapper.py interact https://amazon.com 'search for keyboard'")
    print("  python3 scripts/firecrawl_wrapper.py extract https://shop.com '列出所有商品名称和价格'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    cmds = {
        "scrape": cmd_scrape,
        "search": cmd_search,
        "map": cmd_map,
        "crawl": cmd_crawl,
        "crawl-status": cmd_crawl_status,
        "interact": cmd_interact,
        "extract": cmd_extract,
    }
    handler = cmds.get(cmd)
    if not handler:
        print(json.dumps({"success": False, "error": f"未知命令: {cmd}"}, ensure_ascii=False))
        sys.exit(1)
    result = handler(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("success"):
        sys.exit(1)
