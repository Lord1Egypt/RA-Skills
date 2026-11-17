#!/usr/bin/env python3
"""Check the captioned videos against each platform and plan the posts (WoopSocial requests).

    python3 scripts/post_plan.py post.json                  # check, schedule, write plan.md + requests/
    python3 scripts/post_plan.py post.json --media media.json   # fill in uploaded mediaIds

post.json (the agent writes it after the user has approved the captioned videos):
{
  "manifest": "captioned/manifest.json",
  "start": "2026-11-16",                  first day to post (each account's own time zone)
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "socialAccountId": "...", "output": "vertical",
     "language": "en", "timezone": "America/New_York", "times": ["18:00"], "days": ["mon","wed","fri"],
     "privacyLevel": "PUBLIC_TO_EVERYONE"},
    {"name": "Reels ES", "platform": "INSTAGRAM", "socialAccountId": "...", "output": "vertical", "language": "es"},
    {"name": "YouTube", "platform": "YOUTUBE", "socialAccountId": "...", "output": "youtube", "privacy": "public"}
  ],
  "posts": {
    "speed": {"en": {"text": "Post text...", "title": "YouTube title"}, "es": {"text": "..."}}
  },
  "order": ["speed", "intro"]               optional: which video goes out first
}
Every account gets each video once, in its language and output, one post a day at most.
Platforms: TIKTOK, INSTAGRAM, YOUTUBE, FACEBOOK, LINKEDIN, LINKEDIN_PAGES, X, THREADS, BLUESKY.
An account without a socialAccountId is planned anyway (connect WoopSocial, then run this again).
Writes plan.md and requests/captions/<video>.<account>.json next to post.json. media.json maps each
video file (as in plan.md) to the mediaId from WoopSocial's upload.
"""
import argparse, datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import die, guard, probe, read_json, rel, write_json  # noqa: E402

PLATFORMS = {  # documented API/app limits for a video post (seconds, bytes); text limits in characters
    "TIKTOK": {"min_s": 3, "max_s": 600, "bytes": 4 * 1024 ** 3, "text": 2200, "fps": (23, 60), "vertical": True},
    "INSTAGRAM": {"min_s": 3, "max_s": 15 * 60, "bytes": 300 * 1024 ** 2, "text": 2200, "fps": (23, 60), "vertical": True,
                  "hashtags": 5},
    "YOUTUBE": {"min_s": 1, "max_s": 12 * 3600, "bytes": 256 * 1024 ** 3, "text": 5000, "title": 100},
    "FACEBOOK": {"min_s": 1, "max_s": 4 * 3600, "bytes": 4 * 1024 ** 3, "text": 63206},
    "LINKEDIN": {"min_s": 3, "max_s": 15 * 60, "bytes": 5 * 1024 ** 3, "text": 3000},
    "LINKEDIN_PAGES": {"min_s": 3, "max_s": 15 * 60, "bytes": 5 * 1024 ** 3, "text": 3000},
    "X": {"min_s": 0.5, "max_s": 140, "bytes": 512 * 1024 ** 2, "text": 280},
    "THREADS": {"min_s": 0, "max_s": 300, "bytes": 1024 ** 3, "text": 500},
    "BLUESKY": {"min_s": 0, "max_s": 180, "bytes": 100 * 1024 ** 2, "text": 300},
}
# where a subtitle file can be added to a video that is already live (X and LinkedIn take one only
# while uploading in their own app, so there the burned-in captions do the job)
SRT_IN_APP = {"YOUTUBE": "YouTube Studio > Subtitles", "FACEBOOK": "the video's Captions settings in Meta Business Suite"}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
TIKTOK_PRIVACY = {"PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY"}
issues = []


def issue(level, where, msg):
    issues.append((level, where, msg))


