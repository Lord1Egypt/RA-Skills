#!/usr/bin/env python3
"""Check every clip of a campaign job against the campaign's rules and each platform's limits.

    python3 scripts/check_clips.py clipjob.json           # one line per post, then every problem
    python3 scripts/check_clips.py clipjob.json --json    # the same as JSON

clipjob.json (references/job-file.md) names the campaign file, the accounts with the settings the
user chose, and one post per account: the clip, its caption (and a title for YouTube).

Checked per post: the file (length, size, frame rate, codec, shape) for its platform; the campaign's
length and shape; the caption starts with the disclosure (#ad) and holds every required hashtag,
@mention and link; nothing banned and no engagement bait; the on-screen disclosure and watermark
(from the manifest make_clips.py wrote, or declared for a clip the user made); the footage is one
the campaign supplied; the brand's approval when the brief asks for it; a clip cut for this campaign,
with this campaign's disclosure on screen (a line naming another brand is refused).

Accounts: each has a socialAccountId from this session's social_accounts_list or "by_hand": true.
Accounts saved with plan.py --remember-accounts are matched on platform and handle and shown as
suggestions only; nothing is filled in from them.

Checked across posts: no two accounts get the same file; two accounts don't use mostly the same
footage (over the campaign's max_overlap); no edit already posted, in this campaign or another
(ledger.json); no moment posted again on the same account.

Exit code 0 when nothing blocks posting, 1 otherwise. plan.py runs the same checks.
"""
import argparse, datetime, json, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import campaign as campaign_mod  # noqa: E402
from cliplib import (place_name, ENGAGEMENT_BAIT, ENGAGEMENT_SOFT, LIMITS, PLATFORMS, TIKTOK_PRIVACY, clean_ranges,  # noqa: E402
                     die, file_issues, find_phrases, guard, hashtags, hide_ad_hits, is_num, ledger_path, links,
                     load_ledger, load_saved_accounts, account_key, mentions, money, norm_link, now_utc, overlap_share, parse_time,
                     placeholder_id, probe, read_json, rel, sha256, stamp, text_length, valid_id)

PRIVACY_WORDS = {"PUBLIC_TO_EVERYONE": "everyone", "MUTUAL_FOLLOW_FRIENDS": "friends",
                 "FOLLOWER_OF_CREATOR": "followers", "SELF_ONLY": "only you"}


class Checks:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        if (level, where, msg) not in self.items:
            self.items.append((level, where, msg))

    def errors(self):
        return [i for i in self.items if i[0] == "error"]


def body_words(text):
    """A caption without its hashtags, handles, links and disclosure: what it actually says."""
    t = re.sub(r"(?<![\w&])[#@][\w.]+", " ", text or "")
    t = " ".join(re.sub(r"https?://\S+|www\.\S+", " ", t).lower().split())
    return re.sub(r"[^\w ]", "", t).strip()


def starts_with(text, disclosure):
    """The caption opens with the disclosure as its own word: "#ad ..." yes, "#ad_..." or "#ads" no."""
    t, d = (text or "").lstrip().lower(), disclosure.strip().lower()
    return t.startswith(d) and (len(t) == len(d) or t[len(d)].isspace() or t[len(d)] in ".,:;!|-")


def has_link(text, want):
    """A link the brief requires, matched as a link (not as part of a longer one): example.com/orbit
    isn't satisfied by example.com/orbit-old. A bare domain is satisfied by any link on it."""
    w = norm_link(want)
    found = [norm_link(x) for x in links(text)]
    if w in found:
        return True
    if "/" not in w and any(f.split("/")[0] == w for f in found):
        return True
    low = re.sub(r"(?i)https?://(?:www\.)?|(?<![\w.])www\.", "", (text or "").lower())
    return re.search(r"(?<![\w./-])" + re.escape(w) + r"(?![\w/-])", low) is not None


def same_name(a, b):
    return os.path.basename(str(a or "")).casefold() == os.path.basename(str(b or "")).casefold()


