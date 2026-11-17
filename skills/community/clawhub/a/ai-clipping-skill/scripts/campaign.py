#!/usr/bin/env python3
"""Check a clipping campaign's rules and print them as a numbered checklist.

    python3 scripts/campaign.py campaign.json                    # check, print, write checklist.md
    python3 scripts/campaign.py campaign.json --brief brief.txt  # also scan this brief text

campaign.json is written by the agent from the campaign brief the user pasted (the fields are in
references/campaign-file.md). This script checks every field, prints the checklist the user
confirms before any clip is cut, and writes it to checklist.md next to campaign.json.

It also reads the raw brief text (the "brief_file" in campaign.json, or --brief) and flags:
- sentences that ask to hide that a clip is paid ("don't use #ad", "make it look organic", "skip
  the disclosure" and similar). Never followed: the disclosure stays on every clip.
- sentences that forbid the disclosure on the video itself ("no paid partnership text on the
  video"). The skill keeps it on screen, so the brief and the skill disagree: the user asks the
  campaign team in writing or skips the campaign.
- sentences that ask for bought or arranged engagement or location tricks. A sentence that bans
  them ("no engagement groups") is the brief's own rule and isn't flagged.
- sentences that name the disclosure next to a "no" or a rejection which the patterns can't place:
  listed under "Read these sentences yourself" for the agent to read.

own_content (your own content on your own accounts, nobody paying per view) is refused when the
campaign has a marketplace, a brand, a rate, a payout rule, a budget or a fee, or when its brief
talks about hiding the ad: those are paid campaigns, and every clip of a paid campaign is disclosed.

Exit code 0 when the campaign file has no errors, 1 otherwise.
"""
import argparse, hashlib, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cliplib import (place_name, DISCLOSURE_CONFLICT, ENGAGEMENT_BAIT, ENGAGEMENT_SOFT, LIMITS, LOCATION_TRICKS,  # noqa: E402
                     PLATFORMS, asks_for, die, find_phrases, guard, hashtags, hide_ad_hits, is_num, mentions, money,
                     parse_time, read_json, read_yourself, reading, rel, sound_spec, terms, threshold_views, valid_id, with_defaults,
                     write_text)

DISCLOSURE_WORDS = ("ad", "ads", "advert", "advertisement", "sponsored", "paid", "partnership", "promotion",
                    "promoted", "anzeige", "werbung", "reclame", "publicité", "publicidad", "pubblicità")
CAPTION_DISCLOSURES = ("#ad", "#advert", "#advertisement", "#sponsored", "#paidpartnership", "#anzeige",
                       "#werbung", "#reclame", "#publicidad", "#pub", "ad", "paid partnership")
WEAK_TAGS = ("#sp", "#spon", "#collab", "#partner", "#gifted", "#thanks")
WM_POSITIONS = ("top-left", "top", "top-right", "center", "bottom-left", "bottom", "bottom-right")
IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".webp")


NEGATIONS = ("not", "no", "non", "never", "isn", "isnt", "nt")
DEMO_LINE = "example only"


def says_paid(text):
    """True when an on-screen line plainly says the clip is paid. "Not an ad" or "no ad" says the
    opposite, so a disclosure word with a negation just before it doesn't count."""
    words = "".join(c.lower() if c.isalnum() else " " for c in text or "").split()
    for i, w in enumerate(words):
        if w in DISCLOSURE_WORDS and not any(x in NEGATIONS for x in words[max(0, i - 3):i]):
            return True
    return False


def example_demo(c):
    """The skill's own made-up example (id "example-...", brand "Example ...", "example_demo": true):
    its clips show a line saying they are a demo instead of a paid-partnership line, so footage of
    real people never looks like a real ad or an endorsement. Nothing else can use it."""
    return (isinstance(c, dict) and c.get("example_demo") is True and str(c.get("id") or "").startswith("example-")
            and str(c.get("brand") or "").startswith("Example "))


def screen_line_ok(text, c):
    """The on-screen line is a real disclosure, or, for the skill's own example only, the demo line."""
    if example_demo(c):
        return " ".join(str(text or "").split()).lower().startswith(DEMO_LINE)
    return says_paid(text)


def _num(v, minimum=0.0):
    return is_num(v, minimum)


