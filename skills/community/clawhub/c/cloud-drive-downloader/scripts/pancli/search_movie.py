"""网盘通 搜索/爬虫/电影/X 子模块（从 engine.py 拆分，高风险实验区，命令由 engine 懒加载）。"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from pancli.engine import *  # noqa: F401,F403

def _cmd_get(args):
    from pancli.carriers import cmd_get
    return cmd_get(args)


def _cmd_remote_get(args):
    from pancli.remote import cmd_remote_get
    return cmd_remote_get(args)



def cmd_movie_sources(args):
    """列出公开/公版免费电影资源入口（不搬运盗版源，不破解会员）。"""
    cfg = load_config()
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "sources": MOVIE_SOURCES,
                          "auto_engine": "curl/aria2/yt-dlp", "nas": "get --remote <name>"},
                         ensure_ascii=False, indent=2))
        return 0
    print("免费电影资源（公开/公版/自有授权，请只下载你有权访问的内容）：")
    for i, src in enumerate(MOVIE_SOURCES, start=1):
        print("  %d. %s" % (i, src["name"]))
        print("     入口：%s" % src["how"])
        print("     用法：%s" % src["direct"])
    print()
    print("提速用法：")
    print('  - 种子/磁力：python3 scripts/pan.py get "magnet:?" --to ~/下载（装 aria2）')
    print('  - 直链多源选最快：python3 scripts/pan.py movie get "url1" --candidates "url2,url3"')
    print('  - 下载到 NAS：python3 scripts/pan.py remote add nas 后：python3 scripts/pan.py get "直链或磁力" --remote nas')
    return 0


def cmd_movie_get(args):
    """多候选电影直链测速后选最快下载；带 --remote 则先测速、再交给远程 NAS 下载。"""
    cfg = load_config()
    urls = [getattr(args, "url", None)] or []
    if getattr(args, "candidates", None):
        urls += [c.strip() for c in args.candidates.split(",") if c.strip()]
    urls = [u for u in urls if u]
    if isinstance(urls, str):
        urls = [urls]
    if not urls:
        print("❌ 缺少链接：movie get <url> [--candidates url2,url3]")
        return 1
    best = urls[0]
    detail = ""
    if len(urls) > 1:
        ranked = rank_fastest_urls(urls, cfg=cfg,
                                   timeout=int(getattr(args, "timeout", 6) or 6),
                                   samples=int(getattr(args, "samples", 200000) or 200000))
        ok = [r for r in ranked if r.get("ok")]
        if ok:
            best = ok[0]["url"]
            detail = "（最快 %.1f KB/s）" % ok[0].get("kbps", 0)
        else:
            print("❌ 候选链接均测速失败，尝试用第一个下载。")
    print("选用最快链接%s：%s" % (detail, best))
    remote = getattr(args, "remote", None)
    args2 = argparse.Namespace(url=best, pwd="", at=getattr(args, "at", ""), to=getattr(args, "to", None),
                               engine=getattr(args, "engine", None), tier=getattr(args, "tier", None),
                               path=getattr(args, "path", None), remote=remote or "",
                               dry_run=bool(getattr(args, "dry_run", False)),
                               force=bool(getattr(args, "force", False)),
                               json=bool(getattr(args, "json", False)),
                               events=getattr(args, "events", False), live=getattr(args, "live", False),
                               split=getattr(args, "split", 0) or 0, classify=getattr(args, "classify", None),
                               generic_direct=getattr(args, "generic_direct", False),
                               confirm_own_use=getattr(args, "confirm_own_use", False))
    if remote:
        return _cmd_remote_get(args2)
    return _cmd_get(args2)


def cmd_movie(args):
    """电影入口：先选源（movie sources），再最快下载（movie get / movie x）。"""
    sub = getattr(args, "movie_cmd", None)
    if sub == "sources":
        return cmd_movie_sources(args)
    if sub == "get":
        return cmd_movie_get(args)
    if sub == "x":
        return cmd_movie_x(args)
    print("movie 子命令：sources | get | x")
    print("   movie sources           列出公开/公版电影入口")
    print('   movie get <url> --candidates a,b [--remote nas] [--to dir]  取最快源并下载')
    print('   movie x <url>           下载 X(推特) 视频（走 yt-dlp；登录内容请配置 cookies_from_browser）')
    return 1


def cmd_movie_x(args):
    """下载 X(原推特) 视频：走 stream/yt-dlp；公开推文可直接下。"""
    cfg = load_config()
    url = getattr(args, "url", None)
    if not url:
        print("❌ 缺少 X(推特) 链接：movie x <url>")
        return 1
    key, spec = detect_drive(url, cfg)
    if key != "stream":
        print("❌ %s 未识别为 X/推特视频链接：" % url)
        print("  支持 https://x.com/... 与 https://twitter.com/...（含 mobile.twitter.com）")
        return 1
    if not find_engine_binary("ytdlp", cfg):
        print("❌ 未找到 yt-dlp；请安装便携版或填入 engines.yt-dlp")
        return 2
    if (cfg.get("ytdlp") or {}).get("cookies_from_browser"):
        print("提示：使用 cookies_from_browser=%s（仅本机登录态）。" % cfg["ytdlp"]["cookies_from_browser"])
    else:
        print("提示：X 登录/私密推文若下载失败，请填 config.json ytdlp.cookies_from_browser（如 safari/chrome）后重试。")
    if getattr(args, "dry_run", False):
        plan = build_plan(url, cfg=cfg)
        print(json.dumps(public_plan(plan), ensure_ascii=False, indent=2))
        return 0
    args2 = argparse.Namespace(url=url, pwd="", at="", to=getattr(args, "to", None),
                               engine="ytdlp", tier=getattr(args, "tier", None), path=None,
                               remote=getattr(args, "remote", "") or "",
                               dry_run=False, force=bool(getattr(args, "force", False)),
                               json=bool(getattr(args, "json", False)), events=False,
                               live=getattr(args, "live", False), split=0,
                               classify=getattr(args, "classify", None))
    if getattr(args, "remote", None):
        return _cmd_remote_get(args2)
    return _cmd_get(args2)


SEARCH_KINDS = ("auto", "movie", "video", "music", "file")
SEARCH_PROVIDERS = [
    {"key": "archive", "name": "互联网档案馆(archive.org)", "kinds": ["movie", "video", "music", "file"],
     "desc": "公版/开放电影音频文件，官方 API，无需登录"},
    {"key": "duckduckgo", "name": "DuckDuckGo HTML 搜索", "kinds": ["movie", "video", "music", "file"],
     "desc": "公开网页搜索结果，候选链接需自行判断是否有权下载"},
    {"key": "ytdlp", "name": "yt-dlp 视频搜索", "kinds": ["video", "music"],
     "desc": "可用 yt-dlp 的公开搜索器（ytsearch/bilibili 等），再走 stream 下载"},
]
_MEDIA_KIND_Q = {
    "movie": "mediatype:(movies)",
    "video": "mediatype:(movies)",
    "music": "mediatype:(audio)",
    "file": "mediatype:(texts) OR mediatype:(software)",
}


def fetch_url(url, timeout=20, cfg=None):
    """小体积 HTTP 抓取：标准库 urllib；失败抛 OSError，便于自测 mock。"""
    headers = {"User-Agent": "Mozilla/5.0 (pan-downloader) pan/0.11"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def search_provider_list(kind, cfg=None):
    kind = kind if kind in SEARCH_KINDS else "auto"
    out = []
    for pr in SEARCH_PROVIDERS:
        if kind == "auto" or kind in pr["kinds"]:
            out.append(dict(pr, supported=True))
        else:
            out.append(dict(pr, supported=False))
    return out


def _pick_providers(value, kind):
    value = (value or "auto").strip().lower()
    if value in ("", "auto"):
        return [pr["key"] for pr in SEARCH_PROVIDERS if kind == "auto" or kind in pr["kinds"]]
    keys = [x.strip().lower() for x in value.split(",") if x.strip()]
    return [k for k in keys if k in {pr["key"] for pr in SEARCH_PROVIDERS}]


def search_archive(query, limit=8, timeout=20, cfg=None):
    """archive.org 官方 advancedsearch API，返回可访问的详情页/直链候选。"""
    q = query.strip()
    kind_q = "" if (not cfg or True) else ""
    parts = ['"%s"' % q.replace('"', ' ')]
    mediatype = None
    if cfg and cfg.get("_search_kind"):
        mediatype = _MEDIA_KIND_Q.get(cfg.get("_search_kind"))
    if mediatype:
        parts.append(mediatype)
    url = ("https://archive.org/advancedsearch.php?q=%s&fl[]=identifier&fl[]=title"
           "&rows=%d&page=1&output=json" % (urllib.parse.quote(" ".join(parts), safe=""), int(limit)))
    text = fetch_url(url, timeout=timeout, cfg=cfg)
    data = json.loads(text)
    docs = ((data.get("response") or {}).get("docs")) or []
    result = []
    for d in docs:
        ident = str(d.get("identifier") or "").strip()
        title = str(d.get("title") or ident or "").strip()
        if not ident:
            continue
        result.append({
            "title": title,
            "url": "https://archive.org/details/%s" % ident,
            "provider": "archive",
            "kind": (cfg or {}).get("_search_kind", "movie"),
            "note": "公版/开放内容详情页，打开后选文件用 get/movie get 下载",
        })
    return result


def search_duckduckgo(query, limit=8, timeout=20, cfg=None):
    """DuckDuckGo HTML 结果解析（lite 版）：提取 http/https 链接作为候选。"""
    q = query.strip()
    lq = urllib.parse.quote(q)
    url = "https://html.duckduckgo.com/html/?q=%s&kl=cn-zh" % lq
    text = fetch_url(url, timeout=timeout, cfg=cfg)
    hrefs = re.findall(r'href="(https?://[^"]+)"', text)
    result = []
    seen = set()
    for href in hrefs:
        if "duckduckgo.com" in href or "html.duckduckgo.com" in href:
            continue
        href = urllib.parse.unquote(href)
        if href in seen:
            continue
        seen.add(href)
        result.append({"title": href, "url": href, "provider": "duckduckgo",
                       "kind": (cfg or {}).get("_search_kind", "file"),
                       "note": "网页候选，下载前请确认你有权访问该内容"})
        if len(result) >= int(limit):
            break
    return result


def search_ytdlp(query, limit=8, timeout=20, cfg=None):
    """用 yt-dlp 的公开文本搜索（ytsearch），返回可走 stream 的视频候选。"""
    q = query.strip()
    ytdlp = find_engine_binary("ytdlp", cfg or {})
    if not ytdlp:
        raise OSError("未找到 yt-dlp，无法执行 yt-dlp 搜索")
    argv = [ytdlp, "ytsearch%d:%s" % (int(limit), q), "--flat-playlist",
            "--print", "%(id)s\t%(title)s\t%(webpage_url)s", "--no-warnings"]
    import subprocess as _sp
    proc = _sp.run(argv, capture_output=True, text=True, timeout=timeout)
    result = []
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            vid, title, page = parts[0], parts[1], parts[2]
        elif len(parts) >= 2:
            title, page = parts[0], parts[1]
        else:
            continue
        result.append({"title": title.strip(), "url": page.strip(),
                       "provider": "ytdlp", "kind": "video",
                       "note": "公开视频候选，走 stream(yt-dlp) 下载"})
    return result


def search_candidates(query, kind="auto", providers=None, limit=8, timeout=20, cfg=None):
    """聚合多个公开来源的候选链接；搜索失败的单源自动降级，不中断整体。"""
    kind = kind if kind in SEARCH_KINDS else "auto"
    providers = providers or _pick_providers("auto", kind)
    cfg2 = dict(cfg or {})
    cfg2["_search_kind"] = kind
    jobs = []
    for key in providers:
        if key == "archive":
            jobs.append((key, lambda: search_archive(query, limit=limit, timeout=timeout, cfg=cfg2)))
        elif key == "duckduckgo":
            jobs.append((key, lambda: search_duckduckgo(query, limit=limit, timeout=timeout, cfg=cfg2)))
        elif key == "ytdlp":
            jobs.append((key, lambda: search_ytdlp(query, limit=limit, timeout=timeout, cfg=cfg2)))
    out = []
    for key, fn in jobs:
        try:
            out.extend(fn())
        except (OSError, ValueError, Exception):
            out.append({"provider": key, "title": "", "url": "", "kind": kind,
                        "note": "该源本次不可用（可能未联网或未装 yt-dlp）", "error": True})
    return out



CRAWL_EXT_KIND = {
    "movie": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".rmvb", ".rm", ".ts"),
    "video": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".rmvb", ".rm", ".ts", ".m3u8", ".mpd"),
    "music": (".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a", ".opus", ".wma", ".ape", ".alac"),
    "file":  (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv",
              ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".torrent"),
}


def _absolute_link(base, href):
    if not href:
        return ""
    href = href.strip()
    if not href or href.startswith("#") or href.startswith("javascript:") or href.startswith("data:"):
        return ""
    if href.startswith("//"):
        base_scheme = (base or "http:").split(":", 1)[0]
        return "%s:%s" % (base_scheme, href)
    u = urlparse(href)
    if (u.scheme or "").lower() in ("http", "https", "ftp", "ftps"):
        return href
    if href.startswith("magnet:"):
        return href
    b = urlparse(base)
    import posixpath
    if (b.scheme or "").lower() == "file":
        bpath = b.path or "/"
        if href.startswith("/"):
            return "file://" + posixpath.normpath(href)
        if bpath.endswith("/"):
            base_dir = bpath
        else:
            base_dir = bpath.rsplit("/", 1)[0] or "/"
        joined = posixpath.normpath(posixpath.join(base_dir, href))
        if joined.startswith("../"):
            return ""
        return "file://" + joined
    if not b.scheme or not b.netloc:
        return ""
    bpath = b.path or "/"
    if href.startswith("/"):
        return "%s://%s%s" % (b.scheme, b.netloc, href)
    if bpath.endswith("/"):
        base_dir = bpath
    else:
        base_dir = bpath.rsplit("/", 1)[0] or "/"
    joined = posixpath.normpath(posixpath.join(base_dir, href))
    if joined.startswith("../"):
        return ""
    return "%s://%s%s" % (b.scheme, b.netloc, joined)


def _kind_from_url(url):
    u = urlparse(url)
    path = (u.path or "").lower()
    if url.lower().startswith("magnet:") or path.endswith(".torrent"):
        return "bittorrent_candidate"
    if path.endswith(".m3u8") or path.endswith(".mpd"):
        return "video_candidate"
    for kind in ("movie", "video", "music", "file"):
        for ext in CRAWL_EXT_KIND[kind]:
            if path.endswith(ext):
                return {"movie": "movie_candidate", "video": "video_candidate",
                        "music": "music_candidate", "file": "file_candidate"}[kind]
    return ""


def crawl_page_candidates(url, limit=20, timeout=20, cfg=None, kind="auto", depth=0):
    import posixpath as _pp  # noqa: F401
    cfg2 = dict(cfg or {})
    results = []
    text = fetch_url(url, timeout=timeout, cfg=cfg2)
    candidate_urls = []
    for m in re.finditer(r'(?:href|src|content)\s*=\s*["\']([^"\']+)["\']', text, flags=re.I):
        href = _absolute_link(url, m.group(1))
        if href and href not in candidate_urls:
            candidate_urls.append(href)
    for href in candidate_urls:
        k = _kind_from_url(href)
        if not k or href.startswith("javascript"):
            continue
        if kind != "auto" and kind in ("movie", "video", "music", "file") and not k.startswith(kind):
            continue
        if len(results) >= int(limit):
            break
        results.append({"title": href.rsplit("/", 1)[-1] or href, "url": href, "provider": "crawl",
                        "kind": k.split("_")[0], "note": "网页爬取候选；下载前请确认你有权访问该内容"})
    if depth >= 1 and len(results) < int(limit):
        followed = 0
        seen = set(candidate_urls)
        for href in candidate_urls:
            if followed >= 5 or len(results) >= int(limit):
                break
            if not (href.startswith("http://") or href.startswith("https://")):
                continue
            uh = urlparse(href)
            ub = urlparse(url)
            if uh.netloc != ub.netloc:
                continue
            if not (uh.path.endswith(".htm") or uh.path.endswith(".html")
                    or "/page/" in uh.path or "?" in (uh.query or "")):
                continue
            if href in seen:
                continue
            seen.add(href)
            followed += 1
            try:
                sub = crawl_page_candidates(href, limit=limit - len(results), timeout=timeout,
                                            cfg=cfg2, kind=kind, depth=0)
            except Exception:
                continue
            for c in sub:
                if c["url"] not in seen:
                    seen.add(c["url"])
                    results.append(c)
                if len(results) >= int(limit):
                    break
    order = {"torrent": 0, "video": 1, "movie": 1, "music": 2, "file": 3}
    results.sort(key=lambda c: order.get(c.get("kind"), 9))
    return results[:int(limit)]


def dispatch_chosen_download(args, chosen, query_label=""):
    web_candidate = str(chosen.get("provider") or "") in ("duckduckgo", "web", "crawl")
    if web_candidate and not bool(getattr(args, "dry_run", False)) and not bool(getattr(args, "assume_own", False)) and not bool(getattr(args, "force", False)):
        msg = ("候选「%s」来自网页搜索/爬虫，下载前请确认你对该内容有权访问；" % (chosen.get("title") or chosen.get("url"))) + \
               "确认后请加 --assume-own 或 --force 再执行 --pick（--dry-run 预览计划不需要确认）"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": msg, "need": "assume_own"}, ensure_ascii=False, indent=2))
        else:
            print("⚠️ %s" % msg)
        return 3
    print()
    print("选中第 %d 项：%s" % (getattr(args, "pick", 0) or 0, chosen.get("url")))
    ns = argparse.Namespace(url=chosen.get("url"), pwd="", at="", to=getattr(args, "to", None),
                            engine=getattr(args, "engine", None), tier=getattr(args, "tier", None),
                            path=getattr(args, "path", None), remote=getattr(args, "remote", None) or "",
                            dry_run=bool(getattr(args, "dry_run", False)),
                            force=bool(getattr(args, "force", False)),
                            json=bool(getattr(args, "json", False)), events=False,
                            live=bool(getattr(args, "live", False)), split=int(getattr(args, "split", 0) or 0),
                            classify=getattr(args, "classify", None))
    if getattr(args, "remote", None):
        return _cmd_remote_get(ns)
    return _cmd_get(ns)


def cmd_crawl(args):
    """网络爬虫：抓取一个网页/目录页，提取可直接下载的媒体、文件、magnet/torrent 候选；--pick N 一键下载。"""
    cfg = load_config()
    url = (getattr(args, "url", "") or "").strip()
    kind = getattr(args, "kind", "auto") or "auto"
    kind = kind if kind in SEARCH_KINDS else "auto"
    limit = int(getattr(args, "limit", 20) or 20)
    timeout = int(getattr(args, "timeout", 20) or 20)
    depth = int(getattr(args, "depth", 0) or 0)
    if not url:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": "缺少要抓取的网页 URL"}, ensure_ascii=False, indent=2))
        else:
            print("❌ 缺少 URL：pan crawl <网页URL> [--kind movie|video|music|file] [--pick N]")
        return 1
    try:
        candidates = crawl_page_candidates(url, limit=limit, timeout=timeout, cfg=cfg, kind=kind, depth=depth)
    except Exception as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": ("抓取失败：%s" % exc)[:300]}, ensure_ascii=False, indent=2))
        else:
            print("❌ 抓取失败：%s" % str(exc)[:300])
        return 2
    viable = [c for c in candidates if c.get("url") and not c.get("error")]
    if not viable:
        msg = "未在该页面发现可下载候选（请确认 URL 可访问且页面里含媒体/文件/磁力链接）"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False, indent=2))
        else:
            print("❌ %s" % msg)
        return 2
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "url": url, "kind": kind, "depth": depth,
                          "candidates": viable}, ensure_ascii=False, indent=2))
        return 0
    print("抓取：%s｜类型：%s｜深度：%d" % (url, kind, depth))
    for i, c in enumerate(viable, start=1):
        print("  %d. %s" % (i, c.get("title") or c.get("url")))
        print("     %s" % c.get("url"))
    pick = int(getattr(args, "pick", 0) or 0)
    if 1 <= pick <= len(viable):
        return dispatch_chosen_download(args, viable[pick - 1], query_label=url)
    print()
    print("一键下载：pan crawl \"%s\" --pick <序号> [--kind movie|video|music|file] [--to 目录] [--remote nas] [--depth 1] [--dry-run]" % url)
    return 0


def cmd_search(args):
    """搜索并获得候选链接；--pick N 可直接进入下载流程（本机或 NAS）。"""
    cfg = load_config()
    query = getattr(args, "query", "").strip()
    kind = getattr(args, "kind", "auto")
    kind = kind if kind in SEARCH_KINDS else "auto"
    timeout = int(getattr(args, "timeout", 20) or 20)
    limit = int(getattr(args, "limit", 8) or 8)
    if getattr(args, "check", False):
        return cmd_search_check(cfg, kind=kind, timeout=timeout, json_flag=bool(getattr(args, "json", False)))
    if getattr(args, "list_providers", False):
        provs = search_provider_list(kind, cfg)
        if getattr(args, "json", False):
            print(json.dumps({"ok": True, "kind": kind, "providers": provs}, ensure_ascii=False, indent=2))
        else:
            print("可用搜索源（kind=%s）：" % kind)
            for pr in provs:
                mark = "✓" if pr["supported"] else "·"
                print("  %s %-12s %s" % (mark, pr["key"], pr["name"]))
                print("      %s" % pr["desc"])
        return 0
    if not query:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": "缺少要搜索的关键词"}, ensure_ascii=False))
        else:
            print('❌ 缺少关键词：pan search "关键词" [--kind movie|video|music|file]')
        return 1
    providers = _pick_providers(getattr(args, "providers", "auto"), kind)
    candidates = search_candidates(query, kind=kind, providers=providers, limit=limit, timeout=timeout, cfg=cfg)
    viable = [c for c in candidates if c.get("url") and not c.get("error")]
    if not candidates:
        msg = "未获得任何候选（未联网或所有源不可用）"
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
        else:
            print("❌ %s" % msg)
        return 2
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "query": query, "kind": kind, "providers": providers,
                          "candidates": viable[:limit]}, ensure_ascii=False, indent=2))
        return 0
    print("关键词：%s｜类型：%s｜搜索源：%s" % (query, kind, ",".join(providers) or "auto"))
    for i, c in enumerate(viable, start=1):
        if c.get("error"):
            print("  %d. ⚠️ %s" % (i, c.get("note", "该源不可用")))
        else:
            print("  %d. %s" % (i, c.get("title") or c.get("url")))
            print("     %s" % c.get("url"))
    if not viable:
        print("没有可下载候选；请检查网络或换 --kind / --providers")
        return 2
    pick = int(getattr(args, "pick", 0) or 0)
    if 1 <= pick <= len(viable):
        chosen = viable[pick - 1]
        web_candidate = str(chosen.get("provider") or "") in ("duckduckgo", "web")
        if web_candidate and not bool(getattr(args, "dry_run", False)) and not bool(getattr(args, "assume_own", False)) and not bool(getattr(args, "force", False)):
            msg = ("候选「%s」来自网页搜索，下载前请确认你对该内容有权访问；" % chosen.get("title" or chosen.get("url"))) + \
                   "确认后请加 --assume-own 或 --force 再执行 --pick（--dry-run 预览计划不需要确认）"
            if getattr(args, "json", False):
                print(json.dumps({"ok": False, "error": msg, "need": "assume_own"}, ensure_ascii=False, indent=2))
            else:
                print("⚠️ %s" % msg)
            return 3
        print()
        return dispatch_chosen_download(args, chosen, query_label=query)
    print()
    print("一键下载：pan search \"%s\" --pick <序号> [--to 目录] [--remote nas] [--dry-run]" % query)
    return 0
