#!/usr/bin/env python3
"""
Bilibili Skill - B站数据查询工具
支持：搜索视频、视频详情、UP主信息、热门排行榜、热搜榜
无需 API Key，完全基于 B站公开接口
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept": "application/json",
    # 搜索接口需要 Cookie 避免 412，使用最小化 Cookie
    "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000",
}


def http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_videos(query: str, page: int = 1, page_size: int = 10, order: str = "totalrank") -> dict:
    """
    搜索B站视频
    order: totalrank(综合), click(播放量), pubdate(最新), dm(弹幕), stow(收藏)
    """
    params = urllib.parse.urlencode({
        "keyword": query,
        "page": page,
        "pagesize": page_size,
        "search_type": "video",
        "order": order,
    })
    url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
    data = http_get(url)
    if data.get("code") != 0:
        return {"error": data.get("message", "搜索失败")}

    results = []
    for item in data.get("data", {}).get("result", []):
        bvid = item.get("bvid", "")
        results.append({
            "bvid": bvid,
            "url": f"https://www.bilibili.com/video/{bvid}",
            "title": item.get("title", "").replace('<em class="keyword">', "").replace("</em>", ""),
            "author": item.get("author"),
            "mid": item.get("mid"),
            "play": item.get("play"),
            "danmaku": item.get("video_review"),
            "favorites": item.get("favorites"),
            "like": item.get("like"),
            "pubdate": item.get("pubdate"),
            "duration": item.get("duration"),
            "desc": item.get("description", "")[:100],
        })
    return {
        "total": data.get("data", {}).get("numResults", 0),
        "page": page,
        "results": results
    }


def get_video_detail(bvid: str) -> dict:
    """获取视频详细信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    data = http_get(url)
    if data.get("code") != 0:
        return {"error": data.get("message", "获取失败")}

    v = data.get("data", {})
    stat = v.get("stat", {})
    owner = v.get("owner", {})
    return {
        "bvid": v.get("bvid"),
        "title": v.get("title"),
        "desc": v.get("desc"),
        "owner": {
            "name": owner.get("name"),
            "mid": owner.get("mid"),
        },
        "pubdate": v.get("pubdate"),
        "duration": v.get("duration"),
        "tags": [t.get("tag_name") for t in v.get("tags", [])],
        "stat": {
            "view": stat.get("view"),
            "danmaku": stat.get("danmaku"),
            "reply": stat.get("reply"),
            "favorite": stat.get("favorite"),
            "coin": stat.get("coin"),
            "share": stat.get("share"),
            "like": stat.get("like"),
        },
        "url": f"https://www.bilibili.com/video/{v.get('bvid')}",
    }


def get_user_info(mid: int) -> dict:
    """获取UP主基本信息（无需登录）"""
    # 粉丝/关注数（PC端无需登录）
    stat_url = f"https://api.bilibili.com/x/relation/stat?vmid={mid}"
    stat_data = http_get(stat_url)
    follower = None
    following = None
    if stat_data.get("code") == 0:
        follower = stat_data.get("data", {}).get("follower")
        following = stat_data.get("data", {}).get("following")

    # 投稿列表获取UP主名称和投稿数（移动端UA可绕过风控）
    mobile_headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": f"https://m.bilibili.com/space/{mid}",
        "Cookie": "buvid3=openclaw_bilibili_skill_v1",
    }
    arc_req = urllib.request.Request(
        f"https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=1&pn=1",
        headers=mobile_headers
    )
    name = None
    videos = None
    try:
        with urllib.request.urlopen(arc_req, timeout=10) as resp:
            arc_data = json.loads(resp.read().decode("utf-8"))
        if arc_data.get("code") == 0:
            vlist = arc_data.get("data", {}).get("list", {}).get("vlist", [])
            if vlist:
                name = vlist[0].get("author")
            videos = arc_data.get("data", {}).get("page", {}).get("count")
    except Exception:
        pass

    return {
        "mid": mid,
        "name": name,
        "followers": follower,
        "following": following,
        "videos": videos,
        "url": f"https://space.bilibili.com/{mid}",
    }


def get_popular(page_size: int = 10) -> dict:
    """获取热门视频"""
    url = f"https://api.bilibili.com/x/web-interface/popular?ps={page_size}&pn=1"
    data = http_get(url)
    if data.get("code") != 0:
        return {"error": data.get("message", "获取失败")}

    results = []
    for v in data.get("data", {}).get("list", []):
        stat = v.get("stat", {})
        bvid = v.get("bvid", "")
        results.append({
            "bvid": bvid,
            "url": f"https://www.bilibili.com/video/{bvid}",
            "title": v.get("title"),
            "owner": v.get("owner", {}).get("name"),
            "view": stat.get("view"),
            "like": stat.get("like"),
            "danmaku": stat.get("danmaku"),
        })
    return {"results": results}


def get_hot_search() -> dict:
    """获取热搜榜"""
    url = "https://s.search.bilibili.com/main/hotword"
    data = http_get(url)
    if data.get("code") != 0:
        return {"error": data.get("message", "获取失败")}

    results = []
    for item in data.get("list", [])[:20]:
        keyword = item.get("keyword", "")
        results.append({
            "rank": item.get("pos"),
            "keyword": keyword,
            "search_url": f"https://search.bilibili.com/all?keyword={urllib.parse.quote(keyword)}",
            "hot_id": item.get("hot_id"),
        })
    return {"hot_search": results}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: bilibili.py '<JSON>'", "actions": [
            "search: {action:'search', query:'关键词', page:1, order:'totalrank'}",
            "video: {action:'video', bvid:'BV1xx411c7mD'}",
            "user: {action:'user', mid:123456}",
            "popular: {action:'popular', count:10}",
            "hot_search: {action:'hot_search'}",
        ]}, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON解析错误: {e}"}, ensure_ascii=False))
        sys.exit(1)

    action = params.get("action", "search")

    try:
        if action == "search":
            result = search_videos(
                query=params.get("query", ""),
                page=int(params.get("page", 1)),
                page_size=int(params.get("count", 10)),
                order=params.get("order", "totalrank"),
            )
        elif action == "video":
            bvid = params.get("bvid", "")
            if not bvid:
                result = {"error": "缺少 bvid 参数"}
            else:
                result = get_video_detail(bvid)
        elif action == "user":
            mid = params.get("mid")
            if not mid:
                result = {"error": "缺少 mid 参数"}
            else:
                result = get_user_info(int(mid))
        elif action == "popular":
            result = get_popular(int(params.get("count", 10)))
        elif action == "hot_search":
            result = get_hot_search()
        else:
            result = {"error": f"未知 action: {action}，支持: search, video, user, popular, hot_search"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except urllib.error.URLError as e:
        print(json.dumps({"error": f"网络请求失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