def paid_fields(c):
    """The fields that make a campaign a paid one: someone pays per view, so own_content can't apply."""
    out = []
    if isinstance(c.get("marketplace"), str) and c["marketplace"].strip():
        out.append(f"a marketplace ({c['marketplace']})")
    if isinstance(c.get("brand"), str) and c["brand"].strip():
        out.append(f"a brand ({c['brand']}; for your own content leave brand out)")
    plats = c.get("platforms") if isinstance(c.get("platforms"), dict) else {}
    if any(isinstance(v, dict) and is_num(v.get("rate_per_1k")) and v["rate_per_1k"] > 0 for v in plats.values()):
        out.append("a rate per 1,000 views")
    for k, what in (("min_payout", "a minimum payout"), ("cap_per_clip", "a cap per clip"), ("min_views", "a view minimum"),
                    ("budget_total", "a budget"), ("budget_remaining", "a budget"), ("fee_pct", "a marketplace fee")):
        v = c.get(k)
        per_plat = any(isinstance(x, dict) and is_num(x.get(k)) and x[k] > 0 for x in plats.values())
        if ((is_num(v) and v > 0) or per_plat) and what not in out:
            out.append(what)
    return out


def watermark_spec(wm, base_dir="."):
    """The brief's watermark as {"text" or "image", "position", "opacity", "scale"}, or None.
    A plain string is text at the bottom. An image path is read next to campaign.json."""
    if isinstance(wm, str) and wm.strip():
        return {"text": wm.strip(), "image": None, "position": "bottom", "opacity": 0.85, "scale": None}
    if not isinstance(wm, dict):
        return None
    text = wm.get("text") if isinstance(wm.get("text"), str) and wm["text"].strip() else None
    image = wm.get("image") if isinstance(wm.get("image"), str) and wm["image"].strip() else None
    if not text and not image:
        return None
    pos = wm.get("position") if wm.get("position") in WM_POSITIONS else ("bottom-right" if image else "bottom")
    op = wm.get("opacity") if is_num(wm.get("opacity")) and 0.1 <= wm["opacity"] <= 1 else 0.85
    sc = wm.get("scale") if is_num(wm.get("scale")) and 0.05 <= wm["scale"] <= 0.6 else (0.22 if image else None)
    full = None
    if image:
        full = image if os.path.isabs(image) else os.path.join(base_dir, image)
    return {"text": text.strip() if text else None, "image": image, "image_path": full, "position": pos,
            "opacity": op, "scale": sc}