def check_account(acc, n, camp, ck):
    where = f"account {acc.get('name') or n}"
    p = acc.get("platform")
    own = camp.get("own_content") is True
    if not own:
        mk = camp.get("marketplace") or "the marketplace"
        ver = acc.get("marketplace_verified")
        listed = [str(x).casefold() for x in acc.get("verified_in") or [] if isinstance(x, str)]
        if ver is False:
            ck.add("error", where, f"not verified in {mk}: posts from an account that isn't connected and verified "
                   "there are rejected. Verify it in the marketplace first, or leave it out")
        elif ver is not True and str(camp.get("marketplace") or "").casefold() not in listed:
            ck.add("warning", where, f"ask the user: is this account connected and verified in {mk}? Posts from an "
                   "account that isn't are rejected (set \"marketplace_verified\": true once it is)")
    aud = camp.get("audience") if isinstance(camp.get("audience"), dict) else None
    known = acc.get("audience") if isinstance(acc.get("audience"), dict) else {}
    if aud and isinstance(aud.get("geo"), str) and is_num(known.get(aud["geo"])) and is_num(aud.get("min_share")):
        if known[aud["geo"]] < aud["min_share"]:
            ck.add("warning", where, f"this account's audience is about {known[aud['geo']]:.0%} {aud['geo']}; the "
                   f"campaign rejects clips under {aud['min_share']:.0%}. Expect this one to be rejected: post it from an "
                   f"account whose viewers are mostly in {place_name(aud['geo'])}, or skip it")
    if p not in PLATFORMS:
        ck.add("error", where, f"platform must be one of {', '.join(PLATFORMS)}")
        return
    plats = camp.get("platforms") if isinstance(camp.get("platforms"), dict) else {}
    if p not in plats:
        ck.add("error", where, f"the campaign doesn't pay for {LIMITS[p]['label']} views; leave this account out "
               "or check the brief")
    sid = acc.get("socialAccountId")
    hand = acc.get("by_hand")
    if hand is not None and not isinstance(hand, bool):
        ck.add("error", where, "by_hand is true (the user posts this account in the app) or false")
    if hand is True and sid is not None:
        ck.add("error", where, "by_hand is true and the account also has a socialAccountId. Say which: posted through "
               "WoopSocial (keep the id, take by_hand out) or by hand (take the id out)")
    elif sid is not None and (not isinstance(sid, str) or placeholder_id(sid)):
        ck.add("error", where, "socialAccountId is a placeholder. Put the id from social_accounts_list (this session's "
               "reply), or set \"by_hand\": true to post this account in the app")
    elif sid is None and hand is not True:
        ck.add("error", where, "say how this account posts: \"socialAccountId\" from this session's social_accounts_list "
               "(through WoopSocial), or \"by_hand\": true (the user posts it in the app)")
    if p == "TIKTOK":
        pl = acc.get("privacyLevel")
        opts = acc.get("privacyOptions") if isinstance(acc.get("privacyOptions"), list) else TIKTOK_PRIVACY
        if pl is None:
            ck.add("error", where, "ask the user who can see this TikTok (everyone, friends, followers, only you); "
                   "TikTok makes the account owner choose, never the agent")
        elif pl not in opts:
            ck.add("error", where, f"privacyLevel {pl} isn't one this account offers ({', '.join(opts)})")
        elif pl == "SELF_ONLY":
            ck.add("error", where, "a campaign post can't be posted as \"only you\" on TikTok (a branded post can't be "
                   "private), and a private post earns no campaign views")
        elif pl != "PUBLIC_TO_EVERYONE":
            ck.add("warning", where, f"seen by {PRIVACY_WORDS[pl]} only: campaigns pay for public views, so this post "
                   "will earn little or nothing")
        for k, w in (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches")):
            if not isinstance(acc.get(k), bool):
                ck.add("error", where, f"ask the user: {w} on or off? (TikTok makes the account owner choose)")
    if p == "YOUTUBE":
        if acc.get("privacy") not in ("public", "unlisted", "private"):
            ck.add("error", where, "ask the user: public, unlisted or private? (campaigns count public views only)")
        elif acc["privacy"] != "public":
            ck.add("warning", where, f"{acc['privacy']}: campaigns pay for public views, so this Short will earn nothing")
        if not isinstance(acc.get("madeForKids"), bool):
            ck.add("error", where, "ask the user: is this channel's Short made for kids? (YouTube makes the owner "
                   "declare it)")


def manifest_entries(job, job_dir, ck):
    """{sha256: (entry, manifest)} for every clip in the manifest(s) make_clips.py wrote."""
    paths = job.get("manifest", "clips/manifest.json")
    paths = [paths] if isinstance(paths, str) else paths
    if not isinstance(paths, list):
        ck.add("error", "job", "\"manifest\" is the path of clips/manifest.json (or a list of them)")
        return {}
    out = {}
    for mp in paths:
        full = os.path.join(job_dir, mp) if isinstance(mp, str) else None
        if not full or not os.path.isfile(full):
            if mp != "clips/manifest.json" or "manifest" in job:
                ck.add("error", "job", f"manifest {mp} not found")
            continue
        m = read_json(full, "the clip manifest")
        if not isinstance(m, dict) or not isinstance(m.get("clips"), list):
            ck.add("error", "job", f"{mp} is not a manifest written by make_clips.py")
            continue
        mdir = os.path.dirname(full)
        for c in m["clips"]:
            if isinstance(c, dict) and isinstance(c.get("sha256"), str):
                out[c["sha256"]] = (c, m, mdir)
    return out


SUGGEST = (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches"), ("privacy", "visibility"),
           ("madeForKids", "made for kids"), ("audience", "audience"))


def saved_suggestions(accounts):
    """Lines for the accounts the user saved once (<user_home>/accounts.json) that match an account of
    this job on platform AND handle. Nothing is filled in: the agent shows these to the user, and
    writes what they confirm into clipjob.json. The WoopSocial id, TikTok's privacy choice and the
    marketplace verification are never taken from the saved file."""
    saved = {account_key(a): a for a in load_saved_accounts() if account_key(a)}
    out = []
    for a in accounts:
        s = saved.get(account_key(a))
        if not s:
            continue
        bits = []
        for k, w in SUGGEST:
            if k in s and k not in a:
                v = s[k]
                bits.append(f"{w} {'on' if v is True else 'off' if v is False else json.dumps(v)}")
        if bits:
            out.append(f"{a['name']} {a.get('handle')}: last time {', '.join(bits)}")
    return out


def generic_disclosure(text):
    """A disclosure that names no brand at all ("Ad", "Sponsored", "Paid partnership"): it can't name
    the wrong one."""
    words = "".join(c.lower() if c.isalnum() else " " for c in text or "").split()
    return bool(words) and all(w in campaign_mod.DISCLOSURE_WORDS or w in ("with", "a", "an") for w in words)


def wm_label(w):
    if isinstance(w, dict):
        return f"the logo {w.get('image')}" if w.get("image") else f"\"{w.get('text')}\""
    return f"\"{w}\"" if isinstance(w, str) and w else "none"


def wm_matches(want, got, campaign_dir):
    """The clip carries the watermark the campaign asks for: the same text, or the same logo file."""
    if want.get("image"):
        if not isinstance(got, dict) or not got.get("image"):
            return False
        path = want.get("image_path") or os.path.join(campaign_dir, want["image"])
        if got.get("image_sha256") and os.path.isfile(path):
            return got["image_sha256"] == sha256(path)
        return same_name(got["image"], want["image"])
    text = got.get("text") if isinstance(got, dict) else got
    return isinstance(text, str) and text.strip().lower() == (want.get("text") or "").strip().lower()


def check_job(job_path, ledger_file=None):
    """Load and check a job. Returns a model the plan is drawn from: campaign info, accounts, one row
    per post with its file facts, texts and problems, and every check."""
    ck = Checks()
    job = read_json(job_path, "the campaign job")
    job_dir = os.path.dirname(os.path.abspath(job_path))
    if not isinstance(job, dict):
        die(f"{rel(job_path)} must hold one JSON object: campaign, accounts and posts")
    cpath = job.get("campaign")
    if not isinstance(cpath, str) or not cpath:
        die(f"{rel(job_path)} needs \"campaign\": the path of the campaign file (campaign.json)")
    cfull = os.path.join(job_dir, cpath)
    info = campaign_mod.load(cfull)
    camp = info["campaign"] if isinstance(info["campaign"], dict) else {}
    own = camp.get("own_content") is True
    for lv, f, m in info["issues"]:
        ck.add(lv, "campaign", f"{f}: {m}")
    accounts = job.get("accounts")
    if not isinstance(accounts, list) or not accounts or not all(isinstance(a, dict) for a in accounts):
        die(f"{rel(job_path)} needs \"accounts\": a list with one entry per account, like {{\"name\": \"TikTok\", "
            "\"platform\": \"TIKTOK\", ...}}")
    names = [a.get("name") for a in accounts]
    if not all(isinstance(n, str) and n.strip() for n in names):
        die("every account needs a \"name\" (like \"TikTok\" or \"Reels 2\")")
    if len(set(names)) != len(names):
        die("two accounts share a name; give each its own")
    for line in saved_suggestions(accounts):
        ck.add("note", "accounts", f"saved choice for {line}. Ask the user to confirm, then write it into clipjob.json; "
               "nothing is filled in by itself")
    for n, a in enumerate(accounts, 1):
        if isinstance(a.get("platform"), str):
            a["platform"] = a["platform"].strip().upper()
        check_account(a, n, camp, ck)
    by_name = {a["name"]: a for a in accounts}
    posts = job.get("posts")
    if not isinstance(posts, list) or not posts or not all(isinstance(p, dict) for p in posts):
        die(f"{rel(job_path)} needs \"posts\": a list with one post per account (clip, caption, title for YouTube)")
    lpath = ledger_path(ledger_file)
    ledger = load_ledger(lpath)
    manifest = manifest_entries(job, job_dir, ck)
    cap = camp.get("caption") if isinstance(camp.get("caption"), dict) else {}
    disclosure = cap.get("disclosure") if isinstance(cap.get("disclosure"), str) and cap["disclosure"].strip() else (
        None if own else "#ad")
    length = camp.get("length") if isinstance(camp.get("length"), dict) else {}
    footage = camp.get("footage") if isinstance(camp.get("footage"), dict) else {}
    allowed = footage.get("files") if isinstance(footage.get("files"), list) and footage.get("files") else None
    recency = footage.get("recency_days") if is_num(footage.get("recency_days"), 1) else None
    dates = footage.get("dates") if isinstance(footage.get("dates"), dict) else {}
    max_overlap = camp.get("max_overlap", 0.5)
    want_wm = camp.get("watermark_spec")
    want_sd = (camp.get("on_screen") or {}).get("disclosure") if isinstance(camp.get("on_screen"), dict) else None
    links_where = camp.get("links_where") or "caption"
    now = now_utc()
    ai_default = job.get("ai_generated")
    rows, ids = [], set()
    for n, p in enumerate(posts, 1):
        pid = p.get("id")
        where = f"post {pid if isinstance(pid, str) else n}"
        if not valid_id(pid):
            ck.add("error", where, "give each post a short id of lowercase letters, digits and dashes (like "
                   "\"groundhog-tiktok\")")
            pid = f"post-{n}"
        if pid in ids:
            ck.add("error", where, "this post id is used twice; give each post its own")
        ids.add(pid)
        acc = by_name.get(p.get("account"))
        if acc is None:
            ck.add("error", where, f"account \"{p.get('account')}\" isn't in accounts ({', '.join(names)})")
            continue
        plat = acc.get("platform")
        if plat not in LIMITS:
            continue
        label = LIMITS[plat]["label"]
        row = {"id": pid, "account": acc, "name": acc["name"], "platform": plat, "label": label,
               "handle": acc.get("handle") or "", "connected": isinstance(acc.get("socialAccountId"), str)
               and not placeholder_id(acc["socialAccountId"]) and acc.get("by_hand") is not True,
               "post": p, "issues": [], "posted": None}

        def bad(level, msg, _row=row, _where=where):
            ck.add(level, _where, msg)
            _row["issues"].append((level, msg))
        # the answers only the user can give
        ai = p.get("ai_generated", ai_default)
        if not isinstance(ai, bool):
            bad("error", "ask the user: does the clip show realistic AI-made people, scenes or voices? (ai_generated "
                "true or false)")
        row["ai"] = ai
        # the file
        f = p.get("file")
        full = os.path.join(job_dir, f) if isinstance(f, str) and f else None
        if not full or not os.path.isfile(full):
            bad("error", f"clip file {f!r} not found" if f else "\"file\": which clip this account gets")
            rows.append(row)
            continue
        row["file"] = rel(full, job_dir)
        row["full"] = full
        vinfo = probe(full, row["file"])
        row["info"] = vinfo
        row["sha256"] = sha256(full)
        appr = p.get("approved")
        if camp.get("approval_before_posting"):
            if isinstance(appr, dict):
                fp = appr.get("sha256")
                if not isinstance(fp, str) or not row["sha256"].startswith(fp.lower()) or len(fp) < 12:
                    bad("error", "this file changed after the brand approved it (its fingerprint isn't the approved "
                        "one). Send the new version for approval, or post the approved file")
                row["approved"] = appr
            elif appr is True:
                bad("warning", "approved: keep the brand's approval message. Record it as \"approved\": {\"by\": ..., "
                    "\"at\": ..., \"sha256\": \"" + row["sha256"][:12] + "\"} so a changed file is caught")
                row["approved"] = {}
            else:
                bad("error", "the brief asks for the brand's approval before posting. Send the approval packet "
                    f"(approval/{pid}.md, written by plan.py), then record the answer in \"approved\"")
                row["needs_approval"] = True
        for lv, msg in file_issues(vinfo, plat, acc.get("max_video_s") if plat == "TIKTOK" else None):
            bad(lv, msg)
        s = vinfo["duration"]
        if isinstance(length.get("min_s"), (int, float)) and s + 0.3 < length["min_s"]:
            bad("error", f"{s:.1f} s is shorter than the campaign's minimum of {length['min_s']:g} s")
        if isinstance(length.get("max_s"), (int, float)) and s - 0.3 > length["max_s"]:
            bad("error", f"{s:.1f} s is longer than the campaign's maximum of {length['max_s']:g} s")
        if camp.get("aspect", "9:16") == "9:16" and abs(vinfo["width"] / vinfo["height"] - 9 / 16) > 0.03:
            bad("error", f"{vinfo['width']}x{vinfo['height']} isn't the vertical 9:16 the campaign asks for")
        # where it came from and what is on screen
        ent = manifest.get(row["sha256"])
        if ent:
            c, m, mdir = ent
            src_name = os.path.basename(m.get("video") or "")
            row["source"] = {"file": src_name, "sha256": m.get("video_sha256"), "ranges": clean_ranges(c.get("ranges"))}
            row["screen"] = c.get("on_screen") if isinstance(c.get("on_screen"), dict) else {}
            row["hook"] = c.get("hook") or ""
            row["cover"] = os.path.join(mdir, c["cover"]) if isinstance(c.get("cover"), str) else None
            row["made_by"] = "make_clips.py"
            if c.get("account") and c["account"] != acc["name"]:
                bad("warning", f"this clip was cut for account \"{c['account']}\", not {acc['name']}")
            if m.get("campaign") and m["campaign"] != camp.get("id"):
                bad("error", f"this clip was cut for campaign {m['campaign']}, not {camp.get('id')}: what is on screen "
                    "follows that brief. Cut it again for this campaign with make_clips.py")
        else:
            src = p.get("source") if isinstance(p.get("source"), dict) else {}
            row["source"] = {"file": os.path.basename(src.get("file") or "") if isinstance(src.get("file"), str) else "",
                             "sha256": None, "ranges": clean_ranges(src.get("ranges"))}
            row["screen"] = p.get("on_screen") if isinstance(p.get("on_screen"), dict) else {}
            row["hook"] = p.get("hook") or ""
            row["cover"] = None
            row["made_by"] = "declared"
            if not row["source"]["file"] or row["source"]["ranges"] is None:
                bad("error", "this clip isn't in the manifest make_clips.py wrote. Say which footage it uses: "
                    "\"source\": {\"file\": \"<source video>\", \"ranges\": [[start, end]]} in seconds of the source")
            if not row["screen"] and not own:
                bad("error", "this clip isn't in the manifest make_clips.py wrote. Say what is on screen: "
                    "\"on_screen\": {\"disclosure\": \"...\", \"disclosure_seconds\": 4, \"watermark\": ...}, after "
                    "watching the clip")
        sd = row["screen"].get("disclosure")
        if not own:
            if not isinstance(sd, str) or not sd.strip():
                bad("error", "no disclosure on screen. Every campaign clip shows \"Ad\" or \"Paid partnership with "
                    f"{camp.get('brand', '<brand>')}\" in its first seconds; cut it again with make_clips.py")
            elif not campaign_mod.screen_line_ok(sd, camp):
                bad("error", f"the on-screen line \"{sd}\" doesn't say the clip is paid")
            elif isinstance(want_sd, str) and want_sd.strip() and " ".join(sd.split()).casefold() != \
                    " ".join(want_sd.split()).casefold() and not generic_disclosure(sd):
                bad("error", f"the clip says \"{sd}\" on screen; this campaign's disclosure is \"{want_sd}\". A clip that "
                    "names another brand is a misleading disclosure. Cut it again with make_clips.py")
            else:
                secs = row["screen"].get("disclosure_seconds", 0)
                if not isinstance(secs, (int, float)) or secs < 2:
                    bad("error", "the on-screen disclosure shows for under 2 seconds at the start; viewers must be able "
                        "to read it")
        got_wm = row["screen"].get("watermark")
        if want_wm and not wm_matches(want_wm, got_wm, info["base_dir"]):
            bad("error", f"the brief asks for {wm_label(want_wm)} on screen; this clip has {wm_label(got_wm)}")
        src_file = row["source"]["file"]
        if allowed is not None and src_file and not any(same_name(src_file, x) for x in allowed):
            bad("error", f"footage {src_file} isn't footage this campaign supplied ({', '.join(allowed)})")
        rec = next((v for k, v in dates.items() if src_file and same_name(k, src_file)), None)
        row["footage_date"] = rec
        if recency and src_file:
            try:
                day = datetime.date.fromisoformat(rec) if isinstance(rec, str) else None
            except ValueError:
                day = None
            if day is None:
                bad("error", f"the brief takes footage from the last {recency:g} days only. Ask the user which day "
                    f"{src_file} was recorded (never the file's date on disk) and add it to footage.dates")
            elif (now.date() - day).days > recency:
                bad("error", f"{src_file} was recorded on {rec}, {(now.date() - day).days} days ago; the brief takes "
                    f"footage from the last {recency:g} days only, so this clip would be rejected")
        # the texts
        text = p.get("caption")
        title = p.get("title")
        tags = p.get("tags") or []
        row["text"], row["title"], row["tags"] = text if isinstance(text, str) else "", title if isinstance(title, str) else "", tags
        if not isinstance(text, str) or not text.strip():
            bad("error", "write a caption" + (" (the YouTube description)" if plat == "YOUTUBE" else ""))
            text = ""
        if plat == "YOUTUBE":
            if not isinstance(title, str) or not title.strip():
                bad("error", "a YouTube Short needs a title")
            elif len(title) > 100:
                bad("error", f"the title has {len(title)} characters; YouTube allows 100")
            if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
                bad("error", "\"tags\" is a list of words")
                row["tags"] = []
            if any(ch in (row["title"] + text) for ch in "<>"):
                bad("error", "YouTube refuses < and > in a title or description; write \"less than\", or leave them out")
        n_len = text_length(plat, text)
        row["count"] = n_len
        lim = LIMITS[plat].get("text") or LIMITS[plat].get("text_bytes")
        if n_len > lim:
            bad("error", f"the caption is {n_len} long; {label} allows {lim}")
        if text and disclosure and not starts_with(text, disclosure):
            bad("error", f"the caption must start with {disclosure} as its own word, before anything else, so viewers "
                "see it before \"more\"")
        tags_in = {h.lower() for h in hashtags(text)}
        for h in cap.get("hashtags") or []:
            if isinstance(h, str) and h.lower() not in tags_in:
                bad("error", f"the brief requires {h} in the caption")
        handles_in = {m.lower() for m in mentions(text)}
        for m in cap.get("mentions") or []:
            if isinstance(m, str) and m.lower() not in handles_in:
                bad("error", f"the brief requires {m} in the caption")
        for u in cap.get("links") or []:
            if not isinstance(u, str) or has_link(text, u) or links_where == "bio":
                continue
            if links_where == "either":
                bad("note", f"{u} isn't in the caption, so it must be in the bio (set before posting)")
            else:
                bad("error", f"the brief requires the link {u} in the caption")
        if plat == "INSTAGRAM" and len(hashtags(text)) > LIMITS["INSTAGRAM"]["tags_max"]:
            bad("error", f"{len(hashtags(text))} hashtags; Instagram allows 5")
        everything = " ".join([text, row["title"], row["hook"], " ".join(t for t in row["tags"] if isinstance(t, str))])
        low = everything.lower()
        for b in camp.get("banned") or []:
            if not isinstance(b, str):
                continue
            hit = b.lower() in {h.lower() for h in hashtags(everything)} if b.startswith("#") else \
                re.search(r"(?<!\w)" + re.escape(b.lower()) + r"(?!\w)", low)
            if hit:
                bad("error", f"the brief bans \"{b}\"")
        for sentence, _ in find_phrases(everything, ENGAGEMENT_BAIT):
            bad("error", f"\"{sentence}\" asks for or arranges engagement; that is a permanent ban on the marketplaces")
        for sentence, _ in find_phrases(everything, ENGAGEMENT_SOFT):
            bad("warning", f"\"{sentence}\" reads like asking viewers to swap follows or likes. If it asks for that, "
                "take it out: it is against platform rules and a ban on the marketplaces")
        if not own:
            for sentence, _ in hide_ad_hits(everything):
                bad("error", f"\"{sentence}\" plays down that the clip is paid; take it out")
        # already posted (this exact post, recorded in the ledger)
        for k, e in ledger["posts"].items():
            if e.get("job_post") == pid and e.get("campaign") == camp.get("id") and e.get("account") == acc["name"]:
                row["posted"] = dict(e, key=k)
        rows.append(row)

    # across posts: the same file, mostly the same footage, an edit used before
    ready = [r for r in rows if r.get("sha256")]
    small = [r for r in ready if r["info"]["width"] < 1080 and not r["posted"]]
    if small:
        sizes = sorted({f"{r['info']['width']}x{r['info']['height']}" for r in small})
        ck.add("warning", "clips", f"{len(small)} clip(s) are {', '.join(sizes)}, under 1080x1920: fine for a draft or an "
               "example; for real posts cut them again without --width, platforms show 1080x1920 sharpest")
    for i, a in enumerate(ready):
        for b in ready[i + 1:]:
            pair = f"posts {a['id']} and {b['id']}"
            if a["sha256"] == b["sha256"]:
                ck.add("error", pair, f"{a['name']} and {b['name']} get the same file. Each account gets its own edit: "
                       "another moment, or another hook and caption")
                continue
            compare(a, b, pair, max_overlap, ck)
    for r in ready:
        for k, e in ledger["posts"].items():
            if r["posted"] and r["posted"]["key"] == k:
                continue
            if e.get("sha256") == r["sha256"]:
                if e.get("campaign") != camp.get("id"):
                    ck.add("error", f"post {r['id']}", f"this exact edit was already posted for campaign "
                           f"{e.get('campaign')} ({e.get('account')}). An edit goes into one campaign only")
                else:
                    ck.add("error", f"post {r['id']}", f"this exact edit is already posted on {e.get('account')}. Each "
                           "account gets its own edit")
            elif e.get("campaign") == camp.get("id"):
                other = {"id": e.get("job_post") or k, "name": e.get("account"), "platform": e.get("platform"),
                         "posted": True,
                         "source": {"sha256": e.get("source_sha256"), "file": e.get("source_file"),
                                    "ranges": clean_ranges(e.get("ranges"))},
                         "hook": e.get("hook") or "", "text": e.get("caption") or ""}
                compare(r, other, f"post {r['id']} and the posted {other['id']}", max_overlap, ck)
    # the budget: read it on the campaign page before cutting, and again before posting
    left = camp.get("budget_remaining")
    if is_num(left, 0):
        cur = camp.get("currency", "USD")
        capv = camp.get("cap_per_clip")
        if left <= 0:
            ck.add("error", "campaign", "the remaining budget is 0: views no longer pay. Check the campaign page; if it "
                   "is really empty, skip this campaign")
        elif is_num(capv, 0) and capv and left < 10 * capv:
            ck.add("warning", "campaign", f"only {money(left, cur)} of the budget is left (under 10 clips at the "
                   f"{money(capv, cur)} cap). It can run out before your clips earn; check it again right before posting")
        when = parse_time(camp.get("budget_checked_at"))
        if when and (now - when).total_seconds() > 24 * 3600:
            ck.add("warning", "campaign", f"the remaining budget was read {(now - when).days} day(s) ago. Read it again on "
                   "the campaign page before posting and update budget_remaining")
    return {"job": job, "job_dir": job_dir, "job_path": job_path, "campaign": camp, "camp_info": info,
            "accounts": accounts, "rows": rows, "checks": ck.items, "ledger": ledger, "ledger_path": lpath,
            "disclosure": disclosure}


def compare(a, b, pair, max_overlap, ck):
    """Two edits from the same footage: how much they share, and whether that blocks."""
    sa, sb = a.get("source") or {}, b.get("source") or {}
    same_src = (sa.get("sha256") and sa.get("sha256") == sb.get("sha256")) or (
        not (sa.get("sha256") and sb.get("sha256")) and sa.get("file") and sa.get("file") == sb.get("file"))
    if not same_src or not sa.get("ranges") or not sb.get("ranges"):
        return
    share = overlap_share(sa["ranges"], sb["ranges"])
    if share <= max_overlap:
        return
    where = f"{stamp(sa['ranges'][0][0])} to {stamp(sa['ranges'][-1][1])}"
    if a.get("name") == b.get("name"):
        if a.get("posted") or b.get("posted"):
            ck.add("error", pair, f"{a['name']} already posted {share:.0%} of this footage for this campaign. Posting the "
                   "same moment again on the same account is a double post. Give it another moment")
        else:
            ck.add("warning", pair, f"the same account gets {share:.0%} of the same footage twice; posting it again "
                   "looks like a repost")
    elif a.get("platform") == b.get("platform"):
        ck.add("error", pair, f"{a['name']} and {b['name']} are both {LIMITS[a['platform']]['label']} and share "
               f"{share:.0%} of their footage ({where}). The platforms treat that as the same content on several "
               "accounts. Give one of them another moment")
    elif (a.get("hook") or "").strip().lower() == (b.get("hook") or "").strip().lower() or \
            body_words(a.get("text")) == body_words(b.get("text")):
        ck.add("error", pair, f"{a['name']} and {b['name']} share {share:.0%} of their footage ({where}) with the same "
               "hook or caption. Give one another moment, or both their own hook and caption")
    else:
        ck.add("warning", pair, f"{a['name']} and {b['name']} share {share:.0%} of their footage ({where}). They have "
               "their own hook and caption, so it isn't blocked, but another moment is the safer edit")


def summary(model):
    out = []
    for r in model["rows"]:
        head = f"{r['id']} ({r['name']}{' ' + r['handle'] if r['handle'] else ''}, {r.get('file', 'no file')}"
        if r.get("info"):
            head += f", {r['info']['duration']:.1f} s"
        head += ")"
        lv = [l for l, _ in r["issues"]]
        state = "already posted" if r["posted"] else ("BLOCKED" if "error" in lv else "ok")
        out.append(f"{head}: {state}")
        for l, m in r["issues"]:
            out.append(f"  {l}: {m}")
    shown = {(l, m) for r in model["rows"] for l, m in r["issues"]}
    for l, w, m in model["checks"]:
        if (l, m) in shown:
            continue
        out.append(f"{l}: {w}: {m}")
    return out


def main():
    ap = argparse.ArgumentParser(description="Check every clip against the campaign and the platforms.")
    ap.add_argument("job")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ledger", help="the ledger file (default: AI_CLIPPING_LEDGER, else ~/.ai-clipping/ledger.json)")
    a = ap.parse_args()
    model = check_job(a.job, a.ledger)
    errs = [i for i in model["checks"] if i[0] == "error"]
    warns = [i for i in model["checks"] if i[0] == "warning"]
    if a.json:
        print(json.dumps({"errors": len(errs), "warnings": len(warns),
                          "checks": [{"level": l, "where": w, "message": m} for l, w, m in model["checks"]],
                          "posts": [{"id": r["id"], "account": r["name"], "file": r.get("file"),
                                     "sha256": r.get("sha256"), "issues": [m for _, m in r["issues"]]}
                                    for r in model["rows"]]}, indent=1, ensure_ascii=False))
    else:
        print("\n".join(summary(model)))
        print(f"\n{len(errs)} error(s), {len(warns)} warning(s)")
        if errs:
            print("fix every error, then run this again. Nothing can be posted while one is left")
        else:
            print(f"next: python3 {os.path.join(HERE, 'plan.py')} {rel(a.job)}  (the plan page for the user's yes)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    guard(main)