def tzinfo(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        if name in ("UTC", "Etc/UTC"):
            return datetime.timezone.utc
        die(f"time zone '{name}' not found. Use a name like Europe/Amsterdam (Windows: pip install tzdata)")


def check_video(acc, m, path, text, title):
    """Platform checks for one post. Returns (kind shown in the plan, Facebook reel or not)."""
    p = acc["platform"]
    kind, reel = None, False
    L = PLATFORMS[p]
    where = f"{m['video']} -> {acc['name']}"
    info = probe(path)
    s, b = info["duration"], info["bytes"]
    if s < L["min_s"]:
        issue("error", where, f"{s:.1f} s is shorter than {p}'s minimum of {L['min_s']} s")
    if s > L["max_s"]:
        issue("error", where, f"{s:.0f} s is over {p}'s {L['max_s']:.0f} s limit")
    if b > L["bytes"]:
        issue("error", where, f"{b / 1024 ** 2:.0f} MB is over {p}'s {L['bytes'] / 1024 ** 2:.0f} MB limit")
    fps = L.get("fps")
    if fps and not fps[0] <= info["fps"] <= fps[1] + 0.5:
        issue("error", where, f"{info['fps']} fps; {p} accepts {fps[0]} to {fps[1]}")
    if info["vcodec"] != "h264":
        issue("warning", where, f"video codec {info['vcodec']}; H.264 is the safe choice everywhere")
    vertical = info["height"] > info["width"] * 1.5
    if L.get("vertical") and not vertical:
        issue("warning", where, f"{info['width']}x{info['height']} isn't 9:16; {p} shows it smaller with bars. "
              "Use the vertical output")
    if p == "YOUTUBE":
        short = s <= 180 and info["height"] >= info["width"]
        if not title:
            issue("error", where, "YouTube needs a title (posts.<video>.<lang>.title)")
        elif len(title) > L["title"]:
            issue("error", where, f"title is {len(title)} characters; YouTube allows {L['title']}")
        kind = "Short" if short else "video"
    if p == "FACEBOOK":
        reel = vertical and 3 <= s <= 90
        kind = "Reel" if reel else "video"
    if not text.strip() and p not in ("YOUTUBE",):
        issue("warning", where, "no post text; the post text is what search reads, so say what the video is about")
    if len(text) > L["text"]:
        issue("error", where, f"post text is {len(text)} characters; {p} allows {L['text']}")
    tags = re.findall(r"(?<![\w&])#\w+", text)
    if L.get("hashtags") and len(tags) > L["hashtags"]:
        issue("error", where, f"{len(tags)} hashtags; {p} allows {L['hashtags']}")
    elif len(tags) > 5:
        issue("warning", where, f"{len(tags)} hashtags; 3 to 5 specific ones read better")
    return kind, reel


def body(acc, text, title, media_id, when, reel):
    p = acc["platform"]
    target = {"platform": p, "socialAccountId": acc.get("socialAccountId") or "<connect this account>"}
    if p == "TIKTOK":
        target.update(postType="VIDEO", postMode="DIRECT_POST", privacyLevel=acc.get("privacyLevel"),
                      allowComment=acc.get("allowComment", True), allowDuet=acc.get("allowDuet", True),
                      allowStitch=acc.get("allowStitch", True), isYourBrand=bool(acc.get("isYourBrand", False)),
                      isBrandedContent=bool(acc.get("isBrandedContent", False)), autoAddMusic=False,
                      isAiGeneratedContent=bool(acc.get("isAiGeneratedContent", False)))
    elif p == "INSTAGRAM":
        target.update(postType="REEL", isAiGeneratedContent=bool(acc.get("isAiGeneratedContent", False)))
    elif p == "YOUTUBE":
        target.update(title=title or "", privacy=acc.get("privacy", "public"),
                      madeForKids=acc.get("madeForKids") is True)
        if acc.get("category"):
            target["category"] = str(acc["category"])
    elif p == "FACEBOOK":
        target.update(postType="REEL" if reel else "VIDEO")
    return {"content": [{"text": text, "media": [{"type": "MEDIA_LIBRARY", "mediaId": media_id}]}],
            "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": when},
            "socialAccounts": [target], "autoDeleteMediaAfterPublish": False}