def check_campaign(c, path="campaign.json", base_dir="."):
    """Every problem with a campaign file: a list of (level, field, message)."""
    out = []

    def bad(field, msg, level="error"):
        out.append((level, field, msg))

    if not isinstance(c, dict):
        return [("error", "campaign", f"{path} must hold one JSON object with the campaign's rules")]
    own = c.get("own_content") is True
    if c.get("example_demo") is not None and not example_demo(c):
        bad("example_demo", "only the skill's own made-up example uses this (id \"example-...\", brand \"Example ...\"). "
            "Take it out: a real campaign's clips carry a real disclosure")
    if c.get("own_content") is not None and not isinstance(c.get("own_content"), bool):
        bad("own_content", "true only when the creator posts their own content on their own accounts and nobody "
            "pays the poster; leave it out otherwise")
    if own:
        paid = paid_fields(c)
        if paid:
            bad("own_content", "own_content is for your own content on your own accounts, with nobody paying per view. "
                f"This campaign has {', '.join(paid)}, so it pays per view and every clip is disclosed. Take "
                "own_content out (a creator who pays clippers runs a normal campaign: their clips carry #ad)")
        if not isinstance(c.get("promotes_own_business"), bool):
            bad("promotes_own_business", "ask the user: do these clips promote your own product, service or business "
                "(true), or are they just your show or stream (false)? Only true turns on TikTok's \"Your brand\" "
                "label")
    if not valid_id(c.get("id")):
        bad("id", "give the campaign a short id of lowercase letters, digits and dashes (like \"orbit-hour-nov\"): "
            "the ledger files every post under it")
    if not isinstance(c.get("name"), str) or not c.get("name", "").strip():
        bad("name", "the campaign's name as the marketplace shows it")
    if not own and (not isinstance(c.get("brand"), str) or not c.get("brand", "").strip()):
        bad("brand", "the brand or creator who pays for the views (it goes into the on-screen disclosure)")
    plats = c.get("platforms")
    if not isinstance(plats, dict) or not plats:
        bad("platforms", "list the platforms the campaign pays for, each with its rate per 1,000 views, like "
            "{\"TIKTOK\": {\"rate_per_1k\": 1.0}}")
    else:
        for p, v in plats.items():
            if p not in PLATFORMS:
                bad("platforms", f"{p}: this skill posts to {', '.join(PLATFORMS)}. Leave {p} out")
            elif not isinstance(v, dict) or not _num(v.get("rate_per_1k")):
                bad("platforms", f"{p}: rate_per_1k must be a number (dollars per 1,000 views, 0 or more)")
            else:
                for k in ("min_payout", "cap_per_clip", "min_views"):
                    if v.get(k) is not None and not _num(v.get(k)):
                        bad("platforms", f"{p}: {k} must be a number of 0 or more, or left out to use the campaign's")
                if v.get("cap_per_clip") == 0:
                    bad("platforms", f"{p}: cap_per_clip 0 would pay nothing; leave it out when there is no cap")
                if _num(v.get("min_payout")) and _num(v.get("cap_per_clip")) and v["cap_per_clip"] and \
                        v["min_payout"] > v["cap_per_clip"]:
                    bad("platforms", f"{p}: the cap is lower than the minimum payout; check both numbers in the brief")
    for k in ("min_payout", "cap_per_clip", "budget_total", "budget_remaining", "min_views"):
        if c.get(k) is not None and not _num(c.get(k)):
            bad(k, "must be a number of 0 or more, or left out (null)")
    if c.get("cap_per_clip") == 0:
        bad("cap_per_clip", "0 would pay nothing on every clip. When the brief sets no cap, leave it null")
    if c.get("budget_checked_at") is not None and not parse_time(c.get("budget_checked_at")):
        bad("budget_checked_at", "when the remaining budget was read on the campaign page, like 2026-11-15T14:00:00Z")
    if c.get("fee_pct") is not None and not (_num(c.get("fee_pct")) and c["fee_pct"] < 100):
        bad("fee_pct", "the marketplace fee in percent (0 to 99), or null for the default of 10")
    for k in ("window_days", "days_live", "submit_within_minutes"):
        if c.get(k) is not None and not (_num(c.get(k), 1) and float(c[k]).is_integer()):
            bad(k, "must be a whole number, or null for the default")
    if c.get("window_from") is not None and c.get("window_from") not in ("threshold", "post"):
        bad("window_from", "\"threshold\" (views count from the day the clip crosses the payout threshold, as on "
            "Content Rewards) or \"post\" (from posting), or null")
    if c.get("max_overlap") is not None and not (_num(c.get("max_overlap")) and c["max_overlap"] <= 1):
        bad("max_overlap", "a share from 0 to 1 (0.5 means two accounts may share at most half a clip's footage)")
    if (_num(c.get("min_payout")) and _num(c.get("cap_per_clip")) and c.get("cap_per_clip")
            and c["min_payout"] > c["cap_per_clip"]):
        bad("cap_per_clip", "the cap per clip is lower than the minimum payout; check both numbers in the brief")

    cap = c.get("caption")
    if not isinstance(cap, dict):
        bad("caption", "what every caption must hold: {\"disclosure\": \"#ad\", \"hashtags\": [...], \"mentions\": "
            "[...], \"links\": [...]}. Use empty lists when the brief asks for none")
        cap = {}
    disc = cap.get("disclosure")
    if not isinstance(disc, str) or not disc.strip():
        if not own:
            bad("caption.disclosure", "a campaign post always starts its caption with a disclosure. Use \"#ad\" "
                "unless the brief names a stronger one")
    elif disc.strip().lower() in WEAK_TAGS:
        bad("caption.disclosure", f"{disc} doesn't tell viewers the post is paid. Use \"#ad\"")
    elif disc.strip().lower() not in CAPTION_DISCLOSURES and not says_paid(disc):
        bad("caption.disclosure", f"\"{disc}\" doesn't say the post is paid. Use \"#ad\"")
    for k, check, what in (("hashtags", hashtags, "a hashtag like #orbithour"),
                           ("mentions", mentions, "a handle like @example.orbit")):
        v = cap.get(k, [])
        if v is None:
            continue
        if not isinstance(v, list) or not all(isinstance(x, str) and check(x) == [x] for x in v):
            bad(f"caption.{k}", f"a list where each item is {what} (an empty list when the brief asks for none)")
    lk = cap.get("links", [])
    if lk is not None and (not isinstance(lk, list) or not all(isinstance(x, str) and x.strip() for x in lk)):
        bad("caption.links", "a list of links the caption must hold (an empty list when the brief asks for none)")
    if c.get("links_where") is not None and c.get("links_where") not in ("caption", "bio", "either"):
        bad("links_where", "where the brief wants its link: \"caption\", \"bio\" or \"either\", or null (caption)")
    if c.get("links_where") in ("bio", "either") and not (isinstance(c.get("bio"), str) and c["bio"].strip()):
        bad("bio", "the brief accepts the link in the bio: put that link in \"bio\"")
    if any(isinstance(h, str) and h.lower() in ("#ad", "#ads", "#sponsored") for h in c.get("banned") or []):
        bad("banned", "the brief bans the #ad tag. It is never removed: every campaign post is disclosed")

    scr = c.get("on_screen")
    if not isinstance(scr, dict):
        if not own:
            bad("on_screen", "what goes on the video: {\"disclosure\": \"Paid partnership with <brand>\", "
                "\"disclosure_seconds\": 4, \"watermark\": null}")
        scr = {}
    sd = scr.get("disclosure")
    if not isinstance(sd, str) or not sd.strip():
        if not own:
            bad("on_screen.disclosure", "every campaign clip shows a disclosure in its first seconds, like \"Ad\" or "
                f"\"Paid partnership with {c.get('brand') or '<brand>'}\"")
    elif not screen_line_ok(sd, c):
        bad("on_screen.disclosure", f"\"{sd}\" doesn't say the clip is paid. Use \"Ad\" or \"Paid partnership with "
            f"{c.get('brand') or '<brand>'}\"")
    elif len(sd) > 48:
        bad("on_screen.disclosure", "keep it to 48 characters so it reads in the first seconds")
    secs = scr.get("disclosure_seconds", 4)
    if secs is not None and (not _num(secs, 2) or secs > 10):
        bad("on_screen.disclosure_seconds", "how long the disclosure shows at the start: 2 to 10 seconds")
    wm = scr.get("watermark")
    if wm is not None:
        spec = watermark_spec(wm, base_dir)
        if isinstance(wm, str):
            if not wm.strip() or len(wm) > 40:
                bad("on_screen.watermark", "the watermark text the brief asks for (40 characters at most), or null")
        elif not isinstance(wm, dict) or spec is None:
            bad("on_screen.watermark", "text (\"EXAMPLE ORBIT\"), or {\"image\": \"logo.png\", \"position\": "
                "\"bottom-right\"} for a logo the brief supplies, or null")
        else:
            if wm.get("position") is not None and wm.get("position") not in WM_POSITIONS:
                bad("on_screen.watermark", f"position is one of {', '.join(WM_POSITIONS)}")
            if spec["text"] and len(spec["text"]) > 40:
                bad("on_screen.watermark", "the watermark text is 40 characters at most")
            if spec["image"]:
                if not spec["image"].lower().endswith(IMAGE_TYPES):
                    bad("on_screen.watermark", "the logo is a PNG (best: transparent), JPEG or WebP file")
                elif not os.path.isfile(spec["image_path"]):
                    bad("on_screen.watermark", f"logo file {spec['image']} not found next to the campaign file. Save "
                        "the file the brief supplies there")
    if c.get("bio") is not None and not (isinstance(c["bio"], str) and c["bio"].strip()):
        bad("bio", "what the brief wants in the profile bio, or null")

    ln = c.get("length")
    if not isinstance(ln, dict) or not _num(ln.get("min_s")) or not _num(ln.get("max_s")) or ln["max_s"] <= ln["min_s"]:
        bad("length", "{\"min_s\": 15, \"max_s\": 60}: the shortest and longest clip the campaign accepts")
    if c.get("aspect", "9:16") not in ("9:16", "any", None):
        bad("aspect", "\"9:16\" (vertical) or \"any\"")
    ft = c.get("footage")
    if not isinstance(ft, dict) or not isinstance(ft.get("allowed"), str) or not ft["allowed"].strip():
        bad("footage", "which footage may be used: {\"allowed\": \"supplied only\", \"files\": [\"interview.mp4\"], "
            "\"sources\": [\"<link from the brief>\"]}")
    else:
        if ft.get("files") is not None and (not isinstance(ft.get("files"), list) or not all(
                isinstance(x, str) and x.strip() for x in ft.get("files"))):
            bad("footage.files", "a list of the source file names the campaign supplied (empty when any allowed source)")
        if ft.get("recency_days") is not None and not _num(ft.get("recency_days"), 1):
            bad("footage.recency_days", "how new the footage must be, in days, or null")
        dates = ft.get("dates")
        if dates is not None and (not isinstance(dates, dict) or not all(
                isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) for v in dates.values())):
            bad("footage.dates", "{\"<source file>\": \"YYYY-MM-DD\"}: the day each stream or video was recorded, as the "
                "user says (never the file's date on disk)")
    aud = c.get("audience")
    if aud is not None:
        if not isinstance(aud, dict) or not isinstance(aud.get("geo"), str) or not (
                _num(aud.get("min_share")) and aud["min_share"] <= 1):
            bad("audience", "{\"geo\": \"US\", \"min_share\": 0.3} when the brief sets a minimum audience share, or null")
    if c.get("engagement_min") is not None and not (_num(c.get("engagement_min")) and c["engagement_min"] < 1):
        bad("engagement_min", "the minimum engagement as a share of views (0.03 for 3%), or null")
    if c.get("proof") is not None and (not isinstance(c.get("proof"), list) or not all(isinstance(x, str) for x in c["proof"])):
        bad("proof", "a list of what the campaign wants as proof (screenshots, analytics), or an empty list")
    if not isinstance(c.get("approval_before_posting", False), (bool, type(None))):
        bad("approval_before_posting", "true when the brand must approve each clip before it is posted")
    rs = c.get("required_sound")
    if rs is not None and sound_spec(rs) is None:
        bad("required_sound", "the sound the brief requires (its name), or {\"name\": ..., \"platforms\": [\"TIKTOK\"], "
            "\"volume\": \"5 to 10%\"}, or null")
    elif isinstance(rs, dict) and any(str(p).upper() not in PLATFORMS for p in rs.get("platforms") or []):
        bad("required_sound", f"platforms is a list of {', '.join(PLATFORMS)}")
    if c.get("banned") is not None and (not isinstance(c.get("banned"), list) or not all(
            isinstance(x, str) and x.strip() for x in c.get("banned"))):
        bad("banned", "a list of words, hashtags or topics the brief bans (empty when none)")
    if c.get("boosting_allowed") is not None and not isinstance(c["boosting_allowed"], bool):
        bad("boosting_allowed", "true only when the brief allows paid boosting; leave it out otherwise")
    return out


