"""Source adapters + the API-vs-browser router.

THE ROUTING RULE
----------------
Each source declares how it can be reached:

  mode="api"      plain HTTP JSON API works. Cheapest, use it.
  mode="browser"  bot wall and/or login required. Real browser only.
  mode="auto"     try the API first; if the probe fails, fall back to
                  the browser, which then acts as the HTTP client so we
                  still read the site's own JSON rather than scraping DOM.

`probe_api()` is the decider for "auto": one cheap request, 200 + valid
JSON means the fast path is open, anything else means browser.

Adding a source = adding one subclass + one registry entry.
"""
from __future__ import annotations

import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from errors import ApiUnavailable, NeedsLogin
from normalize import make_record

# Identify yourself. Several sites (Danbooru, e621) ban default library
# UAs and require a name plus contact. Sending a placeholder like
# "set YOUR_EMAIL" is worse than sending nothing: it looks like an
# attempt to evade the rule, and gets the IP banned rather than the
# request throttled. So the contact address is required, not optional.
CONTACT = os.environ.get("HARVEST_CONTACT", "").strip()
UA_BASE = "AgentEpstein/1.0"

API_TIMEOUT = 30


def user_agent() -> str:
    """Build the UA. Raises if the operator has not supplied contact info."""
    if not CONTACT or "@" not in CONTACT:
        raise SystemExit(
            "HARVEST_CONTACT is not set, and it is required.\n"
            "  Danbooru and e621 ban clients that do not identify a contact\n"
            "  address, and a placeholder string gets an IP banned rather\n"
            "  than a request refused.\n"
            "  Set it to a real address you read:\n"
            "    export HARVEST_CONTACT=\"you@example.com\"   # bash\n"
            "    $env:HARVEST_CONTACT = \"you@example.com\"    # PowerShell")
    return f"{UA_BASE} (research dataset harvester; contact: {CONTACT})"


def http_json(url: str, headers: dict | None = None, timeout: int = API_TIMEOUT,
              attempts: int = 3):
    """GET JSON over plain HTTP.

    An HTTPError (401/403/429) is DEFINITIVE — the server answered and
    refused — so it raises immediately and the caller falls back to the
    browser. Anything else (TLS reset, timeout, DNS blip) is TRANSIENT and
    is retried, because a single flaky request must not be mistaken for a
    bot wall and must not push a healthy source onto the slow path.
    """
    last: Exception | None = None
    for i in range(max(1, attempts)):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": user_agent(),
                "Accept": "application/json",
                **(headers or {}),
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as e:                 # 401/403/429...
            raise ApiUnavailable(f"HTTP {e.code} for {url}") from e
        except Exception as e:                              # noqa: BLE001
            last = e
            if i < attempts - 1:
                time.sleep(1.5 * (i + 1))
                continue
            raise ApiUnavailable(f"{type(e).__name__}: {e}") from e
    else:                                                   # pragma: no cover
        raise ApiUnavailable(f"{type(last).__name__}: {last}")

    if not body.strip():
        raise ApiUnavailable(f"empty body for {url}")
    head = body.lstrip()[:120].lower()
    if head.startswith("<"):
        raise ApiUnavailable(f"html not json for {url}")
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise ApiUnavailable(f"bad json for {url}") from e


def ext_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    m = re.search(r"\.([A-Za-z0-9]{2,5})$", path)
    return m.group(1).lower() if m else ""


def parse_count(text: str) -> int:
    """Parse an engagement count as X/Instagram render it.

    '1.2K' -> 1200, '3,456' -> 3456, '2.1M' -> 2100000, '' -> 0.
    Returns -1 when the text carries no number at all (so callers can
    distinguish 'zero' from 'unknown').
    """
    if not text:
        return -1
    t = text.strip().replace(",", "")
    m = re.search(r"([\d.]+)\s*([KkMmBb])?", t)
    if not m:
        return -1
    try:
        n = float(m.group(1))
    except ValueError:
        return -1
    mult = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}
    return int(n * mult.get((m.group(2) or "").lower(), 1))