def slots(acc, start, n):
    tz = tzinfo(acc.get("timezone", "UTC"))
    days = acc.get("days", DAYS)
    if not isinstance(days, list) or not all(isinstance(d, str) for d in days):
        die(f"account {acc['name']}: days must be like [\"mon\", \"wed\", \"fri\"]")
    days = [d.lower()[:3] for d in days]
    if not days or any(d not in DAYS for d in days):
        die(f"account {acc['name']}: days must be like [\"mon\", \"wed\", \"fri\"]")
    times = acc.get("times", ["18:00"])
    if not isinstance(times, list) or not times or not all(
            re.match(r"^([01]?\d|2[0-3]):[0-5]\d$", str(t)) for t in times):
        die(f"account {acc['name']}: times must be 24-hour times like [\"18:00\"]")
    out, d, k = [], start, 0
    now = datetime.datetime.now(datetime.timezone.utc)
    while len(out) < n and k < 400:
        if DAYS[d.weekday()] in days:
            hh, mm = map(int, times[len(out) % len(times)].split(":"))
            local = datetime.datetime(d.year, d.month, d.day, hh, mm, tzinfo=tz)
            utc = local.astimezone(datetime.timezone.utc)
            if utc > now + datetime.timedelta(minutes=15):
                out.append((local, utc))
        d += datetime.timedelta(days=1)
        k += 1
    return out