def brief_flags(c, base_dir, brief_path=None):
    """(the brief text or None, its path, hide-the-ad sentences, disclosure conflicts, engagement or
    location sentences, sentences about the disclosure the agent reads itself)."""
    path = brief_path or (c.get("brief_file") if isinstance(c, dict) else None)
    if not isinstance(path, str) or not path:
        return None, None, [], [], [], []
    full = path if os.path.isabs(path) or brief_path else os.path.join(base_dir, path)
    reading(full)
    try:
        with open(full, encoding="utf-8-sig", errors="replace") as fh:
            text = fh.read()
    except FileNotFoundError:
        die(f"{path} not found (the campaign brief text)")
    except IsADirectoryError:
        die(f"{path} is a folder; give the brief as a text file")
    reading(None)
    conflict = find_phrases(text, DISCLOSURE_CONFLICT)
    in_conflict = {s for s, _ in conflict}
    hide = [(s, m) for s, m in hide_ad_hits(text, brief=True) if s not in in_conflict]
    bait = asks_for(text, ENGAGEMENT_BAIT + ENGAGEMENT_SOFT + LOCATION_TRICKS)
    # Shown whatever own_content says: a brief that talks about hiding the ad is a paid campaign.
    read = read_yourself(text, {s for s, _ in hide} | in_conflict | {s for s, _ in bait})
    return text, full, hide, conflict, bait, read


