import asyncio
import json
from datetime import datetime
import httpx


def clean_title(title: str) -> str:
    return title.replace("<em class=\"keyword\">", "").replace("</em>", "")


async def search_videos(keyword: str, page: int = 1, page_size: int = 20):
    url = "https://api.bilibili.com/x/web-interface/search/type"
    params = {
        "search_type": "video",
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params, headers=headers)
        data = res.json()
    result = data.get("data", {})
    return result.get("result", [])


def save_results(keyword: str, results: list):
    data = {
        "keyword": keyword,
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "videos": [
            {
                "bvid": v.get("bvid", ""),
                "title": clean_title(v.get("title", "")),
                "author": v.get("author", ""),
                "play": v.get("play", 0),
                "duration": v.get("duration", ""),
                "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
            }
            for v in results
        ],
    }
    with open("search.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到 search.json ({len(results)} 条)")


async def main():
    keyword = "红楼梦 陶喆"
    results = await search_videos(keyword)
    if not results:
        print("未找到相关视频")
        return
    save_results(keyword, results)
    print(f"\n共找到 {len(results)} 个视频:\n")
    for i, v in enumerate(results, 1):
        title = clean_title(v.get("title", ""))
        author = v.get("author", "未知")
        play = v.get("play", 0)
        duration = v.get("duration", "未知")
        bvid = v.get("bvid", "")
        print(f"{i:2d}. [{title}]")
        print(f"    UP主: {author} | 播放: {play} | 时长: {duration}s")
        print(f"    BV号: {bvid}")
        print(f"    链接: https://www.bilibili.com/video/{bvid}\n")


if __name__ == "__main__":
    asyncio.run(main())
