#!/usr/bin/env python3
"""
AniCult CLI - Search, discover, and get streaming links for anime.
Uses AniList GraphQL API + Anikoto API + streaming embeds.
Compatible with Telegram formatting (no ANSI codes in --json mode).
"""
import argparse, json, sys, time, urllib.request, urllib.parse, random

ANILIST_URL = "https://graphql.anilist.co"
ANIKOTO_BASE = "https://anikotoapi.site"
MEGAPLAY_BASE = "https://megaplay.buzz"

# All on ONE line - GraphQL doesn't accept newlines in field selections
MEDIA_FIELDS = "id title{romaji english native} coverImage{extraLarge large} bannerImage description genres averageScore popularity format status episodes duration season seasonYear studios{nodes{name isAnimationStudio}} nextAiringEpisode{episode airingAt} relations{edges{relationType node{id title{romaji english} coverImage{large} type}}} streamingEpisodes{site title thumbnail url}"
MEDIA_FIELDS_SMALL = "id title{romaji english} coverImage{extraLarge large} bannerImage description genres averageScore popularity format status episodes season seasonYear"

def gql(query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(ANILIST_URL, data=data, headers={"User-Agent": "AniCult-CLI/1.0", "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.load(r)
    if res.get("errors"):
        raise Exception(res["errors"][0]["message"])
    return res["data"]

def gql_search(query_str, page=1, per_page=10, sort="SEARCH_MATCH"):
    q = "query($page:Int,$perPage:Int,$search:String,$sort:[MediaSort]){Page(page:$page,perPage:$perPage){pageInfo{total currentPage lastPage hasNextPage}media(type:ANIME,search:$search,sort:$sort){" + MEDIA_FIELDS_SMALL + "}}}"
    return gql(q, {"page": page, "perPage": per_page, "search": query_str, "sort": [sort]})

def gql_trending(page=1, per_page=10):
    q = "query($page:Int,$perPage:Int){Page(page:$page,perPage:$perPage){pageInfo{total currentPage lastPage hasNextPage}media(type:ANIME,sort:TRENDING_DESC){" + MEDIA_FIELDS_SMALL + "}}}"
    return gql(q, {"page": page, "perPage": per_page})

def gql_popular(page=1, per_page=10):
    q = "query($page:Int,$perPage:Int){Page(page:$page,perPage:$perPage){pageInfo{total currentPage lastPage hasNextPage}media(type:ANIME,sort:POPULARITY_DESC){" + MEDIA_FIELDS_SMALL + "}}}"
    return gql(q, {"page": page, "perPage": per_page})

def gql_detail(anilist_id):
    q = "query($id:Int){Media(id:$id,type:ANIME){" + MEDIA_FIELDS + "}}"
    return gql(q, {"id": int(anilist_id)})["Media"]

def anikoto_recent(page=1, per_page=10):
    url = f"{ANIKOTO_BASE}/recent-anime?page={page}&per_page={per_page}"
    req = urllib.request.Request(url, headers={"User-Agent": "AniCult-CLI/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def anikoto_series(series_id):
    url = f"{ANIKOTO_BASE}/series/{series_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "AniCult-CLI/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def safe(s, max_len=200):
    if not s: return ""
    s = s.replace("**","").replace("__","").replace("*","").replace("_","").replace("<br>"," ").replace("<b>","").replace("</b>","")
    s = s.strip()
    if len(s) > max_len: s = s[:max_len] + "..."
    return s

def fmt_score(s):
    if not s: return "N/A"
    return f"⭐ {s}/100"

def fmt_list(data, page=1, per_page=10):
    items = data["Page"]["media"]
    info = data["Page"]["pageInfo"]
    lines = []
    for i, a in enumerate(items):
        title = a["title"]
        title_str = title.get("romaji") or title.get("english") or title.get("native") or "Unknown"
        score = fmt_score(a.get("averageScore"))
        eps = a.get("episodes") or "?"
        fmt = a.get("format") or "?"
        status = a.get("status") or "?"
        genres = ", ".join(a.get("genres", [])[:3])
        lines.append(f"{((page-1)*per_page)+i+1}. *{title_str}*")
        lines.append(f"   {score} | {eps} eps | {fmt} | {status}")
        if genres: lines.append(f"   Genre: {genres}")
    lines.append(f"\n📄 Page {info['currentPage']}/{info['lastPage']} | Total: {info['total']}")
    if info.get("hasNextPage"):
        lines.append(f"→ Next page: `anime.py trending --page {page+1}`")
    return "\n".join(lines)

def fmt_recent(data):
    lines = []
    for i, a in enumerate(data["data"][:10], 1):
        title = a.get("title", "Unknown")
        is_sub = a.get("is_sub", 0)
        eps = a.get("episodes", "?")
        status = a.get("status", "?")
        rating = a.get("rating", "?")
        slug = a.get("slug", "")
        ani_id = a.get("ani_id", "")
        ep_embed_id = a.get("episode_embed_id", "")
        lines.append(f"{i}. *{title}*")
        lines.append(f"   Sub: {is_sub} | Eps: {eps} | {status} | {rating}")
        if slug:
            lines.append(f"   🎬 https://anicult.vercel.app/anime/{a['id']}")
        # megaplay streaming link
        if ani_id and ep_embed_id:
            lines.append(f"   ▶️ https://megaplay.buzz/stream/s-2/{ep_embed_id}/sub")
        elif ani_id:
            lines.append(f"   ▶️ https://megaplay.buzz/stream/ani/{ani_id}/1/sub")
    return "\n".join(lines)

def fmt_detail(media, anikoto_data=None):
    title = media["title"]
    main_title = title.get("romaji") or title.get("english") or title.get("native") or "Unknown"
    eng_title = title.get("english", "")

    lines = [
        f"*{main_title}*",
        f"_{eng_title}_" if eng_title and eng_title != main_title else "",
        "",
        f"📊 Score: {fmt_score(media.get('averageScore'))} | Popularity: {media.get('popularity', 'N/A')}",
        f"📺 Format: {media.get('format','?')} | Status: {media.get('status','?')}",
        f"🗓️ Season: {media.get('season', '?')} {media.get('seasonYear', '')} | Episodes: {media.get('episodes') or '?'}",
    ]
    dur = media.get("duration")
    if dur: lines.append(f"⏱️ Duration: {dur} min/episode")
    studios = media.get("studios", {}).get("nodes", [])
    if studios:
        main_studio = next((s["name"] for s in studios if s.get("isAnimationStudio")), studios[0]["name"])
        lines.append(f"🏢 Studio: {main_studio}")

    genres = media.get("genres", [])
    if genres: lines.append(f"🏷️ Genre: {', '.join(genres[:5])}")

    desc = safe(media.get("description", ""), 400)
    if desc: lines.extend(["", f"📝 {desc}"])

    next_ep = media.get("nextAiringEpisode")
    if next_ep:
        at = next_ep.get("airingAt", 0)
        if at:
            from datetime import datetime
            dt = datetime.fromtimestamp(at)
            lines.append(f"\n▶️ Episode {next_ep['episode']} airing: {dt.strftime('%b %d, %H:%M')} JST")

    if anikoto_data and anikoto_data.get("ok"):
        ep_data = anikoto_data["data"]
        anime_info = ep_data.get("anime", {})
        episodes = ep_data.get("episodes", [])
        if episodes:
            total_eps = anime_info.get("episodes", "?")
            lines.append(f"\n🎬 Episodes ({len(episodes)}/{total_eps} available on Anikoto):")
            for ep in episodes[:8]:
                ep_num = ep.get("number", "?")
                ep_title = ep.get("title", f"Episode {ep_num}")
                ep_embed_id = ep.get("episode_embed_id", "")
                stream_url = f"{MEGAPLAY_BASE}/stream/s-2/{ep_embed_id}/sub" if ep_embed_id else ""
                lines.append(f"   Ep {ep_num}: {ep_title}")
                if stream_url: lines.append(f"   → [Watch]({stream_url})")
    elif anikoto_data and not anikoto_data.get("ok"):
        lines.append(f"\n⚠️ Streaming data unavailable: {anikoto_data.get('msg', 'unknown error')}")

    # Streaming links via megaplay.buzz (AniList ID + episode)
    stream_eps = media.get("streamingEpisodes", [])
    if stream_eps:
        lines.append("\n🌐 Streaming (legal):")
        seen = set()
        for se in stream_eps:
            site = se.get('site', '?')
            if site not in seen:
                seen.add(site)
                lines.append(f"   {site}: {se.get('url','#')}")

    # megaplay.buzz direct streaming links (works as Telegram inline links)
    anilist_id = media.get("id")
    if anilist_id:
        lines.append("\n▶️ Stream di Telegram:")
        lines.append(f"   Episode 1: https://megaplay.buzz/stream/ani/{anilist_id}/1/sub")
        lines.append(f"   Episode 2: https://megaplay.buzz/stream/ani/{anilist_id}/2/sub")
        lines.append(f"   Episode 3: https://megaplay.buzz/stream/ani/{anilist_id}/3/sub")
        if media.get("episodes"):
            total = media["episodes"]
            if total > 3:
                lines.append(f"   ... Episode {total}: https://megaplay.buzz/stream/ani/{anilist_id}/{total}/sub")
        lines.append("\n💡 Tap link di atas → buka browser → streaming tanpa perlu VPN!")

    relations = media.get("relations", {}).get("edges", [])
    if relations:
        related = [(e["relationType"], e["node"]) for e in relations if e.get("node")]
        if related:
            lines.append("\n🔗 Related Anime:")
            for rel_type, node in related[:5]:
                node_title = node.get("title", {}).get("romaji") or "?"
                lines.append(f"   [{rel_type}] [{node_title}](https://anilist.co/anime/{node['id']})")

    return "\n".join(l for l in lines if l)

def cmd_search(args):
    sort_map = {"trending": "TRENDING_DESC", "popular": "POPULARITY_DESC", "score": "SCORE_DESC", "search": "SEARCH_MATCH"}
    sort = sort_map.get(args.sort, "SEARCH_MATCH")
    data = gql_search(args.query, page=args.page, per_page=args.limit, sort=sort)
    result = fmt_list(data, page=args.page, per_page=args.limit)
    if args.json:
        items = [{"id": a["id"], "title": a["title"].get("romaji") or a["title"].get("english"), "score": a.get("averageScore"), "episodes": a.get("episodes"), "format": a.get("format")} for a in data["Page"]["media"]]
        print(json.dumps(items, indent=2))
    else:
        labels = {"trending": "🔥 Trending", "popular": "📈 Popular", "score": "⭐ Top Rated", "search": "🔍 Search Results"}
        print(f"*{labels.get(args.sort, '🔍')}: \"{args.query}\"*\n\n{result}")

def cmd_trending(args):
    data = gql_trending(page=args.page, per_page=args.limit)
    result = fmt_list(data, page=args.page, per_page=args.limit)
    if args.json:
        items = [{"id": a["id"], "title": a["title"].get("romaji") or a["title"].get("english"), "score": a.get("averageScore"), "episodes": a.get("episodes"), "format": a.get("format")} for a in data["Page"]["media"]]
        print(json.dumps(items, indent=2))
    else:
        print(f"*🔥 Trending Anime*\n\n{result}")

def cmd_popular(args):
    data = gql_popular(page=args.page, per_page=args.limit)
    result = fmt_list(data, page=args.page, per_page=args.limit)
    if args.json:
        items = [{"id": a["id"], "title": a["title"].get("romaji") or a["title"].get("english"), "score": a.get("averageScore"), "episodes": a.get("episodes"), "format": a.get("format")} for a in data["Page"]["media"]]
        print(json.dumps(items, indent=2))
    else:
        print(f"*📈 Popular Anime*\n\n{result}")

def cmd_detail(args):
    try:
        media = gql_detail(args.id)
    except Exception as e:
        print(f"❌ Error fetching anime {args.id}: {e}")
        return
    anikoto_data = None
    if args.episodes:
        try:
            anilist_id = media.get("id")
            recent = anikoto_recent(page=1, per_page=100)
            for item in recent.get("data", []):
                if str(item.get("ani_id")) == str(anilist_id):
                    anikoto_data = anikoto_series(item["id"])
                    break
        except Exception as e:
            anikoto_data = {"ok": False, "msg": str(e)}
    result = fmt_detail(media, anikoto_data)
    print(result)
    if not args.json and not args.no_url:
        print(f"\n🔗 https://anilist.co/anime/{args.id}")
        print(f"🎬 https://anicult.vercel.app/anime/{args.id}")

def cmd_recent(args):
    data = anikoto_recent(page=args.page, per_page=args.limit)
    if args.json:
        items = [{"id": a["id"], "title": a.get("title"), "is_sub": a.get("is_sub"), "episodes": a.get("episodes"), "status": a.get("status")} for a in data.get("data", [])]
        print(json.dumps(items, indent=2))
    else:
        ts = data.get("data", [{}])[0].get("updated_at", "") if data.get("data") else ""
        print(f"*🆕 Recently Updated* _{ts}_\n\n{fmt_recent(data)}")
        print("\n📺 Stream: megaplay.buzz | anixo.buzz")

def cmd_random(args):
    q = "query($page:Int,$perPage:Int){Page(page:$page,perPage:$perPage){media(type:ANIME,sort:TRENDING_DESC,isAdult:false){id title{romaji english} coverImage{extraLarge large} averageScore format genres}}}"
    data = gql(q, {"page": random.randint(1,5), "perPage": 50})
    items = data["Page"]["media"]
    if args.genre:
        items = [a for a in items if any(args.genre.lower() in g.lower() for g in a.get("genres", []))]
    if not items:
        print("❌ No anime found matching criteria")
        return
    pick = random.choice(items)
    title = pick["title"].get("romaji") or pick["title"].get("english") or "?"
    cover = pick.get("coverImage",{}).get("extraLarge","")
    print(f"*🎲 Random Pick: {title}*")
    print(f"   ⭐ {pick.get('averageScore')}/100 | {pick.get('format')} | Genres: {', '.join(pick.get('genres',[])[:3])}")
    print(f"   🔗 https://anilist.co/anime/{pick['id']}")
    if cover: print(f"   🖼️ {cover}")

def main():
    parser = argparse.ArgumentParser(description="AniCult CLI - Anime search & discovery")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("search", help="Search anime by name")
    p.add_argument("query", nargs="+", help="Anime name to search")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--sort", default="search", choices=["search","trending","popular","score"])
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("trending", help="Get trending anime")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("popular", help="Get popular anime")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("detail", help="Get anime details + episodes")
    p.add_argument("id", type=int, help="AniList anime ID")
    p.add_argument("--episodes", action="store_true", help="Fetch episodes from Anikoto")
    p.add_argument("--no-url", action="store_true")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("recent", help="Recently updated anime (Anikoto)")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("random", help="Random anime pick")
    p.add_argument("--genre", help="Filter by genre (e.g. Action, Romance)")

    args = parser.parse_args()
    if args.cmd == "search":
        args.query = " ".join(args.query)
        cmd_search(args)
    elif args.cmd == "trending": cmd_trending(args)
    elif args.cmd == "popular": cmd_popular(args)
    elif args.cmd == "detail": cmd_detail(args)
    elif args.cmd == "recent": cmd_recent(args)
    elif args.cmd == "random": cmd_random(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