def load(path, brief_path=None):
    """The campaign (optional fields filled with their defaults), its problems, the brief's flags and
    a version stamp. Used by the other scripts too."""
    raw = read_json(path, "the campaign file")
    base = os.path.dirname(os.path.abspath(path))
    issues = check_campaign(raw, rel(path), base)
    text, full, hide, conflict, bait, read = brief_flags(raw, base, brief_path) if isinstance(raw, dict) else (
        None, None, [], [], [], [])
    if isinstance(raw, dict) and raw.get("own_content") is True and (hide or conflict):
        issues.append(("error", "own_content", "the brief talks about the ad disclosure, so it is a paid campaign: "
                       "own_content can't be used. Take it out; every clip is disclosed"))
    with open(path, "rb") as fh:
        h = hashlib.sha256(fh.read())
    if text is not None:
        h.update(text.encode("utf-8", "surrogatepass"))
    c = with_defaults(raw) if isinstance(raw, dict) else raw
    if isinstance(c, dict):
        c["watermark_spec"] = watermark_spec((raw.get("on_screen") or {}).get("watermark") if isinstance(
            raw.get("on_screen"), dict) else None, base)
    return {"campaign": c, "raw": raw, "issues": issues, "brief": text, "brief_path": full, "hide": hide,
            "conflict": conflict, "bait": bait, "read": read, "version": h.hexdigest()[:10], "base_dir": base}