def main():
    ap = argparse.ArgumentParser(description="Plan the posts for the captioned videos.")
    ap.add_argument("plan")
    ap.add_argument("--media", help="media.json: {video file: mediaId} after uploading")
    a = ap.parse_args()
    plan = read_json(a.plan)
    if not isinstance(plan, dict):
        die(f"{a.plan}: post.json must be a JSON object (see the top of this script)")
    base = os.path.dirname(os.path.abspath(a.plan))
    if not isinstance(plan.get("manifest", ""), str):
        die("'manifest' must be the path to captioned/manifest.json")
    man_path = os.path.join(base, plan.get("manifest") or "captioned/manifest.json")
    if not os.path.exists(man_path):
        die(f"{rel(man_path)} not found; run render.py first")
    man = read_json(man_path)
    files = man.get("files", []) if isinstance(man, dict) else []
    if not isinstance(files, list) or not all(isinstance(m, dict) and all(isinstance(m.get(k), str) for k in
                                               ("video", "output", "language", "file", "srt", "style"))
                                               for m in files):
        die(f"{rel(man_path)} is damaged (render.py writes it). Run render.py again to rebuild it.")
    man_base = os.path.dirname(os.path.abspath(man_path))
    if not files:
        die(f"{rel(man_path)} lists no videos; run render.py first")
    media = read_json(os.path.join(base, a.media)) if a.media else {}
    if not isinstance(media, dict) or not all(isinstance(x, str) for x in media.values()):
        die(f"{a.media}: must map each video file to its mediaId, like {{\"captioned/a/a.vertical.en.mp4\": \"123\"}}")
    try:
        start = datetime.date.fromisoformat(str(plan.get("start") or datetime.date.today().isoformat()))
    except ValueError:
        die("start must be a date like 2026-11-16")
    accounts = plan.get("accounts")
    if not isinstance(accounts, list) or not accounts:
        die("post.json needs at least one account")
    posts = plan.get("posts") or {}
    if not isinstance(posts, dict) or not all(isinstance(x, dict) for x in posts.values()):
        die("'posts' must be like {\"speed\": {\"en\": {\"text\": \"...\"}}}")
    for vid, by_lang in posts.items():
        for lang, w in by_lang.items():
            if not isinstance(w, dict) or not isinstance(w.get("text", ""), str) \
                    or not isinstance(w.get("title", ""), (str, type(None))):
                die(f"posts.{vid}.{lang} must be {{\"text\": \"...\", \"title\": \"...\"}}")
    videos = plan.get("order") or sorted({m["video"] for m in files})
    if not isinstance(videos, list) or not all(isinstance(x, str) for x in videos):
        die("'order' must be a list of video ids")
    unknown = set(videos) - {m["video"] for m in files}
    if unknown:
        die(f"'order' names video(s) not in the manifest: {', '.join(sorted(unknown))}")
    req_dir = os.path.join(base, "requests", "captions")
    os.makedirs(req_dir, exist_ok=True)
    for f in os.listdir(req_dir):  # this folder is ours: requests from an older plan go
        if f.endswith(".json"):
            os.remove(os.path.join(req_dir, f))
    written, requests = set(), {}
    rows, uploads, srt_notes, unconnected = [], {}, [], []
    seen_names, by_platform = set(), {}
    for acc in accounts:
        if not isinstance(acc, dict) or acc.get("platform") not in PLATFORMS:
            die(f"each account needs a platform: {', '.join(PLATFORMS)}")
        acc.setdefault("name", acc["platform"].title())
        for k in ("name", "socialAccountId", "output", "language", "timezone", "privacyLevel", "privacy"):
            if acc.get(k) is not None and not isinstance(acc[k], str):
                die(f"account {acc.get('name')}: '{k}' must be text")
        if acc["name"] in seen_names:
            die(f"two accounts are named '{acc['name']}'")
        seen_names.add(acc["name"])
        if not acc.get("socialAccountId"):
            unconnected.append(acc["name"])
        # choices only the user can make: an error once the account is connected, a reminder before
        level = "error" if acc.get("socialAccountId") else "warning"
        if acc["platform"] == "TIKTOK" and acc.get("privacyLevel") not in TIKTOK_PRIVACY:
            issue(level, acc["name"], "choose who can see these TikTok posts (everyone, friends, followers or "
                  "only you); the agent never picks it (privacyLevel)")
        if acc["platform"] == "YOUTUBE" and not isinstance(acc.get("madeForKids"), bool):
            issue(level, acc["name"], "say whether these videos are made for kids (a legal setting; the agent "
                  "never picks it; madeForKids)")
        if acc["platform"] == "YOUTUBE" and acc.get("privacy", "public") not in ("public", "unlisted", "private"):
            die(f"account {acc['name']}: privacy must be public, unlisted or private")
        if acc.get("category") is not None and not str(acc["category"]).isdigit():
            die(f"account {acc['name']}: category is a YouTube category number, like \"28\"")
        for k in ("allowComment", "allowDuet", "allowStitch", "isYourBrand", "isBrandedContent",
                  "isAiGeneratedContent", "madeForKids"):
            if acc.get(k) is not None and not isinstance(acc[k], bool):
                die(f"account {acc['name']}: {k} is true or false")
        key = (acc["platform"], acc.get("language"), acc.get("output"))
        if key in by_platform:
            issue("warning", acc["name"], f"posts the same videos as {by_platform[key]} on the same platform in the "
                  "same language; to the platform that looks like reposting. Give it another language or output")
        by_platform[key] = acc["name"]
        mine = []
        for vid in videos:
            cands = [m for m in files if m["video"] == vid and m["output"] == acc.get("output", m["output"])]
            lang = acc.get("language")
            pick = next((m for m in cands if lang and m["language"] == lang), None) or \
                next((m for m in cands if not lang), None)
            if not pick:
                issue("warning", acc["name"], f"no '{acc.get('output', 'any')}' video in '{lang or 'any'}' for {vid}; skipped")
                continue
            mine.append(pick)
        when = slots(acc, start, len(mine))
        if len(when) < len(mine):
            die(f"account {acc['name']}: no future posting days found")
        for m, (local, utc) in zip(mine, when):
            path = os.path.normpath(os.path.join(man_base, m["file"]))
            if not os.path.exists(path):
                die(f"{m['file']} not found; run render.py again")
            words = (posts.get(m["video"]) or {}).get(m["language"]) or {}
            text, title = str(words.get("text", "")), words.get("title")
            kind, reel = check_video(acc, m, path, text, title)
            key = rel(path, base)
            mid = media.get(key) or f"<mediaId of {key}>"
            uploads[key] = os.path.getsize(path)
            req = body(acc, text, title, mid, utc.strftime("%Y-%m-%dT%H:%M:%SZ"), reel)
            slug = re.sub(r'[^A-Za-z0-9]+', '-', acc['name']).strip('-').lower() or "account"
            name = f"{m['video']}.{slug}.json"
            if name in written:
                die(f"two accounts' names both become '{slug}'; give them more different names")
            written.add(name)
            requests[name] = req
            shown = title if acc["platform"] == "YOUTUBE" and title else text.split("\n")[0]
            rows.append((local, acc, m, key, name, shown[:70] + ("..." if len(shown) > 70 else ""), kind, text, title))
            if acc["platform"] in SRT_IN_APP:
                srt = os.path.normpath(os.path.join(man_base, m["srt"]))
                srt_notes.append(f"- {m['video']} on {acc['name']}: add `{rel(srt, base)}` in {SRT_IN_APP[acc['platform']]} "
                                 "after it's live (closed captions viewers can switch on; WoopSocial posts the video only)")
    rows.sort(key=lambda r: (r[0].astimezone(datetime.timezone.utc), r[1]["name"]))
    errors = [i for i in issues if i[0] == "error"]
    if not errors:  # with errors, no request files: nothing half-decided can be sent
        for name, req in requests.items():
            write_json(os.path.join(req_dir, name), req)
    lines = ["# Posting plan", "",
             f"{len(rows)} posts to {len(accounts)} accounts, from {start.isoformat()}. Nothing is posted until you say yes.", "",
             "| When (account's time) | Account | File | Text |", "|---|---|---|---|"]
    for local, acc, m, key, name, first, kind, text, title in rows:
        k = f" ({kind})" if kind else ""
        lines.append(f"| {local.strftime('%a %d %b %H:%M')} {local.tzname()} | {acc['name']}{k} | "
                     f"`{os.path.basename(key)}` | {first.replace('|', '/')} |")
    lines += ["", "## Post texts", ""]
    done = set()
    for local, acc, m, key, name, first, kind, text, title in rows:
        if (m["video"], m["language"]) in done:
            continue
        done.add((m["video"], m["language"]))
        lines += [f"**{m['video']} ({m['language']})**" + (f": {title}" if title else ""), "",
                  "> " + (text.strip() or "(no text yet)").replace("\n", "\n> "), ""]
    lines += ["", "## Files", ""]
    lines += [f"- `{k}` ({b / 1024 ** 2:.1f} MB)" for k, b in sorted(uploads.items())]
    if srt_notes:
        lines += ["", "## Subtitle files to add in the apps", ""] + srt_notes
    if issues:
        lines += ["", "## Checks", ""] + [f"- {lv.upper()} {w}: {msg}" for lv, w, msg in issues]
    if unconnected:
        ig = [x["name"] for x in accounts if x["platform"] == "INSTAGRAM" and not x.get("socialAccountId")]
        lines += ["", "## Not connected yet", "",
                  f"{', '.join(unconnected)}. To have your agent schedule this plan, connect these accounts to "
                  "WoopSocial once and say \"schedule plan.md\". To post by hand instead, every file, text and "
                  "time is above."]
        if ig:
            lines += ["", f"{', '.join(ig)}: Instagram posting needs a Business or Creator account (free to "
                          "switch in the Instagram app)."]
    with open(os.path.join(base, "plan.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    for lv, w, msg in issues:
        print(f"{lv}: {w}: {msg}", file=sys.stderr)
    print(f"{len(rows)} posts planned -> {rel(os.path.join(base, 'plan.md'))}, requests/captions/ "
          f"({len(errors)} errors, {len(issues) - len(errors)} warnings)")
    if unconnected:
        print(f"not connected yet: {', '.join(unconnected)}")
    if errors:
        print("no requests written until the errors above are fixed")
    elif unconnected:
        print("next: connect the accounts above, add their socialAccountIds to post.json, run this again")
    elif any("<mediaId" in json.dumps(r) for r in requests.values()):
        print("next: upload each file in plan.md, save {file: mediaId} as media.json, run with --media media.json")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    guard(main)
