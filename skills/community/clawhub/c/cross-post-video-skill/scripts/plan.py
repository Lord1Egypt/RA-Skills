#!/usr/bin/env python3
"""Check a cross-post job and write the plan: every account, text, setting and time on one page.

    python3 scripts/plan.py crosspost.json                      # check everything, write plan.md, plan.html,
                                                                #   requests/ and by-hand/
    python3 scripts/plan.py crosspost.json --media media.json   # fill in the uploaded mediaIds
    python3 scripts/plan.py crosspost.json --posted requests/launch.json <postId>   # record a sent post
    python3 scripts/plan.py crosspost.json --failed launch "TikTok"     # an account whose post failed:
                                                                #   the next plan sends it again
    python3 scripts/plan.py crosspost.json --posted-by-hand launch "Shorts"   # the user posted it by hand

crosspost.json is described in references/job-file.md. In short: "accounts" (where the video goes,
with the settings only the user can choose), and "videos" (the file, the cover, when, the user's
answers about the video, and one text per platform).

What it writes, next to crosspost.json:
  plan.md, plan.html   every post as it will go out, with every check. Show this before posting.
  requests/*.json      one WoopSocial request per video and time: one post with a child per account,
                       each with its own text. Only written when there are no errors.
  by-hand/<video>/     for accounts that aren't connected: the text and the steps to post in the app;
                       for a TikTok draft: the caption to paste and the steps to finish it.
  posted.json          which video went to which account, so no account gets the same video twice.
Every run starts by removing the plan, the requests and the by-hand pages of the run before, so a
plan that stops on an error never leaves an old request that could still be sent.
--media is looked for in the folder you run from first, then next to crosspost.json.
Works without WoopSocial: every account without a socialAccountId is planned as "by hand".
Exit code 0 when there are no errors, 1 otherwise.
"""
import argparse, base64, copy, datetime, hashlib, html, json, math, os, re, sys, urllib.parse

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xplib import (LIMITS, MB, SHORT_FORM, TIKTOK_PRIVACY, die, file_issues, file_kind, guard, hashtags,  # noqa: E402
                   jpeg_size, links, mentions, probe, read_json, reading, rel, same_file, slug, tags_length,
                   text_length, valid_id, write_json, write_text)

AUDIO = ("original", "licensed", "app_sound")
PROMO = ("no", "own_brand", "paid_partnership")
GENERIC_TAGS = {"#fyp", "#foryou", "#foryoupage", "#viral", "#fy", "#trending", "#explore", "#explorepage"}
PRIVACY_WORDS = {"PUBLIC_TO_EVERYONE": "everyone", "MUTUAL_FOLLOW_FRIENDS": "friends",
                 "FOLLOWER_OF_CREATOR": "followers", "SELF_ONLY": "only you"}
DEFAULT_KEYS = ("when", "own_video", "audio", "ai_generated", "promotional", "tiktok_draft")
DRAFT_LEAD = datetime.timedelta(hours=2)   # a TikTok draft lands at its scheduled time: 2 hours before the post
YT_CATEGORIES = {"1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music", "15": "Pets & Animals",
                 "17": "Sports", "19": "Travel & Events", "20": "Gaming", "22": "People & Blogs", "23": "Comedy",
                 "24": "Entertainment", "25": "News & Politics", "26": "Howto & Style", "27": "Education",
                 "28": "Science & Technology", "29": "Nonprofits & Activism"}
issues = []   # (level, where, message)
missing = []  # (where, question): answers only the user can give that the job doesn't have yet


def issue(level, where, msg):
    if (level, where, msg) not in issues:
        issues.append((level, where, msg))


def shown_now():
    """The moment the plan page counts from: its "Planned ..." line and every "(in N days)". The
    CROSSPOST_NOW environment variable (an ISO date and time) fixes it, so a page made for an example
    or a test reads the same on every day. Nothing else reads it: the checks always use the real clock."""
    fixed = os.environ.get("CROSSPOST_NOW", "").strip()
    if not fixed:
        return datetime.datetime.now(datetime.timezone.utc)
    try:
        t = datetime.datetime.fromisoformat(fixed.replace("Z", "+00:00"))
    except ValueError:
        die("CROSSPOST_NOW must be a date and time like 2026-11-12T12:00:00+01:00")
    return (t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)).astimezone(datetime.timezone.utc)


def local_text(t, zone):
    """'Fri 20 Nov 2026, 18:00 CET' in the job's time zone (the computer's own when the job has none)."""
    local = t.astimezone(tzinfo(zone)) if zone else t.astimezone()
    return local.strftime("%a %d %b %Y, %H:%M ") + (local.tzname() or "")