def rate_line(c):
    plats = c.get("platforms") or {}
    cur = c.get("currency", "USD")
    out = []
    for p, v in plats.items():
        if p not in LIMITS or not isinstance(v, dict):
            continue
        rate, mn, cap, mv = terms(c, p)
        bits = [f"{LIMITS[p]['label']} {money(rate, cur)} per 1,000 views"]
        own = [k for k in ("min_payout", "cap_per_clip", "min_views") if v.get(k) is not None]
        if own:
            bits.append("(" + ", ".join(
                [f"minimum {money(mn, cur)}" if "min_payout" in own else "",
                 f"cap {money(cap, cur)}" if "cap_per_clip" in own and cap else "",
                 f"at least {mv:,} views" if "min_views" in own else ""]).strip(", ").replace(", ,", ",") + ")")
        out.append(" ".join(b for b in bits if b and b != "()"))
    return ", ".join(out)


def window_text(c):
    days = int(c.get("window_days"))
    if c.get("window_from") == "threshold":
        return f"views count for {days} days from the day a clip crosses the payout threshold"
    return f"views count for {days} days after posting"


def checklist(info):
    """The numbered checklist, as lines of Markdown."""
    c = info["campaign"]
    own = c.get("own_content") is True
    cur = c.get("currency", "USD")
    cap, scr = c.get("caption") or {}, c.get("on_screen") or {}
    ln, ft = c.get("length") or {}, c.get("footage") or {}
    items = []
    items.append(f"**Platforms and rates:** {rate_line(c) or 'none given'}.")
    pay = []
    pay.append(f"minimum payout per clip {money(c['min_payout'], cur)}" if c.get("min_payout") else "no minimum payout given")
    if c.get("min_views"):
        pay.append(f"minimum {c['min_views']:,} views per clip")
    pay.append(f"cap per clip {money(c['cap_per_clip'], cur)}" if c.get("cap_per_clip") else "no cap per clip given")
    pay.append(f"marketplace fee {c['fee_pct']:g}%")
    if c.get("budget_total"):
        pay.append(f"total budget {money(c['budget_total'], cur)}")
    if c.get("budget_remaining") is not None:
        when = parse_time(c.get("budget_checked_at"))
        pay.append(f"{money(c['budget_remaining'], cur)} left" + (f" when checked {when:%d %b %H:%M} UTC" if when else ""))
    items.append("**Payout:** " + "; ".join(pay) + ". When the budget runs out, views stop paying.")
    need = [f"{LIMITS[p]['label']} {threshold_views(c, p):,}" for p in (c.get("platforms") or {})
            if p in LIMITS and threshold_views(c, p)]
    if need:
        items.append("**Pays from:** " + ", ".join(need) + " views per clip; under that a clip earns nothing.")
    req = [f"starts with **{cap['disclosure']}**"] if cap.get("disclosure") else (
        ["no paid disclosure (your own content on your own accounts)"] if own else [])
    for k in ("hashtags", "mentions"):
        if cap.get(k):
            req.append(f"{k}: " + ", ".join(cap[k]))
    where = c.get("links_where") or "caption"
    if cap.get("links"):
        req.append("links: " + ", ".join(cap["links"]) + {"caption": "", "bio": " (in the bio, not the caption)",
                                                          "either": " (in the caption or the bio)"}[where])
    items.append("**Every caption:** " + "; ".join(req) + ".")
    wm = c.get("watermark_spec")
    onscr = []
    if scr.get("disclosure"):
        onscr.append(f"\"{scr['disclosure']}\" for the first {scr.get('disclosure_seconds') or 4:g} seconds, at the "
                     "top inside the app's safe area")
    elif own:
        onscr.append("no paid disclosure (your own content)")
    if wm and wm.get("image"):
        onscr.append(f"the logo {wm['image']} {wm['position']} for the whole clip")
    elif wm:
        onscr.append(f"watermark text \"{wm['text']}\" for the whole clip")
    items.append(f"**On screen:** {'; '.join(onscr) or 'nothing required'}.")
    items.append(f"**Profile bio:** {c['bio']} (set in each app before posting)." if c.get("bio")
                 else "**Profile bio:** nothing required.")
    items.append(f"**Length:** {ln.get('min_s'):g} to {ln.get('max_s'):g} seconds; shape {c.get('aspect', '9:16')}."
                 if _num(ln.get("min_s")) and _num(ln.get("max_s")) else "**Length:** not given.")
    foot = f"{ft.get('allowed', 'not given')}"
    if ft.get("files"):
        foot += "; files: " + ", ".join(ft["files"])
    if ft.get("sources"):
        foot += "; from: " + ", ".join(ft["sources"])
    if ft.get("recency_days"):
        foot += f"; recorded in the last {ft['recency_days']:g} days only (the day of each stream is checked)"
    if isinstance(ft.get("dates"), dict) and ft["dates"]:
        foot += "; recorded: " + ", ".join(f"{k} on {v}" for k, v in ft["dates"].items())
    items.append(f"**Footage:** {foot}.")
    aud = c.get("audience")
    items.append(f"**Audience:** at least {aud['min_share']:.0%} of viewers in {place_name(aud['geo'])}, or the whole clip can be "
                 "rejected after it has views. Post from accounts whose audience is there." if isinstance(aud, dict)
                 else "**Audience:** no country floor given.")
    eng = c.get("engagement_min")
    items.append(f"**Engagement:** at least {eng:.0%} of views (likes, comments and shares)." if eng
                 else "**Engagement:** no floor given.")
    items.append(f"**Time live:** stays public and unchanged for {int(c['days_live'])} days; {window_text(c)}.")
    items.append("**Proof to keep:** " + ("; ".join(c["proof"]) if c.get("proof") else "nothing extra named")
                 + ". Screenshots at 48 hours, 72 hours and 7 days per post either way.")
    items.append("**Approval:** the brand approves each clip before it is posted (the plan writes a packet to send)."
                 if c.get("approval_before_posting") else "**Approval:** no approval step before posting.")
    snd = c.get("required_sound")
    if snd:
        plats = ", ".join(LIMITS[p]["label"] for p in snd["platforms"] if p in LIMITS)
        items.append(f"**Sound:** \"{snd['name']}\"" + (f" at {snd['volume']}" if snd.get("volume") else "")
                     + f" on {plats}. No posting API can add a sound, so those posts are made by hand, with the sound "
                     "added before posting.")
    else:
        items.append("**Sound:** no required sound.")
    items.append("**Banned:** " + (", ".join(c["banned"]) if c.get("banned") else "nothing named") + ".")
    items.append(f"**Submitting:** within {int(c['submit_within_minutes'])} minutes of posting; one post goes into one "
                 "campaign, once.")
    if not own:
        items.append(f"**Accounts:** post only from accounts connected and verified in "
                     f"{c.get('marketplace') or 'the marketplace'}; posts from other accounts are rejected.")
    items.append(f"**Overlap:** two accounts may share at most {c['max_overlap']:.0%} of a clip's footage; each "
                 "account gets its own edit.")
    return items