# ==========================================================================
# Base
# ==========================================================================
class Source:
    name = "base"
    mode = "api"                 # api | browser | auto
    base = ""
    needs_login = False
    referer = ""                 # set when the CDN hotlink-protects

    # -- login markers (a `Browser` reads these via login_needed/probe_login)
    login_url = ""               # where to send the human
    login_url_markers = ("/login",)
    login_dom_markers: tuple[str, ...] = ()
    logged_in_markers: tuple[str, ...] = ()

    # -- API path ----------------------------------------------------------
    def api_url(self, tags: str, limit: int, page: int) -> str:
        raise NotImplementedError

    def api_headers(self) -> dict:
        return {}

    def parse_api(self, payload, tags: str) -> list[dict]:
        raise NotImplementedError

    def search(self, tags: str, limit: int, page: int) -> list[dict]:
        payload = http_json(self.api_url(tags, limit, page), self.api_headers())
        return self.parse_api(payload, tags)

    # -- browser path ------------------------------------------------------
    def browser_search(self, browser, tags: str, limit: int, page: int) -> list[dict]:
        """Default: use the browser purely as an authenticated HTTP client."""
        payload = browser.get_json(self.api_url(tags, limit, page))
        return self.parse_api(payload, tags)


# ==========================================================================
# Danbooru-2.x family  (danbooru, testbooru)
# ==========================================================================
class Danbooru(Source):
    name = "danbooru"
    mode = "auto"                # Cloudflare on the main site; testbooru is open
    base = "https://danbooru.donmai.us"

    def __init__(self, login: str = "", api_key: str = "", base: str = "") -> None:
        self.login = login
        self.api_key = api_key
        if base:
            self.base = base

    def api_url(self, tags, limit, page):
        q = {"tags": tags, "limit": min(limit, 200), "page": page}
        if self.login and self.api_key:
            q["login"] = self.login
            q["api_key"] = self.api_key
        return f"{self.base}/posts.json?" + urllib.parse.urlencode(q)

    def parse_api(self, payload, tags):
        # A booru asked for something it refuses answers with a bare JSON
        # object or string, NOT a list of posts: testbooru returns
        # {"success": false, "error": "PostQuery::TagLimitError"} for more
        # than two tags, and Danbooru's auth wall returns a plain string.
        # Iterating either yields strings, so the p.get() below raised
        # "'str' object has no attribute 'get'" and lost the whole source
        # instead of reporting an empty page. Records must degrade, not crash.
        if isinstance(payload, dict):
            return []
        if not isinstance(payload, list):
            return []
        out = []
        for p in payload:
            if not isinstance(p, dict):
                continue
            if p.get("is_deleted") or p.get("is_banned"):
                continue
            url = p.get("file_url") or p.get("large_file_url") or ""
            if not url:
                continue
            out.append(make_record(
                source=self.name,
                source_id=p.get("id"),
                page_url=f"{self.base}/posts/{p.get('id')}",
                file_url=url,
                tags=p.get("tag_string", ""),
                artist=(p.get("tag_string_artist", "") or "").split()[0]
                        if p.get("tag_string_artist") else "",
                rating=p.get("rating", ""),
                width=p.get("image_width") or 0,
                height=p.get("image_height") or 0,
                file_ext=p.get("file_ext") or ext_from_url(url),
                md5=p.get("md5", ""),
                extra={"source_url": p.get("source"), "pixiv_id": p.get("pixiv_id")},
            ))
        return out


class Testbooru(Danbooru):
    name = "testbooru"
    mode = "api"
    base = "https://testbooru.donmai.us"


# ==========================================================================
# Moebooru family  (yande.re, konachan)
# ==========================================================================
class Moebooru(Source):
    name = "moebooru"
    mode = "auto"
    base = ""

    def __init__(self, base: str = "") -> None:
        if base:
            self.base = base

    def api_url(self, tags, limit, page):
        q = {"tags": tags, "limit": min(limit, 100), "page": page}
        return f"{self.base}/post.json?" + urllib.parse.urlencode(q)

    def parse_api(self, payload, tags):
        out = []
        for p in payload or []:
            url = p.get("file_url") or p.get("jpeg_url") or p.get("sample_url") or ""
            if not url:
                continue
            tags_str = p.get("tags", "")
            artist = p.get("author") or ""
            if not artist:
                m = re.search(r"artist:(\S+)", tags_str)
                artist = m.group(1) if m else ""
            out.append(make_record(
                source=self.name,
                source_id=p.get("id"),
                page_url=f"{self.base}/post/show/{p.get('id')}",
                file_url=url,
                tags=tags_str,
                artist=artist,
                rating=p.get("rating", ""),
                width=p.get("width") or 0,
                height=p.get("height") or 0,
                file_ext=p.get("file_ext") or ext_from_url(url),
                md5=p.get("md5", ""),
                extra={"source_url": p.get("source"), "score": p.get("score")},
            ))
        return out