def file_print(path):
    """(sha256, size) of a video: what posted.json keeps, so a new file under an old id is caught."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest(), os.path.getsize(path)


def tzinfo(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        if name in ("UTC", "Etc/UTC"):
            return datetime.timezone.utc
        die(f"time zone '{name}' not found. Use a name like Europe/Amsterdam or America/New_York, spelled "
            "with these capitals (Windows: pip install tzdata)")


def check_when(video, accounts, targets):
    """The shape of "when", before any account is planned: a wrong key or a missing time is an
    error here, never a quiet "now"."""
    w = video.get("when", "now")
    if isinstance(w, dict):
        known = [a["name"] for a in accounts]
        known += [p for p in sorted({a["platform"] for a in accounts}) if p not in known] + ["default"]
        bad = [k for k in w if k not in known]
        if bad:
            die(f"video {video['id']}: \"when\" has \"{bad[0]}\", which is not an account name or a platform in "
                f"this job. Use one of: {', '.join(known)}")
        for acc in targets:
            if not any(k in w for k in (acc["name"], acc["platform"], "default")):
                die(f"video {video['id']}: \"when\" gives no time for {acc['name']}. Add \"{acc['name']}\" or "
                    "\"default\" to it, with \"now\" or a time")
    elif not isinstance(w, str) or not w.strip():
        die(f"video {video['id']}: 'when' must be \"now\" or a time like \"2026-11-20 18:00\"")


def when_for(video, acc, default_tz, check_past=True):
    """(local time or None for now, utc text or None)."""
    w = video.get("when", "now")
    if isinstance(w, dict):
        w = w.get(acc["name"], w.get(acc["platform"], w.get("default")))
    if not isinstance(w, str) or not w.strip():
        die(f"video {video['id']}: 'when' must be \"now\" or a time like \"2026-11-20 18:00\"")
    if w.strip().lower() == "now":
        return None, None
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[ T](\d{1,2}):(\d{2})$", w.strip())
    if not m:
        die(f"video {video['id']}: time '{w}' must look like \"2026-11-20 18:00\" (24-hour), or \"now\"")
    zone = acc.get("timezone") or default_tz
    if not zone:
        die(f"video {video['id']}: the time '{w}' needs a time zone. Add \"timezone\" to the job with the "
            "user's own zone as an IANA name, like \"Europe/Amsterdam\" or \"America/New_York\"")
    tz = tzinfo(zone)
    try:
        day = datetime.date.fromisoformat(m.group(1))
        local = datetime.datetime(day.year, day.month, day.day, int(m.group(2)), int(m.group(3)), tzinfo=tz)
        utc = local.astimezone(datetime.timezone.utc)
        back = utc.astimezone(tz)
        now = datetime.datetime.now(datetime.timezone.utc)
    except (ValueError, OverflowError):
        die(f"video {video['id']}: '{w}' is not a real date and time")
    where = f"{video['id']} -> {acc['name']}"
    if (back.hour, back.minute) != (local.hour, local.minute):
        issue("error", where, f"{w} doesn't exist in {zone}: the clocks go forward over it that night. Pick "
              "another time")
    elif check_past and utc < now + datetime.timedelta(minutes=5):
        issue("error", where, f"{w} is in the past or less than 5 minutes away; pick a later time, or \"now\"")
    return local, utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def text_for(video, acc):
    """The words for one account: {'text', 'title', 'tags', 'link'}. Account name wins over platform."""
    t = video.get("text") or {}
    raw = t.get(acc["name"], t.get(acc["platform"]))
    where = f"{video['id']} -> {acc['name']}"
    out = {"text": "", "title": None, "tags": [], "link": None}
    if raw is None:
        issue("error", where, f"no text for this account. Add text.{acc['platform']} (or text.\"{acc['name']}\") "
              "to the video")
        return out
    if isinstance(raw, str):
        out["text"] = raw
    elif isinstance(raw, dict):
        body = raw.get("description", raw.get("text", ""))
        if not isinstance(body, str) or not isinstance(raw.get("title", ""), (str, type(None))):
            die(f"{where}: title and description must be text")
        out["text"], out["title"] = body, raw.get("title")
        tags = raw.get("tags") or []
        if not isinstance(tags, list) or not all(isinstance(x, str) for x in tags):
            die(f"{where}: tags must be a list of words, like [\"nasa\", \"space station\"]")
        out["tags"] = [x.strip() for x in tags if x.strip()]
        if raw.get("link") is not None and not isinstance(raw["link"], str):
            die(f"{where}: link must be text")
        out["link"] = raw.get("link")
    else:
        die(f"{where}: text must be a string, or {{\"title\": ..., \"description\": ...}} for YouTube and Pinterest")
    return out


def check_text(video, acc, words):
    p = acc["platform"]
    L = LIMITS[p]
    where = f"{video['id']} -> {acc['name']}"
    text, title = words["text"], words["title"]
    if p in ("YOUTUBE", "PINTEREST"):
        if not (title or "").strip():
            issue("error", where, f"{L['label']} needs a title")
        elif len(title) > L["title"]:
            issue("error", where, f"title is {len(title)} characters; {L['label']} allows {L['title']}")
        if p == "YOUTUBE" and re.search(r"[<>]", (title or "") + text):
            issue("error", where, "YouTube rejects < and > in the title and description; remove them")
    elif title:
        issue("warning", where, f"{L['label']} has no title; only the text is used")
    n, approx = text_length(p, text)
    if p == "YOUTUBE":
        if n > L["text_bytes"]:
            issue("error", where, f"description is {n} bytes; YouTube allows {L['text_bytes']} (emoji and "
                  "non-Latin letters count as 2 to 4 each)")
        tn = tags_length(words["tags"])
        if tn > L["tags_chars"]:
            issue("error", where, f"tags add up to {tn} characters the way YouTube counts them (a comma between "
                  f"tags, and 2 more for every tag with a space); YouTube allows {L['tags_chars']}")
    else:
        if n > L["text"] and approx:
            issue("warning", where, f"text is about {n} characters the way {L['label']} counts, and it allows "
                  f"{L['text']}. The count is approximate for joined emoji and accented scripts: shorten the "
                  "text, or check it in the app before posting")
        elif n > L["text"]:
            how = {"X": " (X counts every link as 23 and wide characters and emoji as 2)",
                   "TIKTOK": " (most emoji count as 2)"}.get(p, "")
            issue("error", where, f"text is {n} characters{how}; {L['label']} allows {L['text']}")
        if words["tags"]:
            issue("warning", where, f"{L['label']} has no hidden tags; put hashtags in the text instead")
    if not text.strip() and p != "YOUTUBE":
        issue("warning", where, "no text. The text is what search reads: say what the video is about")
    tags = hashtags(text) + (hashtags(title) if title else [])
    if L.get("tags_max") and len(tags) > L["tags_max"]:
        issue("error", where, f"{len(tags)} hashtags; Instagram allows {L['tags_max']} per post")
    elif L.get("tags_ignored") and len(tags) > L["tags_ignored"]:
        issue("error", where, f"{len(tags)} hashtags; above {L['tags_ignored']} YouTube ignores every one of them")
    elif len(tags) > L.get("tags_warn", 5):
        issue("warning", where, f"{len(tags)} hashtags; Instagram advises fewer, more specific ones, and the "
              "TikTok app reports a limit of 5")
    generic = sorted({t.lower() for t in tags} & GENERIC_TAGS)
    if generic:
        issue("warning", where, f"{', '.join(generic)} says nothing about the video; use hashtags that name the topic")
    if p == "YOUTUBE" and any(t.lower() == "#shorts" for t in tags):
        issue("note", where, "#Shorts isn't needed: YouTube decides by length and shape")
    if L.get("mentions") and len(mentions(text)) > L["mentions"]:
        issue("error", where, f"{len(mentions(text))} @mentions; Instagram allows {L['mentions']}")
    if p in ("TIKTOK", "INSTAGRAM", "YOUTUBE") and links(text):
        link = links(text)[0]
        issue("warning", where, f"links can't be clicked in {L['label']} text ({link[:60]}{'...' if len(link) > 60 else ''}); "
              "put the link on the profile and point to it")
    if p in SHORT_FORM and text.strip():
        first = text.strip().split("\n")[0]
        if len(first) > 150:
            issue("warning", where, f"the first line is {len(first)} characters. Only the start shows before "
                  "\"more\", so make the first line short enough to stand on its own")


def placeholder_id(sid):
    """True for a made-up id copied from an example ("<id>", "id", "your-tiktok-account-id")."""
    low = sid.lower()
    return "<" in sid or ">" in sid or low == "id" or low.startswith(("your-", "your_")) or bool(re.search(r"\s", sid))


def ask(level, where, msg):
    """A question only the user can answer. Counted, so the run can say how many are still open."""
    if (where, msg) not in missing:
        missing.append((where, msg))
    issue(level, where, msg)


def check_account(acc, n, draft_only=False):
    if not isinstance(acc, dict):
        die(f"account {n + 1} must be an object like {{\"name\": \"TikTok\", \"platform\": \"TIKTOK\"}}")
    p = acc.get("platform")
    if not isinstance(p, str) or p.strip().upper() not in LIMITS:
        die(f"account {n + 1}: platform must be one of {', '.join(LIMITS)}")
    p = acc["platform"] = p.strip().upper()
    if acc.get("name") is None:
        acc["name"] = LIMITS[p]["label"]
    for k in ("name", "socialAccountId", "timezone", "privacyLevel", "privacy", "pinterestBoardId", "trial",
              "handle", "audience"):
        if acc.get(k) is not None and not isinstance(acc[k], str):
            die(f"account {n + 1}: '{k}' must be text")
    if not acc["name"].strip() or acc["name"] != acc["name"].strip():
        die(f"account {n + 1}: the name can't be empty or start or end with a space")
    sid = acc.get("socialAccountId")
    if sid is not None and (not sid.strip() or sid != sid.strip()):
        die(f"account {acc['name']}: socialAccountId is blank or has a space or line break around it. Copy it "
            "from social_accounts_list, or leave it out for an account that isn't connected")
    if sid is not None and placeholder_id(sid):
        die(f"account {acc['name']}: \"{sid[:40]}\" is the example's placeholder; use the id from "
            "social_accounts_list or leave it out to plan this account by hand")
    handle = (acc.get("handle") or "").strip().lstrip("@")
    acc["handle"] = "@" + handle if handle else None
    acc["audience"] = (acc.get("audience") or "").strip() or None
    if acc.get("timezone"):
        tzinfo(acc["timezone"])
    for k in ("allowComment", "allowDuet", "allowStitch", "madeForKids"):
        if acc.get(k) is not None and not isinstance(acc[k], bool):
            die(f"account {acc['name']}: {k} is true or false")
    connected = bool(acc.get("socialAccountId"))
    level = "error" if connected else "warning"
    name = acc["name"]
    if p == "TIKTOK":
        opts = acc.get("privacyOptions")
        if opts is not None and (not isinstance(opts, list) or not all(o in TIKTOK_PRIVACY for o in opts)):
            die(f"account {name}: privacyOptions must be the list from social_accounts_get_platform_inputs")
        if acc.get("privacyLevel") not in TIKTOK_PRIVACY:
            if not (draft_only and connected):   # a draft's audience is picked in the TikTok app
                ask(level, name, "who can see these TikTok posts? TikTok requires the account owner to choose "
                    "(everyone, friends, followers or only you); nobody else picks it (privacyLevel)")
        elif opts and acc["privacyLevel"] not in opts:
            issue("error", name, f"this TikTok account doesn't offer '{PRIVACY_WORDS[acc['privacyLevel']]}'; "
                  f"it offers: {', '.join(PRIVACY_WORDS[o] for o in opts)}")
        gone = [k for k in ("allowComment", "allowDuet", "allowStitch") if not isinstance(acc.get(k), bool)]
        if gone:
            ask(level, name, "allow comments, duets and stitches? TikTok requires the account owner to choose "
                f"each one ({', '.join(gone)})")
        mx = acc.get("max_video_s")
        if mx is not None and (isinstance(mx, bool) or not isinstance(mx, (int, float)) or not math.isfinite(mx)
                               or mx <= 0):
            die(f"account {name}: max_video_s is a number of seconds above 0, like 600")
        if connected and not acc.get("max_video_s"):
            issue("note", name, "this account's own maximum video length wasn't read (max_video_s from "
                  "social_accounts_get_platform_inputs); TikTok sets it per account")
    if p == "YOUTUBE":
        if acc.get("privacy") not in ("public", "unlisted", "private"):
            ask(level, name, "should the YouTube video be public, unlisted or private? (privacy)")
        if not isinstance(acc.get("madeForKids"), bool):
            ask(level, name, "is the video made for kids? YouTube requires the channel owner to say so "
                "(a legal declaration; madeForKids true or false)")
        if acc.get("category") is not None and not re.fullmatch(r"[0-9]{1,3}", str(acc["category"])):
            die(f"account {name}: category is a YouTube category number as text, like \"28\"")
    if p == "INSTAGRAM" and acc.get("trial") not in (None, "MANUAL", "SS_PERFORMANCE"):
        die(f"account {name}: trial is \"MANUAL\" or \"SS_PERFORMANCE\" (a Trial Reel), or leave it out")
    if p == "PINTEREST" and connected and not acc.get("pinterestBoardId"):
        issue("error", name, "which Pinterest board? (pinterestBoardId from social_accounts_get_platform_inputs)")
    return acc


def check_video_answers(video, connected):
    level = "error" if connected else "warning"
    vid = video["id"]
    if not isinstance(video.get("own_video"), bool):
        ask(level, vid, "is this the original export (not a copy saved from an app), and does the user have the "
            "right to post it? (own_video true or false)")
    elif video["own_video"] is False:
        issue("error", vid, "this file is a copy saved from an app or from someone else's post, or the user has "
              "no right to post it. Use the original export of a video the user made or may post (their own, a "
              "client's, licensed): a saved copy carries the app's watermark and is compressed twice, and "
              "Instagram says it doesn't recommend videos with a visible watermark")
    if video.get("audio") not in AUDIO:
        ask(level, vid, "what is the sound: \"original\" (own voice or own recording), \"licensed\" (music "
            "the user has a licence for on every platform) or \"app_sound\" (a sound picked inside an app)? (audio)")
    if not isinstance(video.get("ai_generated"), bool):
        ask(level, vid, "does the video show realistic AI-generated people, scenes or voices? The platforms "
            "require a label when it does (ai_generated true or false)")
    if video.get("promotional") not in PROMO:
        ask(level, vid, "does the video promote something: \"no\", \"own_brand\" (the user's own business) or "
            "\"paid_partnership\" (paid by someone else)? TikTok requires the answer (promotional)")


def answers_line(video):
    """The four answers, in words, shown once per video on the plan and on every by-hand page."""
    def yn(v):
        return ("yes" if v else "no") if isinstance(v, bool) else "NOT ANSWERED"
    sound = {"original": "your own recording", "licensed": "music you have a licence for",
             "app_sound": "a sound picked inside an app"}.get(video.get("audio"), "NOT ANSWERED")
    promo = {"no": "no", "own_brand": "your own brand", "paid_partnership": "a paid partnership"}.get(
        video.get("promotional"), "NOT ANSWERED")
    return (f"Original export, with the right to post it: {yn(video.get('own_video'))}. Sound: {sound}. "
            f"AI-made: {yn(video.get('ai_generated'))}. Promotion: {promo}.")


def body_for(acc, words, video_media, cover_media, video, info):
    p = acc["platform"]
    t = {"platform": p, "socialAccountId": acc["socialAccountId"]}
    if p == "TIKTOK":
        draft = video.get("tiktok_draft") is True
        # A draft (MEDIA_UPLOAD) goes to the account's TikTok inbox. The user picks the audience and the
        # sound in the app, so privacyLevel is left out. autoAddMusic is required by WoopSocial's schema
        # for every TikTok child (TikTok only uses it on photo posts), so it is always sent as false.
        t.update(postType="VIDEO", postMode="MEDIA_UPLOAD" if draft else "DIRECT_POST")
        if not draft:
            t["privacyLevel"] = acc.get("privacyLevel")
        t.update(allowComment=bool(acc.get("allowComment")), allowDuet=bool(acc.get("allowDuet")),
                 allowStitch=bool(acc.get("allowStitch")),
                 isYourBrand=video.get("promotional") == "own_brand",
                 isBrandedContent=video.get("promotional") == "paid_partnership")
        t["autoAddMusic"] = False
        t["isAiGeneratedContent"] = video.get("ai_generated") is True
    elif p == "INSTAGRAM":
        t.update(postType="REEL", isAiGeneratedContent=video.get("ai_generated") is True)
        if acc.get("trial"):
            t["trialParams"] = {"graduationStrategy": acc["trial"]}
    elif p == "YOUTUBE":
        t.update(title=words["title"] or "", privacy=acc.get("privacy"), madeForKids=acc.get("madeForKids") is True)
        if words["tags"]:
            t["tags"] = words["tags"]
        if acc.get("category"):
            t["category"] = str(acc["category"])
    elif p == "FACEBOOK":
        t.update(postType="REEL" if facebook_reel(info) else "VIDEO")
    elif p == "PINTEREST":
        t.update(pinterestBoardId=acc.get("pinterestBoardId"), title=words["title"] or "")
        if words["link"]:
            t["link"] = words["link"]
    if cover_media and p in ("TIKTOK", "INSTAGRAM"):
        t["cover"] = {"type": "MEDIA_LIBRARY", "mediaId": cover_media}
    t["contentOverride"] = [{"text": words["text"], "media": [{"type": "MEDIA_LIBRARY", "mediaId": video_media}]}]
    return t


def facebook_reel(info):
    return info["height"] > info["width"] and 3 <= info["duration"] <= 90


def is_draft(acc, video):
    """A TikTok draft: sent to the account's TikTok inbox, finished by the user in the app."""
    return acc["platform"] == "TIKTOK" and bool(acc.get("socialAccountId")) and video.get("tiktok_draft") is True