def report(info, path):
    c = info["campaign"] if isinstance(info["campaign"], dict) else {}
    lines = [f"# Campaign checklist: {c.get('name', '(no name)')}", ""]
    lines.append(f"Campaign id `{c.get('id', '?')}`, " + ("your own content on your own accounts" if c.get("own_content")
                 is True else f"brand {c.get('brand', '?')}, {c.get('marketplace') or 'marketplace not given'}")
                 + f". Brief dated {c.get('brief_date') or 'not given'}, checklist version `{info['version']}` (changes "
                 "when the campaign file or the brief changes).")
    lines.append("")
    if example_demo(info.get("raw")):
        lines += ["**EXAMPLE ONLY: a made-up demo campaign.** Its clips show \"EXAMPLE ONLY: not a real ad\" where a real "
                  "campaign's clips show their paid-partnership line. A real campaign can't use this.", ""]
    errs = [i for i in info["issues"] if i[0] == "error"]
    if errs:
        lines += [f"**{len(errs)} thing(s) to fix in {rel(path)} before cutting clips:**", ""]
        lines += [f"- `{f}`: {m}" for _, f, m in errs] + [""]
    if isinstance(info["campaign"], dict) and not errs:
        lines += [f"{n}. {t}" for n, t in enumerate(checklist(info), 1)]
        lines.append("")
    if info["conflict"]:
        lines += ["## Conflicts with the disclosure rule", "",
                  "The brief forbids the disclosure on the video. The skill keeps it on screen in the first seconds: "
                  "the marketplace and advertising law require it, and the skill doesn't make undisclosed campaign "
                  "posts. Ask the campaign team in writing whether a short \"Ad\" for the first 2 seconds is "
                  "accepted, or skip this campaign.", ""]
        lines += [f"- \"{s}\"" for s, _ in info["conflict"]] + [""]
    if info["hide"]:
        lines += ["## Never followed", "",
                  "The brief asks to hide that the clip is paid. That is never done: every clip keeps the on-screen "
                  "disclosure, the caption disclosure and the platform's paid-partnership setting. Hiding it breaks "
                  "marketplace rules and advertising law (FTC in the US, CMA in the UK, consumer law in the EU).", ""]
        lines += [f"- \"{s}\"" for s, _ in info["hide"]] + [""]
    if info.get("read"):
        lines += ["## Read these sentences yourself", "",
                  "These sentences talk about the disclosure next to a \"no\" or a rejection, and the checks can't tell "
                  "for sure which way they point. Read each one: if it asks to hide or drop the disclosure, it is never "
                  "followed, the same as above. Every clip stays disclosed either way.", ""]
        lines += [f"- \"{s}\"" for s in info["read"]] + [""]
    if info["bait"]:
        lines += ["## Never done", "", "The brief asks for bought or arranged engagement or location tricks. The skill "
                  "never does this; it is a permanent ban on the marketplaces and against platform rules.", ""]
        lines += [f"- \"{s}\"" for s, _ in info["bait"]] + [""]
    if c.get("boosting_allowed") is True:
        lines += ["Paid boosting is allowed by this brief; the skill never boosts posts itself.", ""]
    lines += ["The campaign's own view count decides what is paid. Rates are low (often about $1 per 1,000 views) "
              "and most clips earn little; nothing here promises income.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Check a clipping campaign and print its checklist.")
    ap.add_argument("campaign")
    ap.add_argument("--brief", help="the brief text as pasted (overrides brief_file in the campaign)")
    ap.add_argument("--out", help="where to write the checklist (default: checklist.md next to the campaign file)")
    a = ap.parse_args()
    info = load(a.campaign, a.brief)
    md = report(info, a.campaign)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.campaign)), "checklist.md")
    write_text(out, md)
    print(md.rstrip())
    print()
    errs = [i for i in info["issues"] if i[0] == "error"]
    flags = len(info["hide"]) + len(info["bait"]) + len(info["conflict"]) + len(info["read"])
    print(f"{len(errs)} error(s), {flags} brief sentence(s) flagged -> {rel(out)}")
    if info["read"]:
        print(f"read yourself: {len(info['read'])} sentence(s) about the disclosure the checks can't place. Read each "
              "one; if it asks to hide the ad, it is never followed")
    if info["conflict"]:
        print("conflict: the brief forbids the on-screen disclosure, which the skill always keeps. Ask the campaign "
              "team in writing, or skip this campaign")
    if not errs:
        print("next: show this checklist to the user and wait for them to confirm it before cutting clips")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    guard(main)
