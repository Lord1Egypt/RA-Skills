"""harvest.py — orchestrator.

Routes each source through the cheapest transport that works, downloads
the images, verifies them, and writes a dataset folder.

    python harvest.py --sources danbooru,yandere,e621 \
        --tags "yuri" --limit 30 --out ./dataset

Exit codes
    0  ok
    2  a source needed a human login (window left open instructions)
    3  no images harvested
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from errors import ApiUnavailable, Blocked, NeedsLogin          # noqa: E402
from normalize import (CEILING_CHOICES, RATING_ORDER, dedupe,     # noqa: E402
                       load_jsonl, record_key, safety_ok, slug,
                       sha256_file, write_jsonl)
from queries import Plan, Query, plan                             # noqa: E402
from search import SearchDriver                                   # noqa: E402

# The profile root is deliberately NOT the skill name. It holds the user's
# browser sessions and logins, so renaming the skill must not orphan them,
# and a cache path should not carry a brand anyway.
# Override with HARVEST_PROFILE_ROOT if you need a second, separate profile.
DEFAULT_PROFILE_ROOT = Path(
    os.environ.get("HARVEST_PROFILE_ROOT", "")
    or Path.home() / ".cache" / "art-dataset-harvest" / "profiles"
)
MIN_SIDE = 512          # reject thumbnails / icons masquerading as art
MIN_BYTES = 20_000


# ==========================================================================
# Config
# ==========================================================================
def load_config() -> dict:
    """Credentials come from the environment only, never from a file
    committed to the skill."""
    return {
        "danbooru": {
            "login": os.environ.get("DANBOORU_LOGIN", ""),
            "api_key": os.environ.get("DANBOORU_API_KEY", ""),
        },
        "gelbooru": {
            "api_key": os.environ.get("GELBOORU_API_KEY", ""),
            "user_id": os.environ.get("GELBOORU_USER_ID", ""),
        },
    }


# ==========================================================================
# Downloading
# ==========================================================================
def _plain_get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/131.0.0.0 Safari/537.36"),
        "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download_image(url: str, dest: Path, browser=None, referer: str = "") -> bool:
    """Fetch one image. Hosts that hotlink-protect (pixiv) must go through
    the browser context so the Referer header survives."""
    data = None
    try:
        if browser is not None and referer:
            data = browser.fetch_bytes(url, referer=referer)
        else:
            data = _plain_get(url)
    except Exception:
        if browser is not None:                     # retry through browser
            try:
                data = browser.fetch_bytes(url, referer=referer or None)
            except Exception:
                return False
        else:
            return False
    if not data or len(data) < 1024:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True


def verify_image(path: Path) -> tuple[bool, str, int, int]:
    """Return (ok, reason, w, h). Rejects corrupt files and tiny images."""
    try:
        from PIL import Image
    except ImportError:
        return True, "", 0, 0
    try:
        if path.stat().st_size < MIN_BYTES:
            return False, "too-small-bytes", 0, 0
        with Image.open(path) as im:
            w, h = im.size
            fmt = (im.format or "").upper()
            im.verify()
        if fmt not in {"JPEG", "PNG", "GIF", "WEBP", "BMP"}:
            return False, f"format:{fmt}", w, h
        if min(w, h) < MIN_SIDE:
            return False, f"too-small:{w}x{h}", w, h
        return True, "", w, h
    except Exception as e:                                   # noqa: BLE001
        return False, f"corrupt:{type(e).__name__}", 0, 0


# ==========================================================================
# Main
# ==========================================================================
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Harvest anime/yuri art into a dataset.")
    p.add_argument("--sources", default="danbooru",
                   help="comma list: danbooru,testbooru,yandere,konachan,"
                        "safebooru,gelbooru,e621,twitter,pixiv")
    p.add_argument("--tags", default="yuri", help="search query / tag string")
    p.add_argument("--fandom", default="",
                   help="game/show/franchise name; used to fan out queries on "
                        "sources with loose tagging (x, pixiv)")
    p.add_argument("--chars", default="",
                   help="comma list of character names to pair up, "
                        "e.g. 'raiden,yae'")
    p.add_argument("--ship-tags", default="",
                   help="comma list of KNOWN ship names, used verbatim and "
                        "ranked above everything generated, e.g. "
                        "'Jinhli,Changli,Yangyang'")
    p.add_argument("--aggressive", action="store_true",
                   help="also search hashtag-compounded queries "
                        "(#Jinhsi #Changli). Hashtag posts are "
                        "disproportionately actual fanart rather than "
                        "reposts and screenshots, so this finds real art a "
                        "keyword search misses. Costs extra queries.")
    p.add_argument("--max-queries", type=int, default=12,
                   help="cap on expanded queries per source")
    p.add_argument("--vision", action="store_true",
                   help="after harvesting, emit a vision worklist for images "
                        "from loosely-tagged sources (x, pixiv)")
    p.add_argument("--vision-gate", action="store_true",
                   help="collect a large candidate POOL from loosely-tagged "
                        "sources WITHOUT downloading, queue it for vision "
                        "review, and stop. Verify, then run --download-only. "
                        "This is the correct flow for X/Pixiv: search terms "
                        "there do not indicate content, so only visually "
                        "confirmed images should be downloaded.")
    p.add_argument("--pool", type=int, default=0,
                   help="candidates to collect per source when --vision-gate "
                        "is on (default: 4x --limit)")
    p.add_argument("--min-likes", type=int, default=0,
                   help="X only: drop tweets below this like count. Applied "
                        "server-side via min_faves: and re-checked on the "
                        "page. Low-engagement posts on X are mostly reposts, "
                        "screenshots and chatter — this is the cheapest "
                        "quality filter on that site.")
    p.add_argument("--download-only", action="store_true",
                   help="download + verify images for rows already in "
                        "metadata.jsonl, skipping harvesting entirely")
    p.add_argument("--limit", type=int, default=25, help="images per source")
    p.add_argument("--pages", type=int, default=1, help="API pages per source")
    p.add_argument("--out", default="", help="output folder")
    # Alias, because every other script in this skill takes --dataset and
    # the instructions harvest.py prints must be copy-pasteable.
    p.add_argument("--dataset", dest="dataset_alias", default="",
                   help="alias for --out, for consistency with the other "
                        "scripts; if both are given, --out wins")
    p.add_argument("--rating", default="general",
                   choices=list(CEILING_CHOICES),
                   help="maximum rating to keep: general (default, safest) "
                        "| sensitive | questionable | explicit | any. This "
                        "is a CEILING, not an exact match, so 'sensitive' "
                        "keeps general and sensitive together. Decides "
                        "whether you get safe results only or everything "
                        "the source has.")
    p.add_argument("--show-rating-breakdown", action="store_true",
                   help="after a run, print how many rows fell in each "
                        "rating band and how many reported none")
    p.add_argument("--headed", action="store_true",
                   help="show the browser window (needed for logins; better "
                        "bot-wall pass rate)")
    p.add_argument("--channel", default="msedge",
                   help="'msedge'/'chrome' for an installed real browser, "
                        "'' for bundled Chromium")
    p.add_argument("--cdp", default="",
                   help="attach to an existing real browser instead of "
                        "launching one, e.g. http://localhost:9222 . Required "
                        "for sites that refuse an automated login (X). "
                        "Start it with scripts/start_browser.py")
    p.add_argument("--delay", type=float, default=1.0,
                   help="seconds between requests (be a good citizen)")
    p.add_argument("--login-wait", type=int, default=600,
                   help="seconds to wait for a human login")
    p.add_argument("--no-wait", action="store_true",
                   help="deprecated and ignored: the harvester never blocks "
                        "waiting on stdin. A login is reported and the run "
                        "exits 2; re-run with --logged-in once the user has "
                        "signed in. Kept so old command lines still parse.")
    p.add_argument("--logged-in", action="store_true",
                   help="the user has signed in already. Skips the login "
                        "gate, but still verifies a real session before "
                        "spending queries, so a claim of being signed in "
                        "cannot turn into a silent 'found 0'.")
    p.add_argument("--dry-run", action="store_true", help="list, download nothing")
    p.add_argument("--probe", action="store_true",
                   help="report which transport each source uses, then exit")
    args = p.parse_args(argv)
    # --out defaults to "" so the alias can fill in without needing to know
    # which of the two the user actually typed. --out wins if both are given.
    args.out = args.out or args.dataset_alias or "./dataset"
    return args


def await_session(br, src, timeout_s: int = 180) -> bool:
    """Poll for positive proof of a signed-in session. No stdin involved.

    The user said they logged in, so rather than trusting the claim blindly,
    watch for actual DOM evidence. Requires `logged_in_markers` rather than
    mere absence of a wall: a logged-out X keeps the /search URL and renders
    a sign-in overlay, and a logged-out Pixiv serves its marketing page.
    Neither matches a wall marker, so a naive check reports success on a page
    that is not signed in, and the run then reports "found 0" — which reads
    as "no such art exists" when the truth is "you were never signed in".
    """
    markers = tuple(getattr(src, "logged_in_markers", ()) or ())
    if not markers:
        return True
    if br.logged_in(markers):
        return True
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(3)
        if br.logged_in(markers):
            return True
    return False


def ask_for_login(br, src, args, reason: str = "") -> bool:
    """Ask for a human login, in terms the AGENT can relay to the user.

    This is the ONLY place a login is requested, and it never types
    anything: the human completes it in the visible window.

    The person using this skill is talking to an agent, not sitting at a
    terminal, so this never asks them to type into a script they cannot see.
    It prints a block the agent copies into the conversation; the user
    answers in their own client; the agent then re-runs with --logged-in.
    """
    lurl = src.login_url or src.base
    print("")
    print("=" * 66)
    print(f"  {src.name.upper()}: NEEDS HUMAN LOGIN")
    print("=" * 66)
    if reason:
        print(f"  reason: {reason}")
    print("  A browser window is open. Ask the user to sign in at:")
    print(f"    {lurl}")
    print()
    print("  Relay this to the user:")
    print(f"    \"A {src.name} browser window is open at {lurl}.")
    print("     Please sign in there yourself, including any 2FA or captcha.")
    print("     I can't type your password for you. Tell me when you're done\"")
    print()
    print("  Then re-run this harvest with --logged-in, which skips this gate")
    print("  and verifies the session before spending any queries.")
    print("=" * 66 + "\n", flush=True)

    if args.logged_in:
        # The user already said they signed in. Verify rather than trust it.
        if not await_session(br, src, timeout_s=args.login_wait):
            print(f"  --logged-in was set but no session is detectable on "
                  f"{src.name}. The sign-in did not take, or the session "
                  f"expired. Re-run without it.", file=sys.stderr)
            return False
        print(f"  session confirmed on {src.name}")
        return True

    return False


def render_probe(registry, sources: list[str], tags: str) -> None:
    from sources import probe_api
    print(f"{'source':<12} {'mode':<9} {'api reachable':<15} detail")
    print("-" * 74)
    for name in sources:
        src = registry[name]
        if src.mode in ("api", "auto"):
            ok, detail = probe_api(src, tags)
        else:
            ok, detail = False, "browser-only"
        print(f"{name:<12} {src.mode:<9} {('yes' if ok else 'no'):<15} {detail[:40]}")
    print("\napi reachable = the plain-HTTP fast path is open right now.")
    print("anything 'no' is harvested through the browser instead.")


def rating_breakdown(rows: list[dict]) -> dict[str, int]:
    """Count rows per normalized rating band, unknown included."""
    out: dict[str, int] = {}
    for r in rows:
        k = r.get("rating") or "unknown"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(),
                       key=lambda kv: RATING_ORDER.get(kv[0], 99)))


def print_rating_breakdown(kept: list[dict], dropped: list[dict]) -> None:
    """Say what the rating choice actually cost.

    Without this, a user who asks for safe results cannot tell the
    difference between "the source had nothing else" and "the ceiling
    threw away 400 rows", and neither can they tell that 12 rows reported
    no rating at all and therefore were never checked against anything.
    """
    kb = rating_breakdown(kept)
    db = rating_breakdown(dropped)
    if not kb and not db:
        return
    bands = [b for b in RATING_ORDER if kb.get(b) or db.get(b)]
    if kb.get("unknown") or db.get("unknown"):
        bands.append("unknown")
    print(f"\n{'rating':<14}{'kept':>8}{'excluded':>10}")
    print("-" * 32)
    for b in bands:
        print(f"{b:<14}{kb.get(b, 0):>8}{db.get(b, 0):>10}")
    print("-" * 32)
    print(f"{'total':<14}{sum(kb.values()):>8}{sum(db.values()):>10}")
    unknown = kb.get("unknown", 0)
    if unknown:
        print(f"\n{unknown} kept row(s) reported no rating, so the ceiling "
              f"could not apply to them.")
        print("Sources without a rating field are not asserting the content "
              "is safe. Use --rating general and check the images, or filter "
              "on the vision pass instead.")


def rating_ok(rating: str, ceiling: str) -> tuple[bool, str]:
    """Is `rating` at or below `ceiling`?

    `ceiling` is a maximum, not an exact match: "--rating sensitive"
    admits general AND sensitive. "any" admits everything. "unknown" is
    admitted under any ceiling because a source that does not report a
    rating has not asserted anything — refusing it would silently empty
    the dataset from every source that omits the field. Callers that need
    a guarantee rather than a default should count unknown separately,
    which the harvest report does.
    """
    if ceiling not in RATING_ORDER:
        return True, ""                      # "any"
    if not rating or rating == "unknown":
        return True, ""
    if RATING_ORDER.get(rating, 99) <= RATING_ORDER[ceiling]:
        return True, ""
    return False, f"rating:{rating}"


def filter_rows(rows: list[dict], args, rejected: list[dict]) -> list[dict]:
    """Apply the HARD safety filters and the rating ceiling to `rows`.

    Every path that can put an image on disk must go through here. Rows
    arriving via --download-only were filtered when they were harvested,
    but metadata.jsonl is a plain file: it can be edited, merged from
    another run, or written by an earlier version of this script with
    different filters. Re-applying the filter at download time means the
    exclusion holds at the moment content actually lands on disk, not
    only at the moment it was fetched.
    """
    keep: list[dict] = []
    for r in rows:
        ok, why = safety_ok(r.get("tags") or r.get("caption", ""))
        if not ok:
            rejected.append({**r, "reject_reason": why})
            continue
        ok, why = rating_ok(r.get("rating", "unknown"), args.rating)
        if not ok:
            rejected.append({**r, "reject_reason": why})
            continue
        keep.append(r)
    return keep


def merge_rejected(out: Path, rejected: list[dict]) -> int:
    """Append new rejections to rejected.jsonl without duplicating old ones.

    --download-only is resumable, so a row that fails to download will
    fail again on the next run. Appending blindly grows the audit trail
    with N copies of the same failure. Dedupe on record identity.
    """
    prev = load_jsonl(out / "rejected.jsonl")
    seen = {record_key(r) for r in prev}
    added = 0
    for r in rejected:
        k = record_key(r)
        if k in seen:
            continue
        seen.add(k)
        prev.append(r)
        added += 1
    write_jsonl(out / "rejected.jsonl", prev)
    return added


def write_manifest(out: Path, args, chars: list[str], wanted: list[str],
                   per_source: dict, n_images: int, n_rejected: int,
                   login_needed: list[str]) -> Path:
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "query": args.tags,
        "fandom": args.fandom,
        "chars": chars,
        "sources_requested": wanted,
        # A ceiling, not a band match: "sensitive" means general+sensitive.
        "rating_filter": args.rating,
        "rating_is_ceiling": True,
        "limit_per_source": args.limit,
        "pages": args.pages,
        "total_images": n_images,
        "total_rejected": n_rejected,
        "per_source": per_source,
        "login_still_needed": login_needed,
        "schema_version": 1,
    }
    mp = out / "manifest.json"
    mp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return mp


def download_rows(rows: list[dict], out: Path, registry, ensure_browser,
                  args, rejected: list[dict]) -> list[dict]:
    """Download + verify every row that does not already have a file.

    Plain HTTP first (fast, no browser). Anything a CDN refuses —
    Cloudflare, hotlink protection — retries through the browser with the
    post page as Referer, which is what those CDNs actually check.
    """
    final: list[dict] = []
    for i, r in enumerate(rows, 1):
        ext = (r.get("file_ext") or "jpg").lstrip(".")
        stem = slug(f"{r['source']}_{r['source_id']}_{(r.get('md5') or '')[:8]}", 90)
        rel = f"images/{stem}.{ext}"
        dest = out / rel
        print(f"  [{i}/{len(rows)}] {r['source']}:{r['source_id']}", end=" ")

        if dest.exists() and dest.stat().st_size > 1024:
            ok, why, w, h = verify_image(dest)
            if ok:
                r["file_path"] = rel
                r["file_name"] = rel
                if w and h:
                    r["width"], r["height"] = w, h
                r["sha256"] = sha256_file(dest)
                r["bytes"] = dest.stat().st_size
                final.append(r)
                print(f"already present {w}x{h}")
                continue

        referer = ""
        try:
            referer = registry[r["source"]].referer
        except KeyError:
            pass

        ok = download_image(r["file_url"], dest)
        if not ok:
            ok = download_image(r["file_url"], dest,
                                browser=ensure_browser(),
                                referer=referer or r.get("page_url", ""))
        if not ok:
            print("FAILED (download)")
            rejected.append({**r, "reject_reason": "download-failed"})
            continue

        ok, why, w, h = verify_image(dest)
        if not ok:
            print(f"FAILED ({why})")
            rejected.append({**r, "reject_reason": why})
            try:
                dest.unlink()
            except OSError:
                pass
            continue

        r["file_path"] = rel
        r["file_name"] = rel
        if w and h:
            r["width"], r["height"] = w, h
        r["sha256"] = sha256_file(dest)
        r["bytes"] = dest.stat().st_size
        final.append(r)
        print(f"ok {w}x{h}")
        if args.delay:
            time.sleep(max(0.3, args.delay / 2))
    return final


def main(argv=None) -> int:
    args = parse_args(argv)
    tags = args.tags
    chars = [c.strip() for c in args.chars.split(",") if c.strip()]
    ship_tags = [s.strip() for s in args.ship_tags.split(",") if s.strip()]
    out = Path(args.out).resolve()
    images_dir = out / "images"

    import sources as S
    from queries import expand
    from vision_filter import LOOSE_TAGGING
    registry = S.build_registry(load_config())
    # X engagement threshold lives on the source object so the query URL
    # and the on-page re-check share one value.
    if args.min_likes and "twitter" in registry:
        registry["twitter"].min_likes = args.min_likes
    wanted = [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in wanted if s not in registry]
    if unknown:
        print(f"unknown source(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"available: {', '.join(sorted(registry))}", file=sys.stderr)
        return 1

    if args.probe:
        render_probe(registry, wanted, tags)
        return 0

    if args.rating != "any":
        print(f"rating ceiling: {args.rating} and below "
              f"(pass --rating any for everything the source has)")
    else:
        print("rating ceiling: none, all ratings included")

    # ---- download-only: resume a dataset that was vision-gated ---------
    # Used after vision_filter --apply --drop to fetch the survivors.
    if args.download_only:
        rows = load_jsonl(out / "metadata.jsonl")
        if not rows:
            print(f"no metadata.jsonl rows in {out}", file=sys.stderr)
            return 1
        print(f"download-only: {len(rows)} row(s) in {out}")
        rejected: list[dict] = []

        # Re-apply the HARD filters. See filter_rows() — metadata.jsonl is
        # just a file, and this is the last point before content hits disk.
        rows = filter_rows(rows, args, rejected)
        if not rows:
            print(f"every row was filtered out ({len(rejected)} rejection(s)); "
                  f"nothing to download", file=sys.stderr)
            merge_rejected(out, rejected)
            return 3

        browser = None
        browser_cm = None

        def ensure_browser_dl(headed=None):
            nonlocal browser, browser_cm
            if browser is None:
                from browser import Browser
                browser_cm = Browser(DEFAULT_PROFILE_ROOT / "shared",
                                     headed=args.headed,
                                     channel=args.channel or None,
                                     cdp_url=args.cdp)
                browser = browser_cm.__enter__()
            return browser

        try:
            final = download_rows(rows, out, registry, ensure_browser_dl,
                                  args, rejected)
        finally:
            if browser_cm is not None:
                try:
                    browser_cm.__exit__(None, None, None)
                except Exception:                              # noqa: BLE001
                    pass
        write_jsonl(out / "metadata.jsonl", final)
        added = merge_rejected(out, rejected)
        dupes = len(rejected) - added
        # Refresh the manifest so total_images matches what actually landed
        # on disk. A gated dataset wrote one with a queued-not-downloaded
        # count, and this run is what actually resolves it.
        prev = {}
        mp = out / "manifest.json"
        if mp.exists():
            try:
                prev = json.loads(mp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                prev = {}
        prev["total_images"] = len(final)
        prev["total_rejected"] = prev.get("total_rejected", 0) + added
        prev["downloaded_utc"] = datetime.now(timezone.utc).isoformat()
        per_source = prev.get("per_source", {})
        for r in final:
            st = per_source.setdefault(
                r.get("source", "?"), {"found": 0, "kept": 0, "transport": "",
                                       "error": ""})
            st["kept"] = st.get("kept", 0) + 1
        prev["per_source"] = per_source
        mp.write_text(json.dumps(prev, indent=2), encoding="utf-8")
        print(f"\ndownloaded {len(final)}/{len(rows)} -> {out}")
        if rejected:
            print(f"  {added} new rejection(s) recorded"
                  f"{f', {dupes} already on file' if dupes else ''}")
        return 0 if final else 3

    # ---- lazy browser: only opened if some source actually needs it ----
    browser = None
    browser_cm = None

    def ensure_browser(headed=None):
        nonlocal browser, browser_cm
        if browser is None:
            from browser import Browser
            profile = DEFAULT_PROFILE_ROOT / "shared"
            browser_cm = Browser(profile,
                                 headed=(args.headed if headed is None else headed),
                                 channel=args.channel or None,
                                 cdp_url=args.cdp)
            browser = browser_cm.__enter__()
        return browser

    collected: list[dict] = []
    rejected: list[dict] = []
    rating_dropped: list[dict] = []
    per_source: dict[str, dict] = {}
    login_needed: list[str] = []

    def _drive(the_plan, one, target: int, adaptive: bool) -> list[dict]:
        """Run the plan. Adaptive on loosely-tagged sources, a single pass
        on strict-tag ones where the query is already exact."""
        if not adaptive:
            return one(tags, target)
        drv = SearchDriver(target=target, delay=args.delay)
        drv.plan = the_plan.queries
        rows = drv.run(one, key=lambda r: r.get("md5")
                       or f"{r.get('source')}:{r.get('source_id')}")
        print(f"[{name}] {drv.summary().splitlines()[0]}")
        print(f"    stopped because: {drv.stopped_because}")
        for q in drv.to_report()["dry_queries"][:6]:
            print(f"    dry: {q}")
        return rows

    try:
        for name in wanted:
            src = registry[name]
            stat = {"found": 0, "kept": 0, "transport": "", "error": ""}
            per_source[name] = stat

            # ---- preflight: ask for a session BEFORE burning queries ----
            # Without this a logged-out X just returns zero results and the
            # run reports "found 0" — which reads as "no art exists" rather
            # than "you are not signed in".
            if src.needs_login:
                try:
                    br = ensure_browser(headed=True)
                except Exception as e:                        # noqa: BLE001
                    # A browser that will not start is an environment
                    # problem, not a source problem. Report it as such and
                    # keep going with the other sources, rather than
                    # crashing the whole run on one unreachable site.
                    stat["error"] = f"browser unavailable: {e}"
                    print(f"[{name}] cannot open a browser: {e}",
                          file=sys.stderr)
                    login_needed.append(name)
                    continue
                if args.logged_in:
                    # The user says they signed in. Verify, don't trust it.
                    ok = await_session(br, src, timeout_s=args.login_wait)
                    stat["login"] = "logged_in" if ok else "not_detected"
                    print(f"[{name}] session check: {stat['login']}")
                    if not ok:
                        print(f"[{name}] --logged-in was set but no session "
                              f"is detectable. The sign-in did not take, or "
                              f"it expired.", file=sys.stderr)
                        stat["error"] = "login claimed but not detected"
                        login_needed.append(name)
                        continue
                else:
                    state = br.probe_login(src)
                    stat["login"] = state
                    print(f"[{name}] session check: {state}")
                    if state != "logged_in":
                        if not ask_for_login(
                                br, src, args,
                                "no signed-in session detected"):
                            login_needed.append(name)
                            stat["error"] = "login required"
                            continue

            # ---- pick the transport -----------------------------------
            transport = "api"
            if src.mode == "browser":
                transport = "browser"
            elif src.mode == "auto":
                ok, detail = S.probe_api(src, tags)
                transport = "api" if ok else "browser"
                print(f"[{name}] probe: {'api ok' if ok else 'api blocked (' + detail[:50] + ')'}"
                      f" -> using {transport}")
            stat["transport"] = transport

            # ---- harvest ----------------------------------------------
            # Two transports, one normalized output. `auto` probes first;
            # if the plain-HTTP path then fails mid-run, downgrade to the
            # browser instead of losing the source.
            fetched: list[dict] = []

            # With --vision-gate we are collecting candidates to be checked,
            # not results to keep, so pull a much wider pool.
            target = args.limit
            if args.vision_gate and src.name in LOOSE_TAGGING:
                target = args.pool or (args.limit * 4)

            loose = src.name in LOOSE_TAGGING
            if loose:
                # Loosely-tagged sources get a RANKED plan and an adaptive
                # driver, because a fixed list treats a dry query as a
                # finished search. On X, "wuwa denrika art" returns 0 while
                # "wuwa denrika" returns 5; the driver relaxes and recovers.
                the_plan = plan(
                    args.fandom, chars,
                    ship_tags=ship_tags,
                    aggressive=args.aggressive,
                    max_queries=args.max_queries)
                for note in the_plan.notes:
                    print(f"[{name}] {note}")
                print(f"[{name}] {len(the_plan)} ranked quer(y/ies), "
                      f"cap {target}, adaptive stop on diminishing returns")
            else:
                # Strict-tag sources: one tag IS the query. A plan here
                # would only dilute it.
                the_plan = Plan([Query(tags, "tag", 50)])

            per_query = max(4, target // max(1, len(the_plan)))

            def fetch_api() -> list[dict]:
                def one(text, want):
                    out = []
                    for page in range(1, args.pages + 1):
                        got = src.search(text, want, page)
                        out.extend(got)
                        if not got:
                            break
                    return out
                return _drive(the_plan, one, target, loose)

            def fetch_browser(br) -> list[dict]:
                def one(text, want):
                    out = []
                    for page in range(1, args.pages + 1):
                        got = src.browser_search(br, text, want, page)
                        out.extend(got)
                        if not got:
                            break
                    return out
                return _drive(the_plan, one, target, loose)

            try:
                if transport == "api":
                    try:
                        fetched = fetch_api()
                    except ApiUnavailable as e:
                        print(f"[{name}] plain-HTTP path failed mid-run ({e})"
                              f" -> falling back to browser")
                        transport = "browser"
                        stat["transport"] = "browser (runtime fallback)"
                        fetched = fetch_browser(ensure_browser(headed=args.headed))
                else:
                    fetched = fetch_browser(
                        ensure_browser(headed=args.headed or src.needs_login))
            except NeedsLogin as e:
                # Hand off to the human, then retry once in the same session.
                print(f"[{name}] LOGIN REQUIRED: {e}")
                br = ensure_browser(headed=True)
                if not ask_for_login(br, src, args, str(e)):
                    login_needed.append(name)
                    stat["error"] = "login not completed"
                    continue
                try:
                    fetched.extend(src.browser_search(
                    br, the_plan.texts()[0] if len(the_plan) else tags,
                    per_query, 1))
                except Exception as e2:                  # noqa: BLE001
                    stat["error"] = f"after-login fetch failed: {e2}"
            except Blocked as e:
                stat["error"] = f"blocked: {e}"
                print(f"[{name}] blocked: {e}")
                continue
            except ApiUnavailable as e:
                stat["error"] = f"api: {e}"
                print(f"[{name}] api error: {e}")
                continue
            except Exception as e:                            # noqa: BLE001
                stat["error"] = f"{type(e).__name__}: {e}"
                print(f"[{name}] error: {e}")
                continue

            # The per-query split can overshoot the cap; enforce it here so
            # --limit means what it says.
            if len(fetched) > target:
                fetched = fetched[:target]

            stat["found"] = len(fetched)
            before = len(rejected)

            # ---- safety + rating filter --------------------------------
            keep = filter_rows(fetched, args, rejected)
            rating_dropped.extend(r for r in rejected[before:]
                                  if str(r.get("reject_reason", "")).startswith("rating:"))

            # ---- dedupe across ALL sources so far ----------------------
            combined, _ = dedupe(collected + keep)
            collected = combined
            stat["kept"] = len(keep)
            print(f"[{name}] found {len(fetched)}, kept {len(keep)}, "
                  f"rejected {len(fetched) - len(keep)}")

        # ---- vision gate: stop BEFORE downloading ---------------------
        # On loosely-tagged sources a search hit is not evidence of
        # content. Queue the whole candidate pool for visual review and
        # download nothing until someone has actually looked at them.
        if args.vision_gate:
            out.mkdir(parents=True, exist_ok=True)
            write_jsonl(out / "metadata.jsonl", collected)
            wl = [{
                "source": r["source"],
                "source_id": r["source_id"],
                "image": r["file_url"],
                "page_url": r.get("page_url", ""),
                "caption": (r.get("caption") or "")[:200],
                "question": "How many female-presenting characters are "
                            "visible, and are two of them a couple?",
            } for r in collected]
            (out / "vision_worklist.json").write_text(
                json.dumps(wl, indent=2), encoding="utf-8")
            merge_rejected(out, rejected)
            # Write the manifest here too: a gated dataset is a real,
            # resumable artifact, and publish.py reads this file. Without
            # it the dataset card says "unknown date".
            write_manifest(out, args, chars, wanted, per_source,
                           len(collected), len(rejected), login_needed)
            if args.show_rating_breakdown:
                print_rating_breakdown(collected, rating_dropped)
            print(f"\n[vision-gate] {len(wl)} candidate(s) queued, "
                  f"0 downloaded")
            print(f"  worklist : {out / 'vision_worklist.json'}")
            print("  These rows have image URLs, no local files yet. Look at")
            print("  each one, judge it, then apply verdicts and download")
            print("  only the survivors:")
            print(f"    vision_filter.py --dataset {out} "
                  f"--apply verdicts.json --drop")
            print(f"    harvest.py --dataset {out} --download-only")
            if login_needed:
                return 2
            return 0 if collected else 3

        # ---- download ------------------------------------------------
        if args.dry_run:
            print("\n[dry-run] no files written")
            for r in collected:
                print(f"  {r['source']}:{r['source_id']}  {r['rating']:<12} {r['file_url'][:80]}")
            return 0 if collected else 3

        final = download_rows(collected, out, registry, ensure_browser,
                              args, rejected)

        # ---- merge with any existing rows, then write -----------------
        # Two harvests into the same --out is a normal way to build a
        # dataset (one query per ship, then another). Overwriting left
        # images on disk that no row referenced, so the manifest count
        # stopped matching the directory and the orphans became invisible
        # to publish, vision_filter and every trainer that reads the folder.
        out.mkdir(parents=True, exist_ok=True)
        existing = load_jsonl(out / "metadata.jsonl")
        if existing:
            prior = {record_key(r): r for r in existing}
            for r in final:
                # Keep a prior vision verdict: this run did not look at the
                # image, so it cannot improve on what was already judged.
                old = prior.get(record_key(r))
                if old and "vision" in old and "vision" not in r:
                    r["vision"] = old["vision"]
                    r["vision_pass"] = old.get("vision_pass")
            merged, _ = dedupe(final + existing)
            print(f"merged: {len(existing)} prior row(s) kept, "
                  f"{len(merged) - len(existing)} added "
                  f"-> {len(merged)} total")
            final = merged

        write_jsonl(out / "metadata.jsonl", final)
        if rejected:
            merge_rejected(out, rejected)

        write_manifest(out, args, chars, wanted, per_source,
                       len(final), len(rejected), login_needed)

        if args.show_rating_breakdown:
            print_rating_breakdown(
                final, [r for r in rejected
                        if str(r.get("reject_reason", "")).startswith("rating:")])

        print(f"\nwrote {len(final)} images + metadata.jsonl -> {out}")

        # Images from loosely-tagged sources have NOT been verified to
        # actually contain two women. Queue them for a vision pass.
        if args.vision:
            loose = [r for r in final if r.get("source") in LOOSE_TAGGING]
            if loose:
                wl = [{
                    "source": r["source"], "source_id": r["source_id"],
                    "image": str(out / r["file_name"]),
                    "page_url": r.get("page_url", ""),
                } for r in loose]
                (out / "vision_worklist.json").write_text(
                    json.dumps(wl, indent=2), encoding="utf-8")
                print(f"{len(wl)} image(s) from {sorted({r['source'] for r in loose})}"
                      f" need vision verification -> vision_worklist.json")
                print("  run: vision_filter.py --dataset "
                      f"{out} --backend worklist")
            else:
                print("no loosely-tagged sources in the result; nothing to verify")

        if login_needed:
            print(f"still needs a human login: {', '.join(login_needed)}")
            return 2
        return 0 if final else 3
    finally:
        if browser_cm is not None:
            try:
                browser_cm.__exit__(None, None, None)
            except Exception:                                 # noqa: BLE001
                pass


if __name__ == "__main__":
    raise SystemExit(main())