class Yandere(Moebooru):
    name = "yandere"
    base = "https://yande.re"


class Konachan(Moebooru):
    name = "konachan"
    mode = "browser"             # Cloudflare
    base = "https://konachan.com"


# ==========================================================================
# Gelbooru-DAPI family  (safebooru.org, gelbooru.com)
# ==========================================================================
class Dapi(Source):
    name = "dapi"
    mode = "auto"
    base = ""
    extra_q: dict = {}
    tags_are_html = True

    def __init__(self, api_key: str = "", user_id: str = "") -> None:
        self.api_key = api_key
        self.user_id = user_id

    def api_url(self, tags, limit, page):
        q = {
            "page": "dapi", "s": "post", "q": "index",
            "tags": tags, "limit": min(limit, 100), "pid": page, "json": "1",
        }
        q.update(self.extra_q)
        if self.api_key:
            q["api_key"] = self.api_key
        if self.user_id:
            q["user_id"] = self.user_id
        return f"{self.base}/index.php?" + urllib.parse.urlencode(q)

    def parse_api(self, payload, tags):
        if isinstance(payload, dict):
            payload = payload.get("post") or []
        out = []
        for p in payload or []:
            url = p.get("file_url") or ""
            if not url:
                continue
            raw_tags = p.get("tags", "")
            if self.tags_are_html:
                raw_tags = html.unescape(raw_tags)
            artist = ""
            m = re.search(r"(?:artist|creator):(\S+)", raw_tags)
            if m:
                artist = m.group(1)
            out.append(make_record(
                source=self.name,
                source_id=p.get("id"),
                page_url=f"{self.base}/index.php?page=post&s=view&id={p.get('id')}",
                file_url=url,
                tags=raw_tags,
                artist=artist,
                rating=p.get("rating", ""),
                width=p.get("width") or 0,
                height=p.get("height") or 0,
                file_ext=ext_from_url(url),
                md5=p.get("hash", ""),
                extra={"source_url": p.get("source"), "score": p.get("score")},
            ))
        return out


class Safebooru(Dapi):
    name = "safebooru"
    mode = "api"
    base = "https://safebooru.org"


class Gelbooru(Dapi):
    name = "gelbooru"
    mode = "auto"                # API 401s without api_key+user_id -> browser
    base = "https://gelbooru.com"
    tags_are_html = False


# ==========================================================================
# e621  (nested JSON schema)
# ==========================================================================
class E621(Source):
    name = "e621"
    mode = "api"
    base = "https://e621.net"

    def api_url(self, tags, limit, page):
        q = {"tags": tags, "limit": min(limit, 320), "page": page}
        return f"{self.base}/posts.json?" + urllib.parse.urlencode(q)

    def parse_api(self, payload, tags):
        out = []
        for p in (payload or {}).get("posts", []):
            f = p.get("file") or {}
            url = f.get("url") or ""
            if not url:
                continue
            t = p.get("tags") or {}
            flat = [p.get("description") or ""]
            for group, vals in t.items():
                if isinstance(vals, list):
                    flat.extend(vals)
            out.append(make_record(
                source=self.name,
                source_id=p.get("id"),
                page_url=f"{self.base}/posts/{p.get('id')}",
                file_url=url,
                tags=[v for v in flat if v],
                artist=", ".join((t.get("artist") or [])[:3]),
                rating=p.get("rating", ""),
                width=f.get("width") or 0,
                height=f.get("height") or 0,
                file_ext=f.get("ext") or ext_from_url(url),
                md5=f.get("md5", ""),
                caption=p.get("description") or "",
                extra={"sources": p.get("sources"), "score": p.get("score")},
            ))
        return out