def switches(acc):
    out = []
    for k, w in (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches")):
        v = acc.get(k)
        out.append(f"{w} {'on' if v else 'off'}" if isinstance(v, bool) else f"{w} NOT CHOSEN")
    return out


def settings_bits(acc, video, info):
    """The settings of one post as short phrases: one chip each on plan.html, one line on plan.md."""
    p = acc["platform"]
    ai, promo = video.get("ai_generated"), video.get("promotional")
    bits = []
    if p == "FACEBOOK":
        bits.append("posts as a Reel" if facebook_reel(info) else "posts as a normal video (not vertical, or over 90 s)")
    if p == "TIKTOK":
        if is_draft(acc, video):
            bits.append("draft: finish it in the TikTok app")
        else:
            bits.append("seen by " + PRIVACY_WORDS.get(acc.get("privacyLevel"), "NOT CHOSEN"))
        bits += switches(acc)
        if promo in PROMO:
            bits.append({"no": "no promotion label", "own_brand": "labelled \"Promotional content\"",
                         "paid_partnership": "labelled \"Paid partnership\""}[promo])
    if p == "YOUTUBE":
        bits.append(acc.get("privacy") or "privacy NOT CHOSEN")
        k = acc.get("madeForKids")
        bits.append(("made for kids" if k else "not made for kids") if isinstance(k, bool) else "made for kids NOT CHOSEN")
        if acc.get("category"):
            bits.append(YT_CATEGORIES.get(str(acc["category"]), f"category {acc['category']}"))
        if ai is True:
            bits.append("AI: \"Altered content\" is answered in YouTube Studio")
        if promo == "paid_partnership":
            bits.append("\"Paid promotion\" is ticked in YouTube Studio")
    if p == "INSTAGRAM":
        bits.append("Trial Reel (shown to non-followers first)" if acc.get("trial") else "Reel")
    if p in ("TIKTOK", "INSTAGRAM") and isinstance(ai, bool):
        bits.append("AI label on" if ai else "no AI label")
    if p == "INSTAGRAM" and promo in PROMO:
        bits.append("paid partnership label: added in the app" if promo == "paid_partnership"
                    else "no paid partnership label")
    return bits


def frame_words(cover_at):
    return f" at {cover_at:g} s" if cover_at is not None else ""


def cover_line(acc, video, cover_key, cover_at):
    """What happens with the cover on this account, in one line (None where a cover plays no part)."""
    p = acc["platform"]
    connected = bool(acc.get("socialAccountId"))
    if p in ("TIKTOK", "INSTAGRAM"):
        if not cover_key:
            return "Cover: none chosen, so the first frame shows"
        frame = f" (the frame{frame_words(cover_at)})" if cover_at is not None else ""
        if connected:
            return f"Cover: {cover_key} is sent with the post{frame}"
        return f"Cover: you set it in the app{frame}"
    if p == "YOUTUBE" and cover_key:
        if connected:
            return f"Cover: not sent to YouTube; pick the frame{frame_words(cover_at)} in the YouTube app after it's live"
        return f"Cover: pick the frame{frame_words(cover_at)} in the YouTube app after uploading"
    return None


def after_live(acc, video, cover_key, cover_at):
    """What WoopSocial doesn't set on a connected account, so the user does it in the app once the
    post is live. (For a by-hand account these are steps on its own page.)"""
    p = acc["platform"]
    todo = []
    if p == "YOUTUBE":
        if video.get("ai_generated") is True:
            todo.append("YouTube Studio > the video > Details > \"Altered content\": answer Yes (required for "
                        "realistic AI video)")
        if video.get("promotional") == "paid_partnership":
            todo.append("YouTube Studio > Details > \"Paid promotion\": tick the box")
        if cover_key:
            todo.append(f"the cover: in the YouTube app, open the Short, look for the edit option and pick the "
                        f"frame{frame_words(cover_at)} (the cover image isn't sent to YouTube)")
    if p == "INSTAGRAM" and video.get("promotional") == "paid_partnership":
        todo.append("Instagram app > the Reel > ... > \"Add paid partnership label\"")
    return todo


BY_HAND = {
    "FACEBOOK": "Facebook app or Meta Business Suite: look for \"Create reel\" (for a horizontal video or one over "
                "90 s: a normal post with a video), pick the video and paste the text.",
    "LINKEDIN": "LinkedIn: start a post, add the video and paste the text.",
    "LINKEDIN_PAGES": "LinkedIn: open your Page, start a post, add the video and paste the text.",
    "PINTEREST": "Pinterest: create a Pin, pick the video, and fill in the title, description, link and board.",
    "THREADS": "Threads app: start a new thread, attach the video and paste the text.",
    "X": "X: start a post, attach the video and paste the text.",
    "BLUESKY": "Bluesky: start a new post, attach the video and paste the text.",
}
SCHEDULE_HINT = {
    "TIKTOK": "on a computer, look for \"Schedule\" on the upload page",
    "INSTAGRAM": "look for a schedule option under the advanced or \"More options\" settings before sharing",
    "YOUTUBE": "look for \"Schedule\" in the Visibility step of the upload",
}


def when_step(p, row, verb="Post"):
    """The last step: post now, or how to make it go out at the planned time."""
    if not row["clock"]:
        return f"{verb}."
    hint = SCHEDULE_HINT.get(p, "look for \"Schedule\" near the post button")
    return (f"To have it go out at {row['when']}: {verb.lower()} it at that time, or use the app's own schedule "
            f"option if your account has one ({hint}).")


def tiktok_choices(acc, video, draft):
    """The TikTok steps that are the owner's choices: audience, switches, the two labels."""
    seen = PRIVACY_WORDS.get(acc.get("privacyLevel"))
    who = f"Who can watch: {seen}." if seen else "Who can watch: your choice; TikTok asks it for every post."
    steps = [f"{who} {', '.join(switches(acc)).capitalize()}."]
    promo = {"own_brand": "turn on the content disclosure switch (look for \"Disclose post content\" under \"More "
                          "options\") and pick \"Your brand\"; the post is then labelled \"Promotional content\"",
             "paid_partnership": "turn on the content disclosure switch (look for \"Disclose post content\" under "
                                 "\"More options\") and pick \"Branded content\"; the post is then labelled \"Paid "
                                 "partnership\"",
             "no": "leave the content disclosure switch off (this video promotes nothing)"}.get(video.get("promotional"))
    ai = {True: "turn on the AI label (look for \"AI-generated content\" under \"More options\")",
          False: "leave the AI label off"}.get(video.get("ai_generated"))
    labels = [x for x in (promo, ai) if x]
    if labels:
        steps.append("Labels: " + "; ".join(labels) + ".")
    return steps


def hand_steps(acc, video, words, row, fkey, cover_key, cover_at, grid_key):
    """Numbered steps to post one video to one account in its app. Menu names are given as things
    to look for, not exact paths: the apps rename and move them."""
    p = acc["platform"]
    ai, promo = video.get("ai_generated"), video.get("promotional")
    files = f"{fkey} and the cover image ({cover_key})" if cover_key and p == "INSTAGRAM" else fkey
    phone = (f"Get the files to where you post. {files} {'are' if ' and ' in files else 'is'} on this computer: to "
             "post from a phone, send them to the phone first (AirDrop, a cable or your cloud drive).")
    if p == "TIKTOK" and row["draft"]:
        arrive = row["arrives"] if row["arrives"] == "right after you say yes" else f"at {row['arrives']}"
        steps = [f"Wait for the draft. The agent sends the video to this account's TikTok inbox {arrive}. TikTok "
                 "notifies you: look in the app's inbox for a message that a video is ready to edit. It can take a "
                 "few minutes.",
                 "Open it and add the sound (look for \"Add sound\" on the editing screen).",
                 "Paste the text from \"Text\" above. A draft arrives without its caption."]
        if cover_key:
            steps.append(f"Check the cover (look for \"Edit cover\" or \"Cover\"): the frame{frame_words(cover_at)}.")
        post = f"Post it at {row['when']}." if row["clock"] else "Post it."
        return steps + tiktok_choices(acc, video, True) + [post + " Nothing is public until you do."]
    if p == "TIKTOK":
        steps = [phone + " Or upload from a computer, if TikTok's website offers your account an upload page.",
                 "Start a new post (look for + and then \"Upload\"), pick the video and go on to the screen with "
                 "the caption. Paste the text from \"Text\" above."]
        if video.get("audio") == "app_sound":
            steps.append("Add the sound before you post (look for \"Add sound\" on the editing screen).")
        if cover_at is not None:
            steps.append(f"Cover: look for \"Edit cover\" or \"Cover\" and drag to {cover_at:g} s.")
        elif cover_key:
            steps.append(f"Cover: look for \"Edit cover\" or \"Cover\" and pick the frame that matches {cover_key}.")
        else:
            steps.append("Cover: look for \"Edit cover\" or \"Cover\" and pick a frame; without one the first frame shows.")
        return steps + tiktok_choices(acc, video, False) + [when_step(p, row)]
    if p == "INSTAGRAM":
        steps = [phone, "In the Instagram app start a new Reel (look for + and then \"Reel\"), pick the video and "
                        "go on to the screen with the caption."]
        if cover_key:
            grid = f" The profile grid shows the middle of it: {grid_key} shows how." if grid_key else ""
            steps.append(f"Cover: look for \"Edit cover\" and add the cover image from your camera roll.{grid}")
        else:
            steps.append("Cover: look for \"Edit cover\" and pick a frame; without one the first frame shows.")
        steps.append("Paste the text from \"Text\" above.")
        if acc.get("trial"):
            steps.append("Trial Reel: turn on the trial option (look for \"Trial\") before sharing.")
        if ai is True:
            steps.append("AI label: turn it on (look for \"AI label\" under the advanced or \"More options\" "
                         "settings). The post then shows \"AI info\".")
        if promo == "paid_partnership":
            steps.append("Paid partnership: add the label (look for \"Add paid partnership label\" under the same "
                         "settings).")
        return steps + [when_step(p, row, "Share")]
    if p == "YOUTUBE":
        steps = [f"Use a computer if you can: YouTube Studio (studio.youtube.com) takes {fkey} where it is and has a "
                 "field for tags. Look for \"Create\" and then \"Upload videos\". A vertical or square video of up "
                 "to 3 minutes becomes a Short by itself. From a phone: send the video to the phone first "
                 "(AirDrop, a cable or your cloud drive) and upload it in the YouTube app; the tags can be "
                 "added in Studio later.",
                 "Title: paste the title from above. Description: paste the description."]
        kids = acc.get("madeForKids")
        if isinstance(kids, bool):
            steps.append("Audience: answer \"" + ("Yes, it's made for kids" if kids else "No, it's not made for kids") + "\".")
        else:
            steps.append("Audience: answer the \"made for kids\" question yourself; it is a legal declaration.")
        more = []
        if words["tags"]:
            more.append("Tags: paste the line under \"Tags\" above into the Tags field")
        if acc.get("category"):
            more.append("Category: " + YT_CATEGORIES.get(str(acc["category"]), f"number {acc['category']}"))
        if ai is True:
            more.append("\"Altered content\": answer Yes (this video has realistic AI content)")
        if promo == "paid_partnership":
            more.append("\"Paid promotion\": tick the box")
        if more:
            steps.append("Look for \"Show more\" on the details screen. " + ". ".join(more) + ".")
        vis = f"Visibility: {acc['privacy']}." if acc.get("privacy") else "Visibility: your choice (public, unlisted or private)."
        steps.append(vis + (" " + when_step(p, row, "Publish") if row["clock"] else " Publish."))
        if cover_key:
            steps.append(f"The cover, once it's uploaded: open the Short in the YouTube app, look for the edit option "
                         f"and pick the frame{frame_words(cover_at)}.")
        return steps
    return [phone, BY_HAND[p], when_step(p, row)]


def hand_page(acc, video, words, row, fkey, cover_key, cover_at, grid_key, info):
    """by-hand/<video>/<account>.md: everything to post one video to one account without the agent,
    or (for a TikTok draft) to finish the draft the agent sent."""
    p = acc["platform"]
    vid = video["id"]
    who = f"{acc['name']} {acc['handle']}" if acc.get("handle") else acc["name"]
    if row["draft"]:
        lines = [f"# {vid} on {who} ({LIMITS[p]['label']}): finish the draft in the TikTok app", "",
                 f"Draft arrives: {row['arrives']}", f"Post it at: {row['when']}"]
    else:
        lines = [f"# {vid} on {who} ({LIMITS[p]['label']}), by hand", "", f"When: {row['when']}"]
    lines.append(f"Video: {fkey}")
    if cover_key:
        lines.append(f"Cover: {cover_key}")
    if cover_at is not None:
        lines.append(f"Cover frame: {cover_at:g} s")
    lines.append(f"Answers: {answers_line(video)}")
    if words["title"] and p in ("YOUTUBE", "PINTEREST"):
        lines += ["", "## Title", "", words["title"]]
    lines += ["", "## Description" if p in ("YOUTUBE", "PINTEREST") else "## Text", "", words["text"] or "(none)"]
    if words["tags"]:
        lines += ["", "## Tags", "", ", ".join(words["tags"])]
    if words["link"]:
        lines += ["", "## Link", "", words["link"]]
    if row["settings"]:
        lines += ["", "## Settings", "", ", ".join(row["settings"])]
    lines += ["", "## Steps", "", "Menu names differ between app versions. Where a name below isn't on your "
              "screen, look for the nearest one.", ""]
    steps = hand_steps(acc, video, words, row, fkey, cover_key, cover_at, grid_key)
    lines += [f"{n}. {s}" for n, s in enumerate(steps, 1)]
    if not row["draft"]:
        lines += ["", f"Done? Tell the agent \"posted {acc['name']} by hand\", so a later run leaves it out."]
    return "\n".join(lines) + "\n"


def esc(s):
    return html.escape(str(s), quote=True)


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def summary_line(m):
    """The first line of the plan: how many posts, how they go out, and what a yes means."""
    posts = f"{plural(len(m['rows']), 'post')} to {plural(m['accounts_n'], 'account')}"
    done = f"{len(m['already'])} already sent" if m["already"] else ""
    if not m["connected_n"]:
        extra = f" ({done})" if done else ""
        return (f"{posts}, all by hand{extra}. You post these yourself from the by-hand pages; the agent "
                "sends nothing.")
    parts = [f"{m['send_n']} through WoopSocial"]
    if m["draft_n"]:
        parts.append(f"{m['draft_n']} of them as a TikTok draft you finish in the app")
    parts.append(f"{m['by_hand_n']} by hand")
    if done:
        parts.append(done)
    return f"{posts} ({', '.join(parts)}). Nothing is posted until you say yes."


def card_head(r):
    """(name with handle, platform label or '') for a card or a heading."""
    name = f"{r['account']} {r['handle']}" if r["handle"] else r["account"]
    return name, ("" if r["account"] == r["label"] else r["label"])


CELL = {"posted": "posted", "scheduled": "scheduled", "draft": "draft sent"}
HEAD = {"posted": " (already posted)", "scheduled": " (scheduled)", "draft": " (sent as draft)"}
LEFT = {"posted": "already posted", "scheduled": "scheduled", "draft": "sent as a draft"}


def sent_status(done, zone, now):
    """(kind, words, detail) for an account that already has the video: posted, scheduled (its time
    is still ahead) or a TikTok draft that was sent. Never "already posted" for a post that isn't out."""
    pid = done["postId"]
    if done.get("byHand"):
        return "posted", "already posted by hand", "by hand"
    if done.get("draft") is True:
        return "draft", f"sent as a draft (post {pid})", f"post {pid}"
    try:
        at = datetime.datetime.strptime(done.get("when") or "", "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except (TypeError, ValueError):
        at = None
    if at and at > now:
        t = local_text(at, zone)
        return "scheduled", f"scheduled for {t} (post {pid})", f"post {pid}, {t}"
    return "posted", f"already posted (post {pid})", f"post {pid}"


def planned_line(m):
    line = f"Planned {m['planned']}."
    if any(r["rel"] for r in m["rows"]):
        line += " The \"(in ...)\" times count from then."
    return line


def schedule_rows(m):
    """The batch table: one row per video, one column per account, the time in each cell."""
    names = [a["name"] for a in m["accounts"]]
    table = []
    for vid in m["by_video"]:
        cells = []
        for n in names:
            r = next((r for r in m["rows"] if r["video"] == vid and r["account"] == n), None)
            cells.append("-" if r is None else (CELL[r["posted"]] if r["posted"] else r["short"]))
        table.append((vid, cells))
    return names, table


def page_html(m):
    css = """
:root{--bg:#f6f6f4;--card:#fff;--ink:#17181a;--mute:#62666d;--line:#dcdcd8;--err:#b3261e;--warn:#8a5a00;--ok:#1d6b3a;--chip:#eeeeea}
@media (prefers-color-scheme:dark){:root{--bg:#141516;--card:#1d1f21;--ink:#ececec;--mute:#a1a5ab;--line:#33363a;--err:#ff8a80;--warn:#f0c060;--ok:#7fd49b;--chip:#2a2d30}}
*{box-sizing:border-box;min-width:0}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:24px 16px 64px;overflow-wrap:anywhere}h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:32px 0 6px}
.sub{color:var(--mute);margin:0 0 16px}.answers{color:var(--mute);font-size:14px;margin:0 0 12px}
.video{display:grid;grid-template-columns:200px minmax(0,1fr);gap:20px;align-items:start}
.video img{width:100%;border-radius:10px;display:block;background:#000}.nocover{aspect-ratio:9/16;border:1px dashed var(--line);border-radius:10px;display:grid;place-items:center;color:var(--mute);font-size:14px;text-align:center;padding:12px}
.cards{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr))}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.card h3{margin:0;font-size:16px}.when{color:var(--mute);font-size:14px;margin:2px 0 10px}.title{font-weight:650;margin:0 0 6px}
.text{white-space:pre-wrap;margin:0 0 10px}.count{color:var(--mute);font-size:13px}.fine{color:var(--mute);font-size:13px;margin:8px 0 0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0}.chip{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:13px;max-width:100%}
.hand{color:var(--warn);font-size:13px;font-weight:600}.sent{color:var(--ok);font-weight:600}ul.checks{padding-left:20px;margin:8px 0}.error{color:var(--err)}.warning{color:var(--warn)}.note{color:var(--mute)}
.banner{border-radius:12px;padding:12px 16px;margin:0 0 8px;border:1px solid var(--line);background:var(--card)}
.scroll{overflow-x:auto}table{border-collapse:collapse;font-size:14px}th,td{border:1px solid var(--line);padding:4px 10px;text-align:left}th{background:var(--chip)}
code{font-size:14px}
@media (max-width:640px){.video{grid-template-columns:minmax(0,1fr)}.video>div:first-child{max-width:200px}}
"""
    rows, by_video, job_dir = m["rows"], m["by_video"], m["job_dir"]
    out = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Cross-post plan</title>",
           f"<style>{css}</style></head><body><main>", "<h1>Cross-post plan</h1>",
           f"<p class=\"sub\">{esc(planned_line(m))}<br>{esc(summary_line(m))}</p>"]
    errs = [i for i in issues if i[0] == "error"]
    if errs:
        out.append(f"<div class=\"banner error\"><strong>{len(errs)} thing(s) to fix before this can be posted.</strong> "
                   "They are listed under Checks.</div>")
    if missing:
        out.append(f"<div class=\"banner warning\"><strong>{plural(len(missing), 'answer')} still missing.</strong> "
                   "This plan isn't finished: the questions are listed under Checks.</div>")
    if len(by_video) > 1:
        names, table = schedule_rows(m)
        out.append("<h2>Schedule</h2><div class=\"scroll\"><table><tr><th>Video</th>"
                   + "".join(f"<th>{esc(n)}</th>" for n in names) + "</tr>")
        for vid, cells in table:
            out.append(f"<tr><td>{esc(vid)}</td>" + "".join(f"<td>{esc(c)}</td>" for c in cells) + "</tr>")
        out.append("</table></div>")
    for vid, v in by_video.items():
        out.append(f"<h2>{esc(vid)}</h2><p class=\"answers\">{esc(v['answers'])}</p><div class=\"video\"><div>")
        if v["cover"] and v["cover_ok"]:
            cpath = os.path.join(job_dir, v["cover"])
            if os.path.getsize(cpath) < 2 * MB:   # inside the page, so it shows wherever the page is opened
                with open(cpath, "rb") as fh:
                    src = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode("ascii")
            else:   # a link next to the page; encoded, so a #, ? or % in the name can't break it
                src = urllib.parse.quote(v["cover"], safe="/")
            out.append(f"<img src=\"{esc(src)}\" alt=\"Cover of {esc(vid)}\">")
        elif v["cover"]:
            out.append("<div class=\"nocover\">The cover file can't be shown: it is not a JPEG image</div>")
        else:
            out.append("<div class=\"nocover\">No cover chosen: TikTok and Instagram show the first frame</div>")
        frame = f"<br>Cover frame: {v['cover_at']:g} s" if v["cover_at"] is not None else ""
        out.append(f"<p class=\"count\">{esc(v['file'])}<br>{esc(v['facts'])}{frame}</p></div><div class=\"cards\">")
        for r in [r for r in rows if r["video"] == vid]:
            out.append("<div class=\"card\">")
            name, label = card_head(r)
            sub = f" <span class=\"count\">{esc(label)}</span>" if label else ""
            out.append(f"<h3>{esc(name)}{sub}</h3>")
            if r["posted"]:
                out.append(f"<div class=\"when sent\">{esc(r['when'])}</div>")
            else:
                flag = " <span class=\"hand\">draft</span>" if r["draft"] else ("" if r["connected"] else " <span class=\"hand\">by hand</span>")
                out.append(f"<div class=\"when\">{esc(r['when'] + r['rel'])}{flag}</div>")
            if r["title"]:
                out.append(f"<p class=\"title\">{esc(r['title'])}</p>")
            out.append(f"<p class=\"text\">{esc(r['text']) or '<em>(no text)</em>'}</p>")
            out.append(f"<div class=\"count\">{esc(r['count'])}</div>")
            chips = list(r["settings"])
            if r["tags"]:
                chips.append("tags: " + ", ".join(r["tags"]))
            if chips:
                out.append("<div class=\"chips\">" + "".join(f"<span class=\"chip\">{esc(c)}</span>" for c in chips) + "</div>")
            for line in ([r["cover_line"]] if r["cover_line"] else []) + r["legal"]:
                out.append(f"<p class=\"fine\">{esc(line)}</p>")
            out.append("</div>")
        out.append("</div></div>")
    if issues:
        out.append("<h2>Checks</h2><ul class=\"checks\">")
        for lv, w, msg in sorted(issues, key=lambda i: ("error", "warning", "note").index(i[0])):
            out.append(f"<li class=\"{lv}\"><strong>{esc(w)}</strong>: {esc(msg)}</li>")
        out.append("</ul>")

    def listing(title, intro, items, code=False):
        out.append(f"<h2>{esc(title)}</h2>" + (f"<p class=\"sub\">{esc(intro)}</p>" if intro else "") + "<ul class=\"checks\">"
                   + "".join(f"<li>{'<code>' + esc(t) + '</code>' if code else esc(t)}</li>" for t in items) + "</ul>")
    if m["todo"]:
        listing("After it's live", "WoopSocial doesn't set these, so they are done in the app:", m["todo"])
    if m["draft_files"]:
        listing("Drafts to finish in the TikTok app", "Each page has the caption to paste and the steps:", m["draft_files"], True)
    if m["hand_files"]:
        listing("By hand", "These accounts aren't connected, so each has a page with its text and steps:", m["hand_files"], True)
    if m["already"]:
        listing("Already sent", "These accounts already have the video, or have it scheduled, so they are in no request:",
                [f"{x['video']} on {x['account']}: {x['words']}" for x in m["already"]])
    if m["uploads"]:
        listing("Files to upload", "", [f"{k} ({b / MB:.1f} MB)" for k, b in sorted(m["uploads"].items())], True)
    if m["connected_n"] > 2:
        out.append(f"<p class=\"sub\">{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 "
                   "social accounts; more need a paid plan.</p>")
    out.append("</main></body></html>")
    return "\n".join(out)


def page_md(m):
    rows = m["rows"]
    lines = ["# Cross-post plan", "", planned_line(m), "", summary_line(m), ""]
    if missing:
        lines += [f"**{plural(len(missing), 'answer')} still missing.** This plan isn't finished: the questions "
                  "are listed under Checks.", ""]
    if len(m["by_video"]) > 1:
        names, table = schedule_rows(m)
        lines += ["## Schedule", "", "| Video | " + " | ".join(n.replace("|", "/") for n in names) + " |",
                  "|---|" + "---|" * len(names)]
        lines += [f"| {vid} | " + " | ".join(cells) + " |" for vid, cells in table] + [""]
    for vid, v in m["by_video"].items():
        frame = f" (the frame at {v['cover_at']:g} s)" if v["cover_at"] is not None else ""
        cover = f"Cover: `{v['cover']}`{frame}" if v["cover"] else "Cover: none (TikTok and Instagram show the first frame)"
        lines += [f"## {vid}", "", f"File: `{v['file']}` ({v['facts']})  \n{cover}  \n{v['answers']}", ""]
        for r in [r for r in rows if r["video"] == vid]:
            how = HEAD[r["posted"]] if r["posted"] else (" (draft)" if r["draft"] else ("" if r["connected"] else " (by hand)"))
            name, label = card_head(r)
            head = f"{name} ({label})" if label else name
            lines += [f"### {head}{how}", "", f"- When: {r['when']}{'' if r['posted'] else r['rel']}"]
            if r["settings"]:
                lines.append(f"- Settings: {', '.join(r['settings'])}")
            if r["cover_line"]:
                lines.append(f"- {r['cover_line']}")
            if r["title"]:
                lines.append(f"- Title: {r['title']}")
            if r["tags"]:
                lines.append(f"- Tags: {', '.join(r['tags'])}")
            lines.append(f"- Length: {r['count']}")
            lines += [f"- {x}" for x in r["legal"]]
            lines += ["", "> " + (r["text"].strip() or "(no text)").replace("\n", "\n> "), ""]
    if issues:
        lines += ["## Checks", ""]
        for lv in ("error", "warning", "note"):
            lines += [f"- {lv.upper()} {w}: {msg}" for l2, w, msg in issues if l2 == lv]
        lines.append("")
    if m["todo"]:
        lines += ["## After it's live", "", "WoopSocial doesn't set these, so they are done in the app:", ""]
        lines += [f"- {t}" for t in m["todo"]] + [""]
    if m["draft_files"]:
        lines += ["## Drafts to finish in the TikTok app", "", "Each page has the caption to paste and the steps:", ""]
        lines += [f"- `{f}`" for f in m["draft_files"]] + [""]
    if m["hand_files"]:
        lines += ["## By hand", "", "These accounts aren't connected, so each has a page with its text and steps:", ""]
        lines += [f"- `{f}`" for f in m["hand_files"]] + [""]
    if m["already"]:
        lines += ["## Already sent", "", "These accounts already have the video, or have it scheduled, so they are in no request:", ""]
        lines += [f"- {x['video']} on {x['account']}: {x['words']}" for x in m["already"]] + [""]
    if m["uploads"]:
        lines += ["## Files to upload", ""] + [f"- `{k}` ({b / MB:.1f} MB)" for k, b in sorted(m["uploads"].items())] + [""]
    if m["connected_n"] > 2:
        lines += [f"{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 social accounts; more need a paid plan.", ""]
    return "\n".join(lines)


def load_posted(job_dir):
    """posted.json: {"<video id>|<socialAccountId>": {"postId", "account", "platform", "sha256", ...}},
    and "<video id>|hand:<account name>" for a post the user made by hand to an account that isn't
    connected (moved to the account's id once it is). A damaged file is an error and is left exactly
    as it is: it may be the only record of what went out."""
    path = os.path.join(job_dir, "posted.json")
    if not os.path.exists(path):
        return {}
    posted = read_json(path)
    if not isinstance(posted, dict) or not all(
            isinstance(v, dict) and isinstance(v.get("postId"), str) and v["postId"].strip() and "|" in k
            for k, v in posted.items()):
        die("posted.json is damaged: it must hold one entry per video and account, each with its postId. It "
            "was left as it is. Repair it, or move it away if nothing in it was really posted")
    return posted


def now_text():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_posted(job_dir, request, post_id):
    post_id = post_id.strip()
    if not post_id:
        die("give the post id that posts_create returned, like: --posted requests/<name>.json <postId>")
    idx_path = os.path.join(job_dir, "requests", "index.json")
    idx = read_json(idx_path) if os.path.exists(idx_path) else {}
    name = os.path.basename(request)
    if not isinstance(idx, dict) or not all(
            isinstance(e, dict) and isinstance(e.get("video"), str) and isinstance(e.get("when"), str)
            and isinstance(e.get("accounts"), list)
            and all(isinstance(x, dict) and isinstance(x.get("name"), str) and isinstance(x.get("socialAccountId"), str)
                    for x in e["accounts"]) for e in idx.values()):
        die("requests/index.json is damaged. Run plan.py crosspost.json again to rewrite it, then record the post")
    if name not in idx or not os.path.exists(os.path.join(job_dir, "requests", name)):
        die(f"{name} isn't one of this plan's requests ({', '.join(sorted(k for k in idx)) or 'none written yet'})")
    posted = load_posted(job_dir)
    entry = idx[name]
    stamp = {}
    vpath = os.path.join(job_dir, entry["file"]) if isinstance(entry.get("file"), str) else None
    if vpath and os.path.isfile(vpath):
        digest, size = file_print(vpath)
        stamp = {"file": entry["file"], "sha256": digest, "size": size}
    for x in entry["accounts"]:
        key = f"{entry['video']}|{x['socialAccountId']}"
        if key in posted and posted[key]["postId"] != post_id:
            die(f"{entry['video']} on {x['name']} is already recorded as post {posted[key]['postId']}. If that is "
                f"wrong, release it first with: plan.py crosspost.json --failed {entry['video']} \"{x['name']}\"")
        when = x.get("when") if isinstance(x.get("when"), str) else entry["when"]
        posted[key] = dict({"postId": post_id, "video": entry["video"], "account": x["name"],
                            "platform": x.get("platform"), "when": when, "request": name, "recorded": now_text()},
                           **({"draft": True} if x.get("draft") is True else {}), **stamp)
    write_json(os.path.join(job_dir, "posted.json"), posted)
    who = ", ".join(x["name"] for x in entry["accounts"])
    print(f"recorded: {name} was sent as post {post_id} ({entry['video']} on {who}). plan.py leaves these "
          "accounts out of every new request for this video.")
    print(f"next: posts_get {post_id} and report each account. An account that fails can be released with: "
          f"plan.py crosspost.json --failed {entry['video']} \"<account name>\", then plan again")


def job_accounts(job_path):
    job = read_json(job_path)
    accs = job.get("accounts") if isinstance(job, dict) else None
    return [a for a in accs if isinstance(a, dict)] if isinstance(accs, list) else [], job


def release(job_dir, job_path, which, account):
    """--failed: take one account's entry for one video out of posted.json, so the next plan puts
    that account (and only that account) in a new request."""
    posted = load_posted(job_dir)
    accs, _ = job_accounts(job_path)
    sids = {a["socialAccountId"] for a in accs if a.get("name") == account and isinstance(a.get("socialAccountId"), str)}
    req = os.path.basename(which)
    hits = []
    for k, e in posted.items():
        vid, who = k.split("|", 1)
        if not (which in (vid, e.get("video")) or req == e.get("request")):
            continue
        if account == e.get("account") or who in sids or who == f"hand:{account}":
            hits.append(k)
    if not hits:
        known = sorted({f"{e.get('video')} on {e.get('account')}" for e in posted.values()})
        die(f"posted.json has nothing for {account} with {which}. It holds: {', '.join(known) or 'nothing yet'}")
    videos = sorted({posted[k].get("video") or k.split("|")[0] for k in hits})
    for k in hits:
        del posted[k]
    write_json(os.path.join(job_dir, "posted.json"), posted)
    print(f"removed: {account} no longer counts as having {', '.join(videos)}. Plan again: the new request holds "
          f"only {account}. Show the plan and wait for a new yes before posting it")


def record_hand(job_dir, job_path, vid, account):
    """--posted-by-hand: the user posted this video to this account themselves."""
    accs, job = job_accounts(job_path)
    acc = next((a for a in accs if a.get("name") == account), None)
    if acc is None:
        names = [a.get("name") for a in accs if isinstance(a.get("name"), str)]
        die(f"there is no account named \"{account}\" in the job. Accounts: {', '.join(names) or 'none'}")
    vids = job.get("videos") if isinstance(job.get("videos"), list) else []
    ids = [v.get("id") or (slug(os.path.splitext(os.path.basename(v["file"]))[0]) if isinstance(v.get("file"), str) else None)
           for v in vids if isinstance(v, dict)]
    if vid not in ids:
        die(f"there is no video \"{vid}\" in the job. Videos: {', '.join(str(i) for i in ids if i) or 'none'}")
    posted = load_posted(job_dir)
    sid = acc.get("socialAccountId")
    key = f"{vid}|{sid}" if isinstance(sid, str) and sid else f"{vid}|hand:{account}"
    if key in posted or f"{vid}|hand:{account}" in posted:
        die(f"{vid} on {account} is already recorded in posted.json")
    video = next(v for v, i in zip([v for v in vids if isinstance(v, dict)], ids) if i == vid)
    stamp = {}
    vpath = os.path.join(job_dir, video["file"]) if isinstance(video.get("file"), str) else None
    if vpath and os.path.isfile(vpath):
        digest, size = file_print(vpath)
        stamp = {"file": video["file"], "sha256": digest, "size": size}
    platform = acc.get("platform").strip().upper() if isinstance(acc.get("platform"), str) else None
    posted[key] = dict({"postId": "by hand", "video": vid, "account": account, "platform": platform, "byHand": True,
                        "recorded": now_text()}, **stamp)
    write_json(os.path.join(job_dir, "posted.json"), posted)
    print(f"recorded: {vid} was posted by hand on {account}. plan.py leaves it out from now on.")


def clear_old(job_dir):
    """Remove what the run before wrote, before anything is checked: a plan that stops on an error
    then leaves no old request that could still be sent, and no old plan that looks current."""
    req_dir = os.path.join(job_dir, "requests")
    hand_dir = os.path.join(job_dir, "by-hand")
    for d in (req_dir, hand_dir):
        if os.path.lexists(d) and not os.path.isdir(d):
            die(f"{os.path.basename(d)} is a file here, and plan.py needs a folder with that name. Move or "
                "rename the file")
    if os.path.isdir(req_dir):
        old = [f for f in os.listdir(req_dir) if f.endswith(".json")]
        if old and "index.json" not in old:
            die("the folder requests/ here holds JSON files that plan.py didn't write. Run plan.py from your "
                "own project folder, or move those files somewhere else")
        for f in sorted(old, key=lambda f: f == "index.json"):   # the index goes last
            os.remove(os.path.join(req_dir, f))
        if not os.listdir(req_dir):
            os.rmdir(req_dir)
    for f in ("plan.md", "plan.html"):
        if os.path.isfile(os.path.join(job_dir, f)):
            os.remove(os.path.join(job_dir, f))
    if os.path.isdir(hand_dir):
        for sub in os.listdir(hand_dir):
            folder = os.path.join(hand_dir, sub)
            if not os.path.isdir(folder):
                continue
            for f in os.listdir(folder):
                if f.endswith(".md"):
                    os.remove(os.path.join(folder, f))
            if not os.listdir(folder):
                os.rmdir(folder)
        if not os.listdir(hand_dir):
            os.rmdir(hand_dir)


def broken_text(obj):
    """The first text in the job that holds half an emoji (a lone surrogate from a cut-off copy)."""
    if isinstance(obj, str):
        return obj if any(0xD800 <= ord(c) <= 0xDFFF for c in obj) else None
    if isinstance(obj, dict):
        obj = list(obj.keys()) + list(obj.values())
    if isinstance(obj, list):
        for x in obj:
            found = broken_text(x)
            if found is not None:
                return found
    return None


def load_media(arg, job_dir, plan_files):
    """media.json as {file as plan.md lists it: mediaId}. Looked for in the folder the command runs
    from, then next to the job file. A key that is no file of this plan is an error, not ignored."""
    if not arg:
        return {}
    path = arg
    if not os.path.isabs(arg) and not os.path.exists(arg):
        path = os.path.join(job_dir, arg)
        if not os.path.exists(path):
            die(f"{arg} not found (looked in the folder you ran this from and next to the job file)")
    media = read_json(path)
    if not isinstance(media, dict) or not all(isinstance(x, str) and x.strip() for x in media.values()):
        die(f"{arg}: must map each uploaded file to its mediaId, like {{\"clips/launch.mp4\": \"123\"}}")
    out = {}
    for k, v in media.items():
        key = k if k in plan_files else rel(os.path.normpath(os.path.join(job_dir, k)), job_dir)
        if key not in plan_files:
            die(f"{arg} names \"{k}\", which is not a file of this plan. Use the names as plan.md lists them: "
                f"{', '.join(sorted(plan_files))}")
        out[key] = v.strip()
    return out


def check_cover(video, cpath, where):
    """The cover must really be a JPEG (its bytes, not its name). Returns True when it is one."""
    shown = video["cover"]
    size = jpeg_size(cpath)
    if size is None:
        kind = file_kind(cpath)
        what = "a JPEG that is damaged or cut off" if kind == "a JPEG" else kind
        issue("error", where, f"the cover {shown} is not a JPEG image that can be read (the file is {what}). "
              "Instagram takes JPEG only: make the cover with cover.py, or save it again as JPEG")
        return False
    if not cpath.lower().endswith((".jpg", ".jpeg")):
        issue("error", where, f"the cover {shown} is a JPEG, but its name must end in .jpg; rename it")
    elif os.path.getsize(cpath) > 8 * MB:
        issue("error", where, f"the cover is {os.path.getsize(cpath) / MB:.1f} MB; Instagram allows 8 MB")
    elif abs(size[0] / size[1] - 9 / 16) > 0.03:
        issue("warning", where, f"the cover is {size[0]}x{size[1]}; a 9:16 cover fills the screen, "
              "anything else is cropped to its middle")
    return True


def cover_frame(cpath, video_path, video, where):
    """The second the cover was taken from, read from the note cover.py writes next to it
    (covers/<id>.json). None when there is no note. A note made from another video is a warning."""
    side = os.path.splitext(cpath)[0] + ".json"
    if not os.path.isfile(side):
        return None
    try:
        with open(side, encoding="utf-8-sig") as fh:
            note = json.load(fh)
        at = note["at"]
        if isinstance(at, bool) or not isinstance(at, (int, float)) or not math.isfinite(at) or at < 0:
            raise ValueError
    except Exception:
        issue("warning", where, f"{rel(side, os.path.dirname(os.path.dirname(side)))} can't be read, so the cover's "
              "frame time isn't shown. Make the cover again with cover.py --at")
        return None
    src = note.get("video")
    if isinstance(src, str) and not same_file(os.path.join(os.path.dirname(side), src), video_path):
        issue("warning", where, f"the cover {video['cover']} was taken from {os.path.basename(src)}, not from "
              f"{os.path.basename(video_path)}. Make it again from this video with cover.py")
    return float(at)


def count_line(p, words):
    """The length shown on the plan: the same numbers check_text() uses."""
    L = LIMITS[p]
    n, approx = text_length(p, words["text"])
    if p == "YOUTUBE":
        return f"title {len(words['title'] or '')}/{L['title']} characters, description {n}/{L['text_bytes']} bytes"
    nt = len(hashtags(words["text"]))
    return f"{'about ' if approx else ''}{n}/{L['text']} characters, {nt} hashtag{'' if nt == 1 else 's'}"


def in_words(when, now):
    """" (in 1 day 4 h)": the wrong day is caught by the distance, not by the date."""
    mins = max(int((when - now).total_seconds() // 60), 0)
    hours, m = divmod(mins, 60)
    days, h = divmod(hours, 24)
    if days:
        return f" (in {plural(days, 'day')}" + (f" {h} h)" if h else ")")
    if hours:
        return f" (in {h} h" + (f" {m} min)" if m else ")")
    return f" (in {m} min)"


def same_platform_checks(rows, accounts, texts_by_video):
    """Several accounts on one platform: once per job, never once per video."""
    by_name = {a["name"]: a for a in accounts}
    for p in LIMITS:
        names = [a["name"] for a in accounts if a["platform"] == p]
        shared = sorted({r["video"] for r in rows if r["platform"] == p
                         and sum(1 for x in rows if x["video"] == r["video"] and x["platform"] == p) > 1})
        if len(names) < 2 or not shared:
            continue
        who = sorted({r["account"] for r in rows if r["platform"] == p and r["video"] in shared}, key=names.index)
        auds = [by_name[n]["audience"] for n in who]
        label = LIMITS[p]["label"]
        # accounts of this platform with no text under their own name share the platform's text
        inherit, inherit_vids = [], []
        for vid in shared:
            mine = [(acc["name"], own) for acc, own in texts_by_video.get(vid, []) if acc["platform"] == p]
            bare = [n for n, own in mine if not own]
            if len(mine) > 1 and len(bare) > 1:
                inherit_vids.append(vid)
                inherit += [n for n in bare if n not in inherit]
        if inherit:
            vids = ", ".join(inherit_vids[:5]) + (f" and {len(inherit_vids) - 5} more" if len(inherit_vids) > 5 else "")
            issue("warning", label, f"{' and '.join(inherit)} have no text under their own name, so they get the "
                  f"same {label} text ({vids}). Give each account its own text (\"text\": {{\"{inherit[-1]}\": "
                  "...}) in its own language or for its own audience")
        if all(auds) and len(set(a.lower() for a in auds)) == len(auds):
            own = "" if inherit else ", each with the text written for it"
            issue("note", label, f"the same video goes to {len(who)} {label} accounts with different audiences "
                  f"({', '.join(f'{n}: {a}' for n, a in zip(who, auds))}){own}")
            continue
        rule = {"YOUTUBE": "YouTube's spam policy names high volumes of similar content across channels, and edits "
                           "made to disguise copies",
                "INSTAGRAM": "Instagram recommends only the original when it finds identical copies",
                "TIKTOK": "TikTok's guidelines don't name it, but make reused material \"without anything new\" "
                          "ineligible for the For You feed"}.get(p, f"{label} has duplicate-content rules of its own")
        vids = ", ".join(shared[:5]) + (f" and {len(shared) - 5} more" if len(shared) > 5 else "")
        issue("warning", label, f"the same video goes to {len(who)} {label} accounts ({', '.join(who)}): {vids}. "
              f"{rule}. If the accounts serve different audiences (a language, a region, a brand), write that in "
              "each account as \"audience\" and give each its own text. Never change speed, crop or filters to "
              "make copies look different")


def spacing_checks(rows, now):
    """Per account: two posts less than an hour apart, and the documented daily caps."""
    for name in dict.fromkeys(r["account"] for r in rows):
        mine = sorted(((r["at"] or now), r["video"], r) for r in rows if r["account"] == name and not r["posted"])
        close = [(a, b) for a, b in zip(mine, mine[1:]) if (b[0] - a[0]) < datetime.timedelta(minutes=60)]
        if close:
            (t1, v1, _), (t2, v2, _) = close[0]
            issue("warning", name, f"gets {v1} and {v2} less than 60 minutes apart. Give each video its own time "
                  "on this account")
        if not mine:
            continue
        platform = mine[0][2]["platform"]
        window = datetime.timedelta(hours=24)

        def most(items):
            return max(sum(1 for t in items if s <= t < s + window) for s in items) if items else 0
        if platform == "INSTAGRAM" and mine[0][2]["connected"] and most([t for t, _, _ in mine]) > 100:
            issue("warning", name, "more than 100 posts within 24 hours; Instagram allows 100 posts through its "
                  "API per account per 24 hours. Spread them out")
        drafts = [r["send_at"] or now for _, _, r in mine if r["draft"]]
        if most(drafts) > 5:
            issue("warning", name, "more than 5 TikTok drafts within 24 hours; at most 5 drafts wait per account "
                  "per 24 hours. Spread them out, or post some directly")


def record_for(posted, vid, acc):
    """This account's entry for this video, or None. A connected account is found by its id; one
    that isn't connected by its name and platform (a by-hand record)."""
    sid = acc.get("socialAccountId")
    if sid and f"{vid}|{sid}" in posted:
        return posted[f"{vid}|{sid}"]
    hand = posted.get(f"{vid}|hand:{acc['name']}")
    if hand and hand.get("platform") in (None, acc["platform"]):
        return hand
    return None


def follow_hand_records(posted, accounts):
    """A by-hand record ("<video>|hand:<name>") of an account that is now connected moves to the
    account's id, so it keeps counting after the account is renamed. True when anything moved."""
    moved = False
    for acc in accounts:
        sid = acc.get("socialAccountId")
        if not sid:
            continue
        for k in list(posted):
            vid, who = k.split("|", 1)
            e = posted[k]
            if who != f"hand:{acc['name']}" or e.get("platform") not in (None, acc["platform"]):
                continue
            posted.setdefault(f"{vid}|{sid}", dict(e, account=acc["name"], platform=acc["platform"]))
            del posted[k]
            moved = True
    return moved


def orphan_records(vid, posted, accounts):
    """A record of this video that matches no account in the job: say so, never resend in silence."""
    for k, e in posted.items():
        v, who = k.split("|", 1)
        if v != vid or any(record_for({k: e}, vid, acc) for acc in accounts):
            continue
        name = e.get("account") if isinstance(e.get("account"), str) else who
        plat = LIMITS.get(e.get("platform") or "", {}).get("label")
        how = "by hand" if e.get("byHand") else f"post {e['postId']}"
        what = f"\"{name}\" ({plat}, {how})" if plat else f"\"{name}\" ({how})"
        if who.startswith("hand:"):
            why = (f"no account in this job has that name. If that account was renamed, it gets {vid} a second "
                   f"time: name it \"{name}\" again")
        else:
            why = (f"no account in this job has its socialAccountId. If that account is in this job under another "
                   f"id, it gets {vid} a second time")
        issue("warning", vid, f"posted.json records {vid} on {what}, but {why}. If {vid} was never posted there, "
              f"release the record with: plan.py crosspost.json --failed {vid} \"{name}\"")


def same_id_as_before(vid, path, posted, prints):
    """A recorded post of this video id came from another file: a new video under an old id."""
    for k, e in posted.items():
        if k.split("|", 1)[0] != vid or not isinstance(e.get("sha256"), str):
            continue
        if path not in prints:
            size = os.path.getsize(path)
            prints[path] = file_print(path) if e.get("size") in (None, size) else ("", size)
        if prints[path][0] != e["sha256"]:
            die(f"video id '{vid}' was already posted from a different file; give this video a new id "
                f"(\"id\" in the job, for example \"{vid}-{datetime.date.today().isoformat()}\")")


def main():
    ap = argparse.ArgumentParser(description="Check a cross-post job and write the plan.")
    ap.add_argument("job")
    ap.add_argument("--media", help="media.json: {file: mediaId} after uploading the video and the cover")
    ap.add_argument("--posted", nargs=2, metavar=("REQUEST", "POST_ID"), help="record that a request was sent")
    ap.add_argument("--failed", nargs=2, metavar=("REQUEST_OR_VIDEO", "ACCOUNT"),
                    help="release an account whose post failed, so the next plan sends it again")
    ap.add_argument("--posted-by-hand", nargs=2, metavar=("VIDEO", "ACCOUNT"),
                    help="record that the user posted a video to an account by hand")
    a = ap.parse_args()
    if os.path.isdir(a.job):
        die(f"{a.job} is a folder; give the job file (crosspost.json)")
    if not os.path.exists(a.job):
        die(f"{a.job} not found")
    job_dir = os.path.dirname(os.path.abspath(a.job))
    if a.posted:
        return record_posted(job_dir, a.posted[0], a.posted[1])
    if a.failed:
        return release(job_dir, a.job, a.failed[0], a.failed[1])
    if a.posted_by_hand:
        return record_hand(job_dir, a.job, a.posted_by_hand[0], a.posted_by_hand[1])
    clear_old(job_dir)
    job = read_json(a.job)
    if not isinstance(job, dict):
        die(f"{a.job} must be a JSON object (see references/job-file.md)")
    bad = broken_text(job)
    if bad is not None:
        near = " ".join("".join(c for c in bad if not 0xD800 <= ord(c) <= 0xDFFF).split())[:40]
        die(f"{a.job} holds half an emoji or a broken character (a cut-off copy), near \"{near}\". Retype that text")
    for k in job:
        if k != "timezone" and k.replace("_", "").replace(" ", "").replace("-", "").lower() in ("timezone", "tz"):
            die(f"\"{k}\" must be spelled \"timezone\" (lowercase, one word)")
    default_tz = job.get("timezone")
    if default_tz is not None and not isinstance(default_tz, str):
        die("timezone must be a name like Europe/Amsterdam")
    default_tz = (default_tz or "").strip() or None   # no zone is fine until a clock time needs one
    if default_tz:
        tzinfo(default_tz)
    defaults = job.get("defaults")
    if defaults is not None:
        if not isinstance(defaults, dict):
            die("\"defaults\" must be an object, like {\"audio\": \"original\", \"promotional\": \"no\"}")
        wrong = [k for k in defaults if k not in DEFAULT_KEYS]
        if wrong:
            die(f"\"defaults\" has \"{wrong[0]}\"; it can hold {', '.join(DEFAULT_KEYS)}")
    accounts = job.get("accounts")
    if not isinstance(accounts, list) or not accounts:
        die("the job needs \"accounts\": where the video goes (see references/job-file.md)")
    videos = job.get("videos")
    if not isinstance(videos, list) or not videos:
        die("the job needs \"videos\": at least one {\"id\": ..., \"file\": ...}")
    for video in videos:
        if isinstance(video, dict):
            for k, val in (defaults or {}).items():   # a video's own value wins
                video.setdefault(k, copy.deepcopy(val))
            if video.get("tiktok_draft") is not None and not isinstance(video["tiktok_draft"], bool):
                die("tiktok_draft is true or false")

    def all_drafts(acc):
        """True when every video going to this account is a TikTok draft (its audience is then
        picked in the app)."""
        if not isinstance(acc, dict) or not isinstance(acc.get("platform"), str):
            return False
        p = acc["platform"].strip().upper()
        nm = acc.get("name") if acc.get("name") is not None else LIMITS.get(p, {}).get("label")
        mine = [v for v in videos if isinstance(v, dict)
                and (v.get("accounts") is None or (isinstance(v["accounts"], list) and nm in v["accounts"]))]
        return bool(mine) and all(v.get("tiktok_draft") is True for v in mine)
    accounts = [check_account(acc, n, all_drafts(acc)) for n, acc in enumerate(accounts)]
    names = [acc["name"] for acc in accounts]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        die(f"two accounts are named '{dup[0]}'; give each its own name")
    slugs = [slug(n) for n in names]
    if len(set(slugs)) != len(slugs):
        die("two account names are too alike (they become the same file name); make them more different")
    ids = [acc["socialAccountId"] for acc in accounts if acc.get("socialAccountId")]
    if len(set(ids)) != len(ids):
        die("two accounts share one socialAccountId; each account is listed once")
    posted = load_posted(job_dir)
    reading(a.job)
    if follow_hand_records(posted, accounts):
        write_json(os.path.join(job_dir, "posted.json"), posted)
    connected_n = sum(1 for acc in accounts if acc.get("socialAccountId"))
    now = datetime.datetime.now(datetime.timezone.utc)
    shown = shown_now()
    prints = {}   # path: (sha256, size), each video file read once

    rows, by_video, groups, todo, kits, already = [], {}, {}, [], [], []
    plan_files = set()
    seen_ids = set()
    texts_by_video = {}
    for n, video in enumerate(videos):
        if not isinstance(video, dict) or not isinstance(video.get("file"), str) or not video["file"].strip():
            die(f"video {n + 1} needs a \"file\"")
        if video.get("id") is None:
            video["id"] = slug(os.path.splitext(os.path.basename(video["file"]))[0])
        if not valid_id(video["id"]):
            shown = str(video["id"])
            die(f"video id '{shown[:40]}{'...' if len(shown) > 40 else ''}' must be letters, numbers and dashes "
                "only, 80 at most, like \"launch-day\" (and not a name Windows reserves, like con or nul)")
        vid = video["id"]
        if vid.lower() in seen_ids:
            die(f"two videos have the id '{vid}'; give each video its own \"id\"")
        seen_ids.add(vid.lower())
        if video.get("text") is not None and not isinstance(video["text"], dict):
            die(f"video {vid}: \"text\" must be like {{\"TIKTOK\": \"...\", \"YOUTUBE\": {{\"title\": \"...\"}}}}")
        path = os.path.normpath(os.path.join(job_dir, video["file"]))
        info = probe(path, video["file"])
        fkey = rel(path, job_dir)
        same_id_as_before(vid, path, posted, prints)
        orphan_records(vid, posted, accounts)
        plan_files.add(fkey)
        only = video.get("accounts")
        if only is not None and (not isinstance(only, list) or any(x not in names for x in only)):
            die(f"video {vid}: \"accounts\" must list account names from this job ({', '.join(names)})")
        targets = [acc for acc in accounts if only is None or acc["name"] in only]
        if not targets:
            die(f"video {vid} goes to no account")
        check_when(video, accounts, targets)
        check_video_answers(video, any(acc.get("socialAccountId") for acc in targets))
        cover_key, cover_ok, cover_at, grid_key = None, False, None, None
        if video.get("cover"):
            if not isinstance(video["cover"], str):
                die(f"video {vid}: cover is the path to an image")
            cpath = os.path.normpath(os.path.join(job_dir, video["cover"]))
            if os.path.isdir(cpath):
                die(f"video {vid}: cover {video['cover']} is a folder; give the image file")
            if not os.path.exists(cpath):
                die(f"video {vid}: cover {video['cover']} not found (make it with cover.py)")
            cover_ok = check_cover(video, cpath, vid)
            cover_key = rel(cpath, job_dir)
            plan_files.add(cover_key)
            cover_at = cover_frame(cpath, path, video, vid)
            gpath = os.path.splitext(cpath)[0] + "-grid.jpg"
            grid_key = rel(gpath, job_dir) if os.path.isfile(gpath) else None
        elif any(acc["platform"] in ("TIKTOK", "INSTAGRAM") for acc in targets):
            issue("warning", vid, "no cover chosen, so TikTok and Instagram show the first frame (often a blank or "
                  "a blink). Pick one with cover.py")
        if video.get("tiktok_draft") is True and not any(acc["platform"] == "TIKTOK" and acc.get("socialAccountId")
                                                         for acc in targets):
            issue("note", vid, "tiktok_draft only applies to a connected TikTok account; the by-hand pages "
                  "say where the sound is added")
        length = f"{info['duration']:.1f} s" if info["duration"] else "length unknown"
        by_video[vid] = {"file": fkey, "cover": cover_key, "cover_ok": cover_ok, "cover_at": cover_at,
                         "bytes": info["bytes"], "answers": answers_line(video),
                         "cover_bytes": os.path.getsize(cpath) if cover_key else 0,
                         "facts": f"{info['width']}x{info['height']}, {length}, {info['bytes'] / MB:.1f} MB"}
        texts = {}
        own_text = video.get("text") or {}
        for acc in targets:
            p = acc["platform"]
            where = f"{vid} -> {acc['name']}"
            connected = bool(acc.get("socialAccountId"))
            draft = is_draft(acc, video)
            done = record_for(posted, vid, acc)
            mark = len(issues)
            for lv, msg, _ in file_issues(info, p, acc.get("max_video_s")):
                issue(lv, where, msg)
            words = text_for(video, acc)
            check_text(video, acc, words)
            if (p == "TIKTOK" and not draft and video.get("promotional") == "paid_partnership"
                    and acc.get("privacyLevel") == "SELF_ONLY"):
                issue("error", where, "a paid partnership post can't be \"only you\" on TikTok; choose another audience")
            if video.get("audio") == "app_sound" and not draft:
                tip = (" For TikTok you can also send it as a draft (\"tiktok_draft\": true) and add the sound in "
                       "the TikTok app") if p == "TIKTOK" and connected else ""
                if video.get("tiktok_draft") is True:
                    tip = (" This video goes to TikTok as a draft: set \"audio\" to what the file itself carries "
                           "(usually \"original\"). The TikTok sound is added to the draft in the app and isn't in "
                           "the file")
                issue("error", where,
                      "a sound picked inside an app doesn't travel: an uploaded copy can be muted or blocked. Use "
                      "the original export with your own or licensed audio, or post by hand and add the sound in "
                      "the app." + tip)
            if video.get("audio") == "licensed" and p == "YOUTUBE" and info["duration"] > 60:
                issue("warning", where, "over 1 minute with music: if the Short gets an active copyright claim, "
                      "YouTube blocks it everywhere. Keep it under 60 s, or be sure of the licence")
            local, utc = when_for(video, acc, default_tz, check_past=not done)
            at = (datetime.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
                  if utc else None)
            send_utc, send_at, arrives = utc, at, None
            if draft:
                if at and at - DRAFT_LEAD > now + datetime.timedelta(minutes=5):
                    send_at = at - DRAFT_LEAD
                    send_utc = send_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                    arrives = (local - DRAFT_LEAD).strftime("%a %d %b %Y, %H:%M ") + (local.tzname() or "")
                else:
                    send_utc, send_at = None, None
                    arrives = "right after you say yes"
                    if at:
                        issue("note", where, "the draft can't arrive 2 hours before the post time, so it is sent "
                              "right after the yes")
            new, issues[mark:] = issues[mark:], []
            if done:
                # this account already has this video: nothing about it can block or change the plan
                if done.get("when") not in (None, utc or "now") and not done.get("byHand"):
                    issue("warning", where, f"already sent as post {done['postId']} for {done['when']}; the job "
                          "now gives another time. To move it: delete that post (posts_delete), release it with "
                          f"plan.py crosspost.json --failed {vid} \"{acc['name']}\" and plan again")
            else:
                for lv, w, msg in new:   # an account posted by hand can't stop the connected ones
                    issue("warning" if lv == "error" and not connected else lv, w, msg)
            if not draft or not connected:
                texts.setdefault(words["text"].strip(), []).append(acc["name"])
            texts_by_video.setdefault(vid, []).append((acc, acc["name"] in own_text))
            when = (local.strftime("%a %d %b %Y, %H:%M ") + (local.tzname() or "") if local
                    else "as soon as you say yes" if connected else "whenever you post it")
            short = local.strftime("%a %d %b %H:%M") if local else "now"
            if draft:
                short += " (draft)"
            if done:
                kind, when, detail = sent_status(done, acc.get("timezone") or default_tz, now)
                already.append({"video": vid, "account": acc["name"], "kind": kind, "words": when, "detail": detail})
            legal = []
            if p == "TIKTOK" and connected and not done:
                legal.append("By posting, you agree to TikTok's Branded Content Policy and Music Usage Confirmation."
                             if video.get("promotional") == "paid_partnership"
                             else "By posting, you agree to TikTok's Music Usage Confirmation.")
            L = LIMITS[p]
            row = {"video": vid, "account": acc["name"], "handle": acc.get("handle"), "label": L["label"],
                   "platform": p, "when": when, "short": short, "rel": in_words(at, shown) if at and not done else "",
                   "utc": utc, "at": at, "send_at": send_at, "clock": bool(local), "connected": connected,
                   "posted": kind if done else False, "draft": draft and not done, "arrives": arrives,
                   "title": words["title"] if p in ("YOUTUBE", "PINTEREST") else None,
                   "text": words["text"], "count": count_line(p, words),
                   "tags": words["tags"] if p == "YOUTUBE" else [],
                   "settings": settings_bits(acc, video, info),
                   "cover_line": cover_line(acc, video, cover_key, cover_at), "legal": legal}
            rows.append(row)
            if connected:
                for t in after_live(acc, video, cover_key, cover_at):
                    todo.append(f"{vid} on {acc['name']}: {t}")
            if done:
                continue   # never into a request again
            if connected:
                groups.setdefault((vid, send_utc), []).append((acc, words, info, video, fkey, cover_key, utc))
            if not connected or draft:
                kits.append((acc, words, row, fkey, cover_key, cover_at, grid_key, video, info))
        for body, who in texts.items():
            plats = {next(acc["platform"] for acc in accounts if acc["name"] == x) for x in who}
            short_form = [x for x in who if next(acc["platform"] for acc in accounts if acc["name"] == x) in SHORT_FORM]
            if body and len(short_form) > 1 and len(plats) > 1:
                issue("note", vid, f"{' and '.join(short_form)} have the same text. It posts fine; a text written for "
                      "each platform reads better (their limits, hashtags and search differ)")
        handles = {}
        for row in [r for r in rows if r["video"] == vid]:
            for m in mentions(row["text"]):
                handles.setdefault(m.lower(), set()).add(row["platform"])
        for m, where_used in handles.items():
            if len(where_used) > 1:
                issue("warning", vid, f"{m} is used on {len(where_used)} platforms. A handle belongs to one platform: "
                      "check that it's the same account on each, or it tags nobody or a stranger")
    same_platform_checks(rows, accounts, texts_by_video)
    spacing_checks(rows, now)

    media = load_media(a.media, job_dir, plan_files)
    reading(a.job)
    errors = [i for i in issues if i[0] == "error"]
    req_dir = os.path.join(job_dir, "requests")
    index, written, placeholders, uploads = {}, [], False, {}
    per_video = {}
    for (vid, utc) in sorted(groups, key=lambda k: (k[0], k[1] or "")):
        per_video.setdefault(vid, []).append(utc)
    for (vid, utc), members in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")):
        k = per_video[vid].index(utc) + 1
        name = f"{vid}.json" if len(per_video[vid]) == 1 else f"{vid}.{k}.json"
        _, first_words, info, video, fkey, cover_key, _ = members[0]
        draft_of = {acc["name"]: is_draft(acc, video) for acc, *_ in members}
        takes_cover = cover_key and any(acc["platform"] in ("TIKTOK", "INSTAGRAM") for acc, *_ in members)
        uploads[fkey] = by_video[vid]["bytes"]
        if takes_cover:
            uploads[cover_key] = by_video[vid]["cover_bytes"]
        vmedia = media.get(fkey) or f"<mediaId of {fkey}>"
        cmedia = (media.get(cover_key) or f"<mediaId of {cover_key}>") if takes_cover else None
        placeholders = placeholders or "<mediaId" in vmedia or bool(cmedia and "<mediaId" in cmedia)
        req = {"content": [{"text": first_words["text"], "media": [{"type": "MEDIA_LIBRARY", "mediaId": vmedia}]}],
               "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": utc} if utc else {"type": "PUBLISH_NOW"},
               "socialAccounts": [body_for(acc, words, vmedia, cmedia, video, info) for acc, words, *_ in members]}
        index[name] = {"video": vid, "when": utc or "now", "file": fkey,
                       "accounts": [dict({"name": acc["name"], "socialAccountId": acc["socialAccountId"],
                                          "platform": acc["platform"], "when": post_utc or "now"},
                                         **({"draft": True} if draft_of[acc["name"]] else {}))
                                    for acc, *_, post_utc in members]}
        if not errors:   # with errors, no request files: nothing half-decided can be sent
            write_json(os.path.join(req_dir, name), req)
            written.append(name)
    if index:
        write_json(os.path.join(req_dir, "index.json"), index)

    hand_dir = os.path.join(job_dir, "by-hand")
    hand_files, draft_files = [], []
    for acc, words, row, fkey, cover_key, cover_at, grid_key, video, info in kits:
        out = os.path.join(hand_dir, video["id"], f"{slug(acc['name'])}.md")
        write_text(out, hand_page(acc, video, words, row, fkey, cover_key, cover_at, grid_key, info))
        (draft_files if row["draft"] else hand_files).append(rel(out, job_dir))

    by_hand_n = sum(1 for r in rows if not r["connected"] and not r["posted"])
    send_n = sum(1 for r in rows if r["connected"] and not r["posted"])
    m = {"rows": rows, "by_video": by_video, "job_dir": job_dir, "accounts": accounts, "accounts_n": len(accounts),
         "connected_n": connected_n, "send_n": send_n, "by_hand_n": by_hand_n,
         "draft_n": sum(1 for r in rows if r["draft"]), "already": already, "todo": todo,
         "hand_files": hand_files, "draft_files": draft_files, "uploads": uploads,
         "planned": local_text(shown, default_tz)}
    write_text(os.path.join(job_dir, "plan.md"), page_md(m))
    write_text(os.path.join(job_dir, "plan.html"), page_html(m))

    for lv, w, msg in issues:
        print(f"{lv}: {w}: {msg}", file=sys.stderr)
    notes = sum(1 for i in issues if i[0] == "note")
    gap = f", {plural(len(missing), 'answer')} still missing" if missing else ""
    print(f"{plural(len(rows), 'post')} planned{gap} -> plan.md, plan.html ({len(errors)} errors, "
          f"{len(issues) - len(errors) - notes} warnings, {notes} notes)")
    if hand_files:
        print(f"by hand ({len(hand_files)}): by-hand/")
    if draft_files:
        print(f"TikTok drafts to finish in the app ({len(draft_files)}): by-hand/")
    for x in already:
        print(f"{LEFT[x['kind']]}, left out: {x['video']} on {x['account']} ({x['detail']})")
    if errors:
        print("no requests written until the errors above are fixed")
        if missing:
            print(f"next: ask the user the {plural(len(missing), 'missing answer')} in one message, add the answers to "
                  "crosspost.json and plan again")
    elif missing:
        print(f"next: ask the user the {plural(len(missing), 'missing answer')} in one message, add the answers to "
              "crosspost.json and plan again before showing the plan")
    elif written:
        print(f"requests: {', '.join('requests/' + n for n in written)}")
        if placeholders:
            print("next: show plan.html (or paste plan.md) and wait for a clear yes. Only after the yes: upload each "
                  "file under \"Files to upload\", save {file: mediaId} as media.json, run again with --media media.json")
        else:
            print("next: posts_validate each request. If validation made you change the job, plan again, show it and "
                  "wait for a new yes. If nothing changed, posts_create each request (the yes covers it), run "
                  "--posted right after each, then posts_get")
    elif hand_files and not connected_n:
        print("next: show plan.html (or paste plan.md); the user posts from the by-hand pages. Nothing is sent by "
              "the agent")
    elif hand_files:
        print("next: show plan.html; nothing is left to send, the user posts the rest from the by-hand pages")
    elif already:
        print("nothing left to send: every connected account already has its video")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    guard(main)