# ==========================================================================
# X / Twitter  — browser only, login required
# ==========================================================================
class Twitter(Source):
    name = "twitter"
    mode = "browser"
    base = "https://x.com"
    needs_login = True
    # X supports engagement thresholds server-side; this is far cheaper
    # than fetching garbage and discarding it, and it is the single most
    # effective quality filter on this site.
    min_likes = 0
    login_url = "https://x.com/login"
    login_url_markers = ("/i/flow/login", "/i/flow/signup", "/login")
    login_dom_markers = (
        'a[href="/login"]',
        '[data-testid="loginButton"]',
        '[data-testid="signupButton"]',
        '[data-testid="LoginForm_Login_Button"]',
    )
    # Positive proof of a session. If one of these is present we are in,
    # even though a logged-out-looking "Sign in" link may also be on the page.
    logged_in_markers = (
        '[data-testid="SideNav_AccountSwitcher_Button"]',
        '[data-testid="AppTabBar_Home_Link"]',
        '[data-testid="AppTabBar_Profile_Link"]',
        '[aria-label="Post"]',
        '[data-testid="primaryColumn"] article',
    )

    def browser_search(self, browser, tags, limit, page):
        """Scroll the media search page and pull pbs.twimg.com media URLs.

        Tweets below `self.min_likes` are dropped before they are even
        considered: on X, search terms say nothing about content quality,
        and low-engagement posts are mostly reposts, screenshots and
        unrelated chatter.
        """
        from queries import build_x_url
        q = tags or "yuri art"
        url = build_x_url(q, min_likes=self.min_likes)
        browser.goto(url, wait="domcontentloaded", settle=5.0)

        # A logged-out X often keeps the /search URL and just renders a
        # sign-in wall, so checking the URL alone is not enough. Treat
        # "wall present" OR "wall present after scrolling" as needing a login.
        if browser.login_wall(self.login_url_markers, self.login_dom_markers,
                              self.logged_in_markers):
            raise NeedsLogin("x.com requires a signed-in session")

        seen: dict[str, dict] = {}
        skipped_low = 0
        stagnant = 0
        while len(seen) < limit and stagnant < 8:
            before = len(seen)
            cards = browser.page.query_selector_all('article[data-testid="tweet"]') \
                or browser.page.query_selector_all("article")
            for card in cards:
                try:
                    imgs = card.query_selector_all('img[src*="pbs.twimg.com/media"]')
                    if not imgs:
                        continue

                    # -- engagement scraping ---------------------------------
                    likes = -1
                    for sel in ('[data-testid="like"] span',
                                '[data-testid="unlike"] span',
                                '[data-testid="like"]',
                                '[data-testid="unlike"]'):
                        el = card.query_selector(sel)
                        if not el:
                            continue
                        likes = parse_count(
                            (el.get_attribute("aria-label") or "")
                            or (el.inner_text() or ""))
                        if likes >= 0:
                            break
                    if self.min_likes and 0 <= likes < self.min_likes:
                        skipped_low += 1
                        continue

                    txt_el = card.query_selector('[data-testid="tweetText"]')
                    caption = (txt_el.inner_text() if txt_el else "") or ""
                    link_el = card.query_selector('a[href*="/status/"]')
                    href = link_el.get_attribute("href") if link_el else ""
                    page_url = f"{self.base}{href}" if href and href.startswith("/") else href
                    for img in imgs:
                        src = img.get_attribute("src") or ""
                        if not src:
                            continue
                        # Promote the thumbnail to the full-resolution original.
                        orig = re.sub(r"[?&]name=[A-Za-z0-9_]+", "", src)
                        orig = orig + ("&" if "?" in orig else "?") + "name=orig"
                        key = orig.split("?")[0]
                        if key in seen:
                            continue
                        tid = re.search(r"/status/(\d+)", href or "")
                        seen[key] = make_record(
                            source=self.name,
                            source_id=f"{tid.group(1) if tid else 't'}_{len(seen)}",
                            page_url=page_url,
                            file_url=orig,
                            tags=[t for t in caption.split() if t.startswith("#")],
                            caption=caption,
                            file_ext="jpg",
                            md5="",
                            extra={"query": q, "likes": likes},
                        )
                except Exception:
                    continue
            browser.page.mouse.wheel(0, 4000)
            browser.page.wait_for_timeout(2200)
            if len(seen) == before:
                stagnant += 1
            else:
                stagnant = 0
            if len(seen) >= limit:
                break

        if skipped_low:
            print(f"    x: skipped {skipped_low} tweet(s) under "
                  f"{self.min_likes} likes")

        # Found nothing at all AND no session: that is a login problem,
        # not an empty result set. Say so instead of reporting "0 kept".
        if not seen and not browser.logged_in(self.logged_in_markers):
            raise NeedsLogin(
                f"no results on x.com for {q!r} and no signed-in session detected")
        return list(seen.values())[:limit]


# ==========================================================================
# Pixiv  — browser only; login needed for R-18 / originals
# ==========================================================================
class Pixiv(Source):
    name = "pixiv"
    mode = "browser"
    base = "https://www.pixiv.net"
    needs_login = True
    referer = "https://www.pixiv.net/"
    login_url = "https://accounts.pixiv.net/login.php"
    login_url_markers = ("/login", "accounts.pixiv.net")
    login_dom_markers = (
        'a[href*="/login"]',
        'button[data-click-action="login"]',
    )
    logged_in_markers = (
        'a[href="/bookmark.php"]',
        'a[href="/users/"]',
        '[data-testid="user-icon"]',
        'aside figure img',
    )

    def browser_search(self, browser, tags, limit, page):
        word = tags or "yuri"
        api = (f"{self.base}/ajax/search/artworks/{urllib.parse.quote(word)}"
               f"?word={urllib.parse.quote(word)}&order=date_d&mode=all"
               f"&p={page}&s_mode=s_tag&type=all&lang=en")
        browser.goto(f"{self.base}/", wait="domcontentloaded", settle=2.0)
        try:
            payload = browser.get_json(api)
        except Exception as e:
            raise NeedsLogin(
                f"pixiv ajax search failed ({e}); sign in and retry") from e

        data = ((payload or {}).get("body") or {}).get("illustManga", {}).get("data", [])
        out = []
        for it in data:
            if len(out) >= limit:
                break
            iid = it.get("id")
            thumb = it.get("url") or ""
            url = thumb
            w = h = 0
            try:                                   # resolve the original
                detail = browser.get_json(f"{self.base}/ajax/illust/{iid}")
                d = (detail or {}).get("body") or {}
                url = d.get("urls", {}).get("original") or url
                w = d.get("width") or 0
                h = d.get("height") or 0
            except Exception:
                pass
            if not url:
                continue
            tag_list = []
            for t in (it.get("tags") or []):
                tag_list.append(t if isinstance(t, str) else t.get("tag", ""))
            out.append(make_record(
                source=self.name,
                source_id=iid,
                page_url=f"{self.base}/en/artworks/{iid}",
                file_url=url,
                tags=[t for t in tag_list if t],
                artist=it.get("userName") or "",
                rating="r18" if it.get("xRestrict") else "general",
                width=w, height=h,
                file_ext=ext_from_url(url) or "jpg",
                md5="",
                caption=it.get("description") or "",
                extra={"user_id": it.get("userId"), "query": word},
            ))
        return out


# ==========================================================================
# Registry
# ==========================================================================
def build_registry(cfg: dict | None = None) -> dict:
    cfg = cfg or {}
    db = cfg.get("danbooru", {})
    gb = cfg.get("gelbooru", {})
    return {
        "danbooru":   Danbooru(db.get("login", ""), db.get("api_key", "")),
        "testbooru":  Testbooru(),
        "yandere":    Yandere(),
        "konachan":   Konachan(),
        "safebooru":  Safebooru(),
        "gelbooru":   Gelbooru(gb.get("api_key", ""), gb.get("user_id", "")),
        "e621":       E621(),
        "twitter":    Twitter(),
        "pixiv":      Pixiv(),
    }


def probe_api(src: Source, tags: str = "yuri") -> tuple[bool, str]:
    """Is the cheap path open for this source? (ok, detail)."""
    if src.mode == "browser":
        return False, "browser-only source"
    try:
        n = len(src.search(tags, 1, 1))
        return True, f"api ok ({n} item)"
    except ApiUnavailable as e:
        return False, str(e)
    except Exception as e:                                # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
