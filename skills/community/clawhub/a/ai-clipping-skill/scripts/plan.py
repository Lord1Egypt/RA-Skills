#!/usr/bin/env python3
"""The plan page for a campaign batch: every account's clip, caption, checks, settings, expected
earnings and the steps WoopSocial can't do. Then the request, the posted record and the
submission sheet with its 30-minute deadlines.

    python3 scripts/plan.py clipjob.json                       # check everything, write plan.md,
                                                               #   plan.html, requests/, by-hand/
                                                               #   and approval/ when the brief asks
    python3 scripts/plan.py clipjob.json --media media.json    # fill in the uploaded mediaIds:
                                                               #   {"<clip>": {"mediaId", "sha256"}}
    python3 scripts/plan.py clipjob.json --posted requests/<name>.json <postId>
                                                               # right after posts_create: record it
    python3 scripts/plan.py clipjob.json --status status.json [<postId>]
                                                               # the saved posts_get reply: links,
                                                               #   live times, the submission sheet
    python3 scripts/plan.py clipjob.json --posted-by-hand <job post id> <post url> [--at TIME]
                                                               # a post the user made in the app
    python3 scripts/plan.py clipjob.json --failed <job post id>
                                                               # a post that failed to publish: the
                                                               #   next plan sends it again
    python3 scripts/plan.py clipjob.json --remember-accounts   # save the accounts' choices as
                                                               #   suggestions for the next campaign

What it writes, next to clipjob.json:
  plan.md, plan.html   every post as it will go out, with every check. Show this before posting.
  requests/*.json      one WoopSocial request: one post with a child per connected account, each
                       with its own clip and caption. Only written when there are no errors.
  by-hand/<post>.md    for accounts that aren't connected (or need a sound): the clip, caption,
                       settings and steps, in the order they are done.
  approval/<post>.md   when the brief asks for the brand's approval: the packet to send them.
  submit.md            the submission sheet: each post's link, the clock time its 30 minutes run
                       out, what to do in the apps inside that window, when to take screenshots.
And the one ledger shared by every campaign (~/.ai-clipping/ledger.json, or AI_CLIPPING_LEDGER, or
--ledger): every post that went out, with its file fingerprint and source footage, so no edit goes
out twice or into a second campaign, whatever folder each campaign lives in.

Every planning run starts by removing the plan, the requests, the by-hand and approval pages of the
run before (only files this script wrote), so a plan that stops on an error never leaves an old
request that could still be sent. Posting is always "now": a campaign post has to be submitted
within 30 minutes of going live. Exit code 0 when there are no errors, 1 otherwise.
"""
import argparse, base64, datetime, html, math, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_clips import PRIVACY_WORDS, check_job  # noqa: E402
from campaign import example_demo  # noqa: E402

DEMO_NOTE = ("EXAMPLE ONLY: a made-up demo campaign. The brand, the accounts and the links are invented, nothing "
             "here is a real ad, and NASA and the people in the footage endorse nothing.")
from cliplib import (place_name, LIMITS, MB, account_key, clock, die, guard, iso, load_saved_accounts,  # noqa: E402
                     load_zone, money, now_utc, parse_time, parse_user_time, payout, post_items, post_key, read_json,
                     rel, save_ledger, sha256, short_link, stamp, terms, threshold_views, unwrap_reply, user_home,
                     write_json, write_text)

MARK = "<!-- written by plan.py; it replaces this file on every run -->"
SHOT_HOURS = (48, 72, 168)   # screenshot times after a post goes live, merged with any the brief names


def esc(s):
    return html.escape(str(s), quote=True)


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def own(camp):
    return camp.get("own_content") is True


def your_brand(camp):
    """Your own content that promotes your own product, service or business: TikTok's "Your brand"
    label. Your own show or stream without that gets no content disclosure label."""
    return own(camp) and camp.get("promotes_own_business") is True


# ---- what each post needs

def settings_bits(r, camp):
    acc, p = r["account"], r["platform"]
    bits = []
    if p == "TIKTOK":
        bits.append("seen by " + PRIVACY_WORDS.get(acc.get("privacyLevel"), "NOT CHOSEN"))
        for k, w in (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches")):
            v = acc.get(k)
            bits.append(f"{w} {'on' if v else 'off'}" if isinstance(v, bool) else f"{w} NOT CHOSEN")
        bits.append("labelled \"Your brand\" (promotional content)" if your_brand(camp)
                    else "no content disclosure label (your own content)" if own(camp)
                    else "labelled \"Paid partnership\" (branded content on)")
    if p == "INSTAGRAM":
        bits.append("Reel")
        if not own(camp):
            bits.append("paid partnership label: you turn it on in the app after posting")
    if p == "YOUTUBE":
        bits.append(acc.get("privacy") or "privacy NOT CHOSEN")
        k = acc.get("madeForKids")
        bits.append(("made for kids" if k else "not made for kids") if isinstance(k, bool) else "made for kids NOT CHOSEN")
        if not own(camp):
            bits.append("\"includes paid promotion\": you tick it in YouTube Studio")
    if r.get("ai") is True:
        bits.append("AI label: set by hand in YouTube Studio" if p == "YOUTUBE" else "AI label on (sent with the post)")
    elif r.get("ai") is False:
        bits.append("no AI label")
    return bits


def sound_for(r, camp):
    snd = camp.get("required_sound")
    return snd if snd and r["platform"] in snd["platforms"] else None


def before_steps(r, camp):
    """Done before the post goes out: they can't be added afterwards, or they would eat into the
    30 minutes."""
    steps = []
    snd = sound_for(r, camp)
    if snd:
        steps.append(f"{LIMITS[r['platform']]['label']}: the brief requires the sound \"{snd['name']}\""
                     + (f" at {snd['volume']} volume" if snd.get("volume") else "") + ". No posting API can add a "
                     "sound, and it can't be added after posting, so this post is made by hand with the sound added "
                     "in the app before you post.")
    if camp.get("bio"):
        steps.append(f"Profile bio of {r['name']}{' ' + r['handle'] if r['handle'] else ''}: {camp['bio']} (set it now, "
                     "keep it while the clip is live).")
    return steps


def window_steps(r, camp):
    """What WoopSocial can't set and is only possible once the post is live: inside the 30 minutes."""
    p = r["platform"]
    steps = []
    if p == "INSTAGRAM" and not own(camp):
        steps.append("Instagram: edit the Reel in the app and turn on the paid partnership label. WoopSocial can't set "
                     f"it. Tagging {camp.get('brand', 'the brand')} as partner is optional and may need their approval; "
                     "the label itself is what counts.")
    if p == "YOUTUBE" and not own(camp):
        steps.append("YouTube: in YouTube Studio open the Short's details and tick that it includes paid promotion. "
                     "WoopSocial can't set it.")
    if p == "YOUTUBE" and r.get("ai") is True:
        steps.append("YouTube: in YouTube Studio answer Yes to \"Altered or synthetic content\". WoopSocial can't set it.")
    return steps


def is_by_hand(r, camp):
    return not r["connected"] or bool(sound_for(r, camp))


def earnings_text(r, camp):
    rate, mn, cap, mv = terms(camp, r["platform"])
    if rate <= 0:
        return "No rate for this platform in the campaign."
    cur = camp.get("currency", "USD")
    fee = camp["fee_pct"]
    parts = [f"{money(rate, cur)} per 1,000 views, {fee:g}% fee."]
    need = threshold_views(camp, r["platform"])
    if need:
        parts.append(f"Pays nothing under {need:,} views.")
    shown = []
    for v in (1000, 10000, 100000):
        _, paid, why = payout(v, rate, mn, cap, fee, mv, cur)
        shown.append(f"{v:,} views: {money(paid, cur)}" + (" (capped)" if why == "capped" else ""))
    parts.append("; ".join(shown) + ".")
    if cap:
        parts.append(f"Cap {money(cap, cur)} per clip, reached at {int(cap / rate * 1000):,} views.")
    return " ".join(parts)


def window_note(camp):
    days = int(camp["window_days"])
    if camp.get("window_from") == "threshold":
        return f"Views count for {days} days from the day a clip crosses the payout threshold"
    return f"Views count for {days} days after posting"


def shot_hours(camp):
    hours = set(SHOT_HOURS)
    for p in camp.get("proof") or []:
        for n, unit in re.findall(r"(\d+)\s*(h|hours?|d|days?)\b", str(p), re.I):
            hours.add(int(n) * (24 if unit.lower().startswith("d") else 1))
    return sorted(h for h in hours if 0 < h <= 24 * 60)


def hours_label(h):
    return f"{h // 24}d" if h % 24 == 0 and h >= 168 else f"{h}h"


def before_you_post(m):
    """Said once, at the top of the plan: account verification, the audience and engagement rules
    with what helps, the budget."""
    c = m["campaign"]
    out = []
    if not own(c):
        out.append(f"Post only from accounts connected and verified in {c.get('marketplace') or 'the marketplace'}; "
                   "posts from any other account are rejected.")
    aud = c.get("audience")
    if isinstance(aud, dict):
        out.append(f"At least {aud['min_share']:.0%} of each clip's viewers must be in {place_name(aud['geo'])}, or the whole clip "
                   f"is rejected. What helps: post from the accounts whose audience is already mostly in {place_name(aud['geo'])} "
                   "(the app's audience countries show it), post when that audience is awake, and write the caption "
                   "for them. Never a VPN or location trick: that gets accounts banned.")
    if c.get("engagement_min"):
        out.append(f"Engagement must reach {c['engagement_min']:.0%} of views. What helps: a hook that pays off, a "
                   "caption that invites a real reply, and answering comments in the first hour. Never engagement "
                   "groups or bought likes: that is a permanent ban.")
    return out


# ---- the request

def media_id(media, f):
    return media[f]["mediaId"] if media and media.get(f) else f"<mediaId of {f}>"


def child(r, media, camp):
    acc, p = r["account"], r["platform"]
    t = {"platform": p, "socialAccountId": acc["socialAccountId"]}
    if p == "TIKTOK":
        # A campaign post is a paid partnership: TikTok's branded content label is always on. Your own
        # content on your own account is "Your brand" (promotional content) only when it promotes your
        # own product, service or business; your own show or stream gets no label.
        # autoAddMusic is required by WoopSocial's schema for every TikTok child, so it is sent as false.
        t.update(postType="VIDEO", postMode="DIRECT_POST", privacyLevel=acc.get("privacyLevel"),
                 allowComment=acc.get("allowComment") is True, allowDuet=acc.get("allowDuet") is True,
                 allowStitch=acc.get("allowStitch") is True, isYourBrand=your_brand(camp), isBrandedContent=not own(camp),
                 autoAddMusic=False, isAiGeneratedContent=r["ai"] is True)
    elif p == "INSTAGRAM":
        t.update(postType="REEL", isAiGeneratedContent=r["ai"] is True)
    elif p == "YOUTUBE":
        # category is optional: left out, YouTube picks it.
        t.update(title=r["title"], privacy=acc.get("privacy"), madeForKids=acc.get("madeForKids") is True)
        if r["tags"]:
            t["tags"] = r["tags"]
    t["contentOverride"] = [{"text": r["text"], "media": [{"type": "MEDIA_LIBRARY", "mediaId": media_id(media, r["file"])}]}]
    return t


def build_requests(rows, camp, media):
    """One request per round: the first post of every connected account, then the second, and so on
    (one child per account in each request)."""
    queue = {}
    for r in rows:
        if r.get("send"):
            queue.setdefault(r["name"], []).append(r)
    reqs = []
    k = 0
    while any(queue.values()):
        k += 1
        batch = [q.pop(0) for q in queue.values() if q]
        kids = [child(r, media, camp) for r in batch]
        name = f"{camp.get('id', 'campaign')}{'' if k == 1 else '-' + str(k)}.json"
        body = {"content": [dict(kids[0]["contentOverride"][0])], "schedule": {"type": "PUBLISH_NOW"},
                "socialAccounts": kids}
        reqs.append((name, body, batch))
    return reqs


# ---- pages

def footage_line(r):
    src = r.get("source") or {}
    if not src.get("ranges"):
        return ""
    rg = src["ranges"]
    day = f", recorded {r['footage_date']}" if r.get("footage_date") else ""
    return f"{src.get('file')} {stamp(rg[0][0])} to {stamp(rg[-1][1])}{day}"


def wm_text(scr):
    w = scr.get("watermark")
    if isinstance(w, dict):
        return f"logo {w.get('image')} ({w.get('position')})" if w.get("image") else f"\"{w.get('text')}\""
    return f"\"{w}\"" if w else ""


def card_md(r, camp):
    out = [f"### {r['name']}{' ' + r['handle'] if r['handle'] else ''} ({r['label']}), post `{r['id']}`", ""]
    if r["posted"]:
        out += [f"Already posted: {r['posted'].get('url') or 'post ' + str(r['posted'].get('postId'))}.", ""]
    elif r.get("hand"):
        out += ["**By hand**: see `by-hand/" + r["id"] + ".md`.", ""]
    if r.get("info"):
        i = r["info"]
        out.append(f"- Clip: `{r['file']}`, {i['duration']:.1f} s, {i['width']}x{i['height']}, {i['bytes'] / MB:.1f} MB, "
                   f"fingerprint {r['sha256'][:12]}")
    if footage_line(r):
        out.append(f"- Footage: {footage_line(r)}")
    if r.get("hook"):
        out.append(f"- Hook on screen: \"{r['hook']}\"")
    scr = r.get("screen") or {}
    if scr.get("disclosure"):
        out.append(f"- Disclosure on screen: \"{scr['disclosure']}\" for the first {scr.get('disclosure_seconds', 0):g} s")
    if wm_text(scr):
        out.append(f"- Watermark: {wm_text(scr)}")
    if r["title"]:
        out.append(f"- Title: {r['title']}")
    out.append(f"- Caption ({r.get('count', 0)} of {LIMITS[r['platform']].get('text') or LIMITS[r['platform']].get('text_bytes')}):")
    out += ["", "  > " + r["text"].replace("\n", "\n  > "), ""]
    if r["tags"]:
        out.append(f"- Tags: {', '.join(r['tags'])}")
    out.append("- Settings: " + "; ".join(settings_bits(r, camp)))
    out.append("- Expected earnings: " + earnings_text(r, camp))
    lv = [l for l, _ in r["issues"]]
    out.append("- Checks: " + ("BLOCKED" if "error" in lv else "all passed" + (" (see below)" if lv else "")))
    for l, m in r["issues"]:
        out.append(f"  - {l}: {m}")
    pre, win = before_steps(r, camp), window_steps(r, camp)
    if pre and not r["posted"]:
        out.append("- Before posting:")
        out += [f"  - {s}" for s in pre]
    if win:
        out.append(f"- Inside the {int(camp['submit_within_minutes'])} minutes after it is live:")
        out += [f"  - {s}" for s in win]
    out.append("")
    return out


def summary_line(m):
    rows = m["rows"]
    send = [r for r in rows if r.get("send")]
    hand = [r for r in rows if r.get("hand") and not r["posted"]]
    done = [r for r in rows if r["posted"]]
    parts = [f"{plural(len(send), 'post')} through WoopSocial", f"{len(hand)} by hand"]
    if done:
        parts.append(f"{len(done)} already posted")
    return (f"{plural(len(rows), 'clip')} for {plural(len({r['name'] for r in rows}), 'account')} "
            f"({', '.join(parts)}). Everything goes out now, when you say yes, so you can submit each link within "
            f"{int(m['campaign']['submit_within_minutes'])} minutes.")


def footer_lines(c):
    return [f"Submit every link within {int(c['submit_within_minutes'])} minutes, into this campaign only, once. "
            "`submit.md` gives the clock time per post and when to take the proof screenshots.",
            f"Leave every post public and unchanged for {int(c['days_live'])} days. {window_note(c)}.",
            "Earnings are estimates: the campaign's own count decides what is paid, and most clips get few views. "
            "Never buy views or join engagement groups: it is a permanent ban on the marketplaces."]


def page_md(m):
    c = m["campaign"]
    info = m["camp_info"]
    out = [MARK, f"# Clip plan: {c.get('name', '')}", "",
           f"Campaign `{c.get('id')}`" + (" (your own content on your own accounts)" if own(c) else f" for {c.get('brand')}")
           + f". Checklist version `{info['version']}`. Planned {m['planned']}.", "", summary_line(m), ""]
    if example_demo(c):
        out += [f"**{DEMO_NOTE}**", ""]
    errs = [i for i in m["checks"] if i[0] == "error"]
    if errs:
        out += [f"**{len(errs)} thing(s) to fix before anything can be posted.** They are listed under Checks.", ""]
    if info["conflict"]:
        out += ["**Conflict:** the brief forbids the disclosure on the video (" +
                "; ".join(f"\"{s}\"" for s, _ in info["conflict"]) + "). Every clip keeps it on screen. Ask the "
                "campaign team in writing whether a short \"Ad\" for the first seconds is accepted, or skip this "
                "campaign.", ""]
    if info["hide"]:
        out += ["**Never followed:** the brief asks to hide that the clips are paid (" +
                "; ".join(f"\"{s}\"" for s, _ in info["hide"]) + "). " + (
                    "In a real campaign every clip keeps its disclosure; this demo shows its EXAMPLE ONLY line in that "
                    "spot." if example_demo(c) else "Every clip keeps its disclosure."), ""]
    byp = before_you_post(m)
    if byp:
        out += ["## Before you post", ""] + [f"- {s}" for s in byp] + [""]
    for r in m["rows"]:
        out += card_md(r, c)
    other = [i for i in m["checks"] if not any((i[0], i[2]) in r["issues"] for r in m["rows"])]
    if other:
        out += ["## Checks", ""]
        for lv, w, msg in sorted(other, key=lambda i: ("error", "warning", "note").index(i[0])):
            out.append(f"- {lv}: {w}: {msg}")
        out.append("")
    if m["uploads"]:
        out += ["## Files to upload", "", "Only after the yes, once each:", ""]
        out += [f"- `{f}` ({b / MB:.1f} MB, fingerprint `{h[:16]}`)" for f, b, h in m["uploads"]]
        out += ["", "Save each upload in media.json as {\"<file>\": {\"mediaId\": ..., \"sha256\": \"<fingerprint>\"}}. "
                "A clip changed after its upload is refused: upload it again.", ""]
    if m["requests"]:
        out += ["## Requests", ""] + [f"- `requests/{n}`" for n in m["requests"]] + [""]
    if m["hand_files"]:
        out += ["## By hand", ""] + [f"- `{f}`" for f in m["hand_files"]] + [""]
    if m["approval_files"]:
        out += ["## For the brand's approval", "", "Send each packet before posting; record the answer in clipjob.json.", ""]
        out += [f"- `{f}`" for f in m["approval_files"]] + [""]
    out += ["## After it's live", ""] + [f"- {s}" for s in footer_lines(c)] + [""]
    if m["connected_n"] > 2:
        out += [f"{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 social accounts; more "
                "need a paid plan.", ""]
    return "\n".join(out)


CSS = """
:root{--bg:#f6f6f4;--card:#fff;--ink:#17181a;--mute:#62666d;--line:#dcdcd8;--err:#b3261e;--warn:#8a5a00;--ok:#1d6b3a;--chip:#eeeeea;--flag:#fff4e5}
@media (prefers-color-scheme:dark){:root{--bg:#141516;--card:#1d1f21;--ink:#ececec;--mute:#a1a5ab;--line:#33363a;--err:#ff8a80;--warn:#f0c060;--ok:#7fd49b;--chip:#2a2d30;--flag:#2b2416}}
*{box-sizing:border-box;min-width:0}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 64px;overflow-wrap:anywhere}h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:32px 0 6px}
.sub{color:var(--mute);margin:0 0 16px}.cards{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;grid-template-columns:110px minmax(0,1fr);gap:14px;align-items:start}
.card img{width:100%;border-radius:8px;display:block;background:#000}.noimg{aspect-ratio:9/16;border:1px dashed var(--line);border-radius:8px}
.card h3{margin:0;font-size:16px}.meta{color:var(--mute);font-size:13px;margin:2px 0 8px}.text{white-space:pre-wrap;margin:6px 0 8px;font-size:15px}
.title{font-weight:650;margin:6px 0 0}.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.chip{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:13px}
.k{font-size:13px;color:var(--mute);margin:8px 0 2px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}.small{font-size:14px;margin:0}
.state{font-weight:650;font-size:14px}.okc{color:var(--ok)}.error{color:var(--err)}.warning{color:var(--warn)}.note{color:var(--mute)}.hand{color:var(--warn)}
ul{padding-left:20px;margin:6px 0}.banner{border-radius:12px;padding:12px 16px;margin:0 0 10px;border:1px solid var(--line);background:var(--card)}
.flag{background:var(--flag)}code{font-size:14px}.card ul{font-size:14px}
@media (max-width:520px){.card{grid-template-columns:minmax(0,1fr)}.card>div:first-child{max-width:140px}}
"""


def page_html(m):
    c = m["campaign"]
    info = m["camp_info"]
    who = " (your own content on your own accounts)" if own(c) else f" for {esc(c.get('brand'))}"
    out = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">", MARK,
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Clip plan</title>",
           f"<style>{CSS}</style></head><body><main>", f"<h1>Clip plan: {esc(c.get('name', ''))}</h1>",
           f"<p class=\"sub\">Campaign <code>{esc(c.get('id'))}</code>{who}. Checklist version "
           f"<code>{esc(info['version'])}</code>. Planned {esc(m['planned'])}.<br>{esc(summary_line(m))}</p>"]
    if example_demo(c):
        out.append(f"<div class=\"banner\"><strong>EXAMPLE ONLY:</strong> {esc(DEMO_NOTE[len('EXAMPLE ONLY: '):])}</div>")
    errs = [i for i in m["checks"] if i[0] == "error"]
    if errs:
        out.append(f"<div class=\"banner error\"><strong>{len(errs)} thing(s) to fix before anything can be posted."
                   "</strong> They are listed on the cards and under Checks.</div>")
    if info["conflict"]:
        out.append("<div class=\"banner flag\"><strong>Conflict:</strong> the brief forbids the disclosure on the video ("
                   + "; ".join(f"&ldquo;{esc(s)}&rdquo;" for s, _ in info["conflict"]) + "). Every clip keeps it on "
                   "screen. Ask the campaign team in writing whether a short &ldquo;Ad&rdquo; for the first seconds is "
                   "accepted, or skip this campaign.</div>")
    if info["hide"]:
        out.append("<div class=\"banner flag\"><strong>Never followed:</strong> the brief asks to hide that the clips "
                   "are paid (" + "; ".join(f"&ldquo;{esc(s)}&rdquo;" for s, _ in info["hide"]) + "). " + (
                   "In a real campaign every clip keeps its on-screen disclosure, #ad first in the caption and the "
                   "platform's paid-partnership setting; this demo shows its EXAMPLE ONLY line in that spot."
                   if example_demo(c) else "Every clip keeps its on-screen disclosure, #ad first in the caption and "
                   "the platform's paid-partnership setting.") + "</div>")
    byp = before_you_post(m)
    if byp:
        out.append("<div class=\"banner\"><strong>Before you post</strong><ul>" + "".join(f"<li>{esc(s)}</li>" for s in byp)
                   + "</ul></div>")
    out.append("<div class=\"cards\">")
    for r in m["rows"]:
        img = "<div class=\"noimg\"></div>"
        if r.get("cover") and os.path.isfile(r["cover"]) and os.path.getsize(r["cover"]) < 400 * 1000:
            with open(r["cover"], "rb") as fh:
                src = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode("ascii")
            img = f"<img src=\"{src}\" alt=\"First frame of {esc(r['id'])}\">"
        lv = [l for l, _ in r["issues"]]
        if r["posted"]:
            state = "<span class=\"state okc\">already posted</span>"
        elif "error" in lv:
            state = "<span class=\"state error\">blocked</span>"
        else:
            state = "<span class=\"state okc\">all checks passed</span>" + (
                " <span class=\"state hand\">by hand</span>" if r.get("hand") else "")
        meta = [r["label"], f"post {r['id']}"]
        if r.get("info"):
            meta.append(f"{r['info']['duration']:.1f} s")
        if footage_line(r):
            meta.append("footage " + footage_line(r).split(" ", 1)[1])
        out.append(f"<div class=\"card\"><div>{img}</div><div>")
        out.append(f"<h3>{esc(r['name'])} {esc(r['handle'])}</h3><div class=\"meta\">{esc(' · '.join(meta))}</div>{state}")
        if r.get("hook"):
            out.append(f"<p class=\"k\">Hook</p><p class=\"small\">{esc(r['hook'])}</p>")
        scr = r.get("screen") or {}
        if scr.get("disclosure") or wm_text(scr):
            bits = []
            if scr.get("disclosure"):
                bits.append(f"&ldquo;{esc(scr['disclosure'])}&rdquo; for the first {scr.get('disclosure_seconds', 0):g} s")
            if wm_text(scr):
                bits.append("watermark " + esc(wm_text(scr)))
            out.append(f"<p class=\"k\">On screen</p><p class=\"small\">{'; '.join(bits)}</p>")
        out.append("<p class=\"k\">" + ("Title and description" if r["platform"] == "YOUTUBE" else "Caption") + "</p>")
        if r["title"]:
            out.append(f"<p class=\"title\">{esc(r['title'])}</p>")
        out.append(f"<p class=\"text\">{esc(r['text'])}</p>")
        out.append("<div class=\"chips\">" + "".join(f"<span class=\"chip\">{esc(b)}</span>" for b in settings_bits(r, c))
                   + "</div>")
        out.append(f"<p class=\"k\">Expected earnings</p><p class=\"small\">{esc(earnings_text(r, c))}</p>")
        if r["issues"]:
            out.append("<ul>" + "".join(f"<li class=\"{l}\">{esc(msg)}</li>" for l, msg in r["issues"]) + "</ul>")
        pre, win = before_steps(r, c), window_steps(r, c)
        if pre and not r["posted"]:
            out.append("<p class=\"k\">Before posting</p><ul>" + "".join(f"<li>{esc(s)}</li>" for s in pre) + "</ul>")
        if win:
            out.append(f"<p class=\"k\">Inside the {int(c['submit_within_minutes'])} minutes</p><ul>"
                       + "".join(f"<li>{esc(s)}</li>" for s in win) + "</ul>")
        out.append("</div></div>")
    out.append("</div>")
    other = [i for i in m["checks"] if not any((i[0], i[2]) in r["issues"] for r in m["rows"])]
    if other:
        out.append("<h2>Checks</h2><ul>")
        for lv, w, msg in sorted(other, key=lambda i: ("error", "warning", "note").index(i[0])):
            out.append(f"<li class=\"{lv}\"><strong>{esc(w)}</strong>: {esc(msg)}</li>")
        out.append("</ul>")
    if m["uploads"]:
        out.append("<h2>Files to upload</h2><p class=\"sub\">Only after the yes, once each:</p><ul>"
                   + "".join(f"<li><code>{esc(f)}</code> ({b / MB:.1f} MB, fingerprint <code>{esc(h[:16])}</code>)</li>"
                             for f, b, h in m["uploads"]) + "</ul>")
    if m["hand_files"]:
        out.append("<h2>By hand</h2><ul>" + "".join(f"<li><code>{esc(f)}</code></li>" for f in m["hand_files"]) + "</ul>")
    if m["approval_files"]:
        out.append("<h2>For the brand's approval</h2><ul>"
                   + "".join(f"<li><code>{esc(f)}</code></li>" for f in m["approval_files"]) + "</ul>")
    out.append("<h2>After it's live</h2><ul>" + "".join(
        f"<li>{esc(s).replace('`submit.md`', '<code>submit.md</code>')}</li>" for s in footer_lines(c)) + "</ul>")
    if m["connected_n"] > 2:
        out.append(f"<p class=\"sub\">{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 social "
                   "accounts; more need a paid plan.</p>")
    out.append("</main></body></html>")
    return "\n".join(out)


def hand_page(r, camp):
    acc = r["account"]
    win = int(camp["submit_within_minutes"])
    out = [MARK, f"# {r['name']}{' ' + r['handle'] if r['handle'] else ''}: post `{r['id']}` by hand", "",
           f"Campaign: {camp.get('name')} (`{camp.get('id')}`).", ""]
    if example_demo(camp):
        out += [f"**{DEMO_NOTE}**", ""]
    out += ["## Before you post", ""]
    steps = [f"Put `{r.get('file')}` on your phone (AirDrop, cloud drive, or a cable). Post this exact file: don't trim, "
             "filter or re-edit it in the app" + ("; adding the required sound is the one exception." if sound_for(r, camp)
                                                    else ".")]
    if not own(camp):
        steps.append(f"Post from this account only if it is connected and verified in "
                     f"{camp.get('marketplace') or 'the campaign marketplace'}.")
    steps += before_steps(r, camp)
    out += [f"{n}. {s}" for n, s in enumerate(steps, 1)] + ["", "## Post it", ""]
    post = []
    snd = sound_for(r, camp)
    if r["platform"] == "TIKTOK":
        if snd:
            post.append(f"In TikTok, add the sound \"{snd['name']}\"" + (f" and set it to {snd['volume']}" if snd.get("volume")
                        else "") + " before posting.")
        post.append(f"Paste the caption below. Who can see it: "
                    f"{PRIVACY_WORDS.get(acc.get('privacyLevel'), 'ask the account owner')}; comments "
                    f"{'on' if acc.get('allowComment') else 'off'}, duets {'on' if acc.get('allowDuet') else 'off'}, "
                    f"stitches {'on' if acc.get('allowStitch') else 'off'}.")
        if your_brand(camp):
            post.append("Under more options, turn on the content disclosure setting and choose \"Your brand\".")
        elif not own(camp):
            post.append("Under more options, turn on the content disclosure setting and choose paid partnership "
                        "(branded content).")
        if r.get("ai") is True:
            post.append("Turn on the AI-generated content label.")
        post.append("Post.")
    elif r["platform"] == "INSTAGRAM":
        if snd:
            post.append(f"New Reel; add the sound \"{snd['name']}\"" + (f" at {snd['volume']}" if snd.get("volume") else "")
                        + " before sharing.")
        post.append("New Reel, paste the caption below" + ("" if own(camp) else
                    ", and turn on the paid partnership label (tagging the brand as partner is optional and may need "
                    "their approval)") + ".")
        if r.get("ai") is True:
            post.append("Turn on the AI label.")
        post.append("Share.")
    else:
        post.append(f"Upload it as a Short. Title and description below; visibility {acc.get('privacy', 'public')}; "
                    f"{'made for kids' if acc.get('madeForKids') else 'not made for kids'}"
                    + ("" if own(camp) else "; tick that it includes paid promotion") + ".")
        if r.get("ai") is True:
            post.append("Answer Yes to \"Altered or synthetic content\".")
        post.append("Publish.")
    out += [f"{n}. {s}" for n, s in enumerate(post, 1)] + ["", f"## Right after (you have {win} minutes)", ""]
    after = ["Copy the post's link from the share menu and paste it back to your agent. It records the post and tells "
             "you the exact time your window closes.",
             f"Submit the link to the campaign within {win} minutes of it going live, into this campaign only, once.",
             "Tell your agent it is submitted (with the submission id if the campaign shows one)."]
    out += [f"{n}. {s}" for n, s in enumerate(after, 1)] + [""]
    out += (["## Title", "", r["title"], ""] if r["title"] else [])
    out += ["## Caption" if r["platform"] != "YOUTUBE" else "## Description", "", "```", r["text"], "```", ""]
    if r["tags"]:
        out += ["## Tags", "", ", ".join(r["tags"]), ""]
    out += [f"Expected earnings: {earnings_text(r, camp)} {window_note(camp)}; the campaign's own count decides.", ""]
    return "\n".join(out)


def approval_page(r, camp):
    src = r.get("source") or {}
    rg = src.get("ranges") or []
    scr = r.get("screen") or {}
    out = [MARK, f"# For approval: `{r['id']}` ({r['label']}, {r['name']}{' ' + r['handle'] if r['handle'] else ''})", "",
           f"Campaign: {camp.get('name')} (`{camp.get('id')}`). Send the clip file and this text to the campaign team "
           "where the brief says (Discord, email or the marketplace chat). Post only after a clear yes.", "",
           f"- Clip: `{r.get('file')}`, {r['info']['duration']:.1f} s, fingerprint `{r['sha256'][:12]}`",
           f"- Footage: {src.get('file') or '?'} " + (", ".join(f"{stamp(a)} to {stamp(b)}" for a, b in rg) if rg else "")]
    if r.get("hook"):
        out.append(f"- Hook on screen: \"{r['hook']}\"")
    if scr.get("disclosure"):
        out.append(f"- Disclosure on screen: \"{scr['disclosure']}\" for the first {scr.get('disclosure_seconds', 0):g} s")
    if r["title"]:
        out.append(f"- Title: {r['title']}")
    out += ["", "## Caption", "", "```", r["text"], "```", "", "## Message to paste", "", "```",
            f"Hi! Draft for {camp.get('name')} on {r['label']} ({r['handle'] or r['name']}). Clip attached "
            f"(fingerprint {r['sha256'][:12]}), caption below. OK to post as is?", "", r["text"], "```", "",
            "## When they answer", "",
            "Tell your agent who approved it and when. It records this in clipjob.json as "
            f"`\"approved\": {{\"by\": \"<name>\", \"at\": \"<time>\", \"sha256\": \"{r['sha256'][:12]}\"}}`. If the file "
            "changes after that, the check stops it until the new version is approved too. Keep their message: it is "
            "the evidence if a payout is disputed.", ""]
    return "\n".join(out)


def ours(path):
    """True when this file was written by plan.py (it carries the marker)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return MARK in fh.read(4000)
    except OSError:
        return False


def clear_old(job_dir):
    req_dir = os.path.join(job_dir, "requests")
    for d in ("requests", "by-hand", "approval"):
        full = os.path.join(job_dir, d)
        if os.path.lexists(full) and not os.path.isdir(full):
            die(f"{d} is a file here, and plan.py needs a folder with that name. Move or rename the file")
    for f in ("plan.md", "plan.html"):
        full = os.path.join(job_dir, f)
        if os.path.isfile(full) and not ours(full):
            die(f"{f} here wasn't written by plan.py, and planning would replace it. Rename your own {f}, or plan "
                "from another folder")
    if os.path.isdir(req_dir):
        old = [f for f in os.listdir(req_dir) if f.endswith(".json")]
        if old and "index.json" not in old:
            die("the folder requests/ here holds JSON files that plan.py didn't write. Run plan.py from your own "
                "project folder, or move those files somewhere else")
        for f in sorted(old, key=lambda f: f == "index.json"):
            os.remove(os.path.join(req_dir, f))
        if not os.listdir(req_dir):
            os.rmdir(req_dir)
    for d in ("by-hand", "approval"):
        full = os.path.join(job_dir, d)
        if os.path.isdir(full):
            for f in os.listdir(full):
                if f.endswith(".md") and ours(os.path.join(full, f)):
                    os.remove(os.path.join(full, f))
            if not os.listdir(full):
                os.rmdir(full)
    for f in ("plan.md", "plan.html"):
        if os.path.isfile(os.path.join(job_dir, f)):
            os.remove(os.path.join(job_dir, f))


def load_media(arg, job_dir, files):
    """media.json: {"<clip file>": {"mediaId": ..., "sha256": "<the fingerprint plan.md lists>"}}. The
    fingerprint ties each upload to the file as it was uploaded: a clip cut again under the same name
    is refused, so the post never carries an older cut than the one the user said yes to."""
    path = arg if os.path.isfile(arg) else os.path.join(job_dir, arg)
    media = read_json(path, "the uploaded media ids")
    form = "{\"<clip file as plan.md lists it>\": {\"mediaId\": \"<mediaId>\", \"sha256\": \"<its fingerprint>\"}}"
    if not isinstance(media, dict):
        die(f"{arg} must be {form}")
    for k, v in media.items():
        if isinstance(v, str):
            die(f"{arg}: {k} has a mediaId but no fingerprint. Write {form}, with the fingerprint plan.md lists "
                "under \"Files to upload\"")
        if not isinstance(v, dict) or not isinstance(v.get("mediaId"), str) or not v["mediaId"].strip():
            die(f"{arg} must be {form}; {k} has no mediaId")
        if not isinstance(v.get("sha256"), str) or len(v["sha256"].strip()) < 12:
            die(f"{arg}: {k} needs \"sha256\", the fingerprint plan.md lists for it (12 characters or more)")
    unknown = [k for k in media if k not in files]
    if unknown:
        die(f"{arg} names {', '.join(unknown)}, which isn't a file of this plan ({', '.join(files) or 'none'})")
    missing = [f for f in files if f not in media]
    if missing:
        die(f"{arg} has no mediaId for {', '.join(missing)}. Upload each file under \"Files to upload\" once and add "
            "its mediaId, then run this again")
    changed = [f for f in files if not sha256(os.path.join(job_dir, f)).startswith(media[f]["sha256"].strip().lower())]
    if changed:
        die(f"{', '.join(changed)} changed after it was uploaded (its fingerprint isn't the uploaded one). Upload it "
            "again, put the new mediaId and fingerprint in media.json, and show the plan for a new yes")
    return media


def plan(job_path, media_arg=None, ledger_file=None):
    m = check_job(job_path, ledger_file)
    job_dir, camp = m["job_dir"], m["campaign"]
    clear_old(job_dir)
    m = check_job(job_path, ledger_file)   # again, after clearing: nothing from the run before is read
    errs = [i for i in m["checks"] if i[0] == "error"]
    for r in m["rows"]:
        r.setdefault("text", "")
        r.setdefault("title", "")
        r.setdefault("tags", [])
        r["hand"] = is_by_hand(r, camp) and not r["posted"]
        r["send"] = bool(r.get("file")) and not r["hand"] and not r["posted"]
    files = sorted({r["file"] for r in m["rows"] if r.get("send")})
    media = load_media(media_arg, job_dir, files) if media_arg else {}
    m["uploads"] = [(f, os.path.getsize(os.path.join(job_dir, f)), sha256(os.path.join(job_dir, f))) for f in files]
    zone = m["job"].get("timezone")
    m["planned"] = clock(now_utc(), zone)
    m["connected_n"] = len({r["name"] for r in m["rows"] if r["connected"]})
    m["requests"], m["hand_files"], m["approval_files"] = [], [], []
    for r in m["rows"]:
        if r.get("needs_approval") and r.get("file") and not r["posted"]:
            path = os.path.join(job_dir, "approval", f"{r['id']}.md")
            write_text(path, approval_page(r, camp))
            m["approval_files"].append(rel(path, job_dir))
    if not errs:
        reqs = build_requests(m["rows"], camp, media)
        index = {}
        for name, body, batch in reqs:
            write_json(os.path.join(job_dir, "requests", name), body)
            m["requests"].append(name)
            index[name] = {"campaign": camp.get("id"), "posts": [
                {"post": r["id"], "account": r["name"], "socialAccountId": r["account"]["socialAccountId"],
                 "platform": r["platform"], "file": r["file"]} for r in batch]}
        if index:
            write_json(os.path.join(job_dir, "requests", "index.json"), index)
        for r in m["rows"]:
            if r["hand"] and r.get("file"):
                path = os.path.join(job_dir, "by-hand", f"{r['id']}.md")
                write_text(path, hand_page(r, camp))
                m["hand_files"].append(rel(path, job_dir))
    write_text(os.path.join(job_dir, "plan.md"), page_md(m))
    write_text(os.path.join(job_dir, "plan.html"), page_html(m))
    warns = [i for i in m["checks"] if i[0] == "warning"]
    print(f"{plural(len(m['rows']), 'clip')} planned -> plan.md, plan.html ({len(errs)} errors, {len(warns)} warnings)")
    if zone and load_zone(zone) is None:
        print(f"warning: the time zone {zone} can't be loaded here, so times are shown in UTC. On Windows: pip install "
              "tzdata")
    if m["camp_info"]["conflict"]:
        print(f"conflict: {len(m['camp_info']['conflict'])} brief sentence(s) forbid the on-screen disclosure. Ask the "
              "campaign team in writing, or skip this campaign")
    if m["camp_info"]["hide"]:
        print(f"never followed: {len(m['camp_info']['hide'])} brief sentence(s) asking to hide the ad")
    if m["approval_files"]:
        print(f"for approval ({len(m['approval_files'])}): approval/ (send each packet to the campaign team)")
    if errs:
        print("fix every error (listed on the plan) and run this again. No request was written")
        for lv, w, msg in errs:
            print(f"  error: {w}: {msg}")
        sys.exit(1)
    if m["hand_files"]:
        print(f"by hand ({len(m['hand_files'])}): by-hand/")
    if m["requests"]:
        print("requests: " + ", ".join("requests/" + n for n in m["requests"]))
        if media_arg:
            print("next: posts_validate each request; then posts_create, and right after it: plan.py "
                  f"{rel(job_path)} --posted requests/<name>.json <postId>")
        else:
            print("next: show plan.html (or paste plan.md) and wait for a clear yes. Only after the yes: upload each "
                  "file under \"Files to upload\", save {file: {mediaId, sha256}} as media.json, run again with --media "
                  "media.json")
    elif m["hand_files"]:
        print("next: show plan.html (or paste plan.md) and wait for a clear yes; then hand over the by-hand pages")
    else:
        print("nothing left to post: every clip in this job is recorded in the ledger. See submit.md for what is "
              "still to submit")


# ---- after posting

def index_entry(job_dir, request):
    idx_path = os.path.join(job_dir, "requests", "index.json")
    idx = read_json(idx_path, "the request index") if os.path.exists(idx_path) else {}
    name = os.path.basename(request)
    if not isinstance(idx, dict) or name not in idx or not isinstance(idx[name], dict) or \
            not isinstance(idx[name].get("posts"), list):
        die(f"{name} isn't one of this plan's requests ({', '.join(sorted(idx)) if isinstance(idx, dict) else 'none'}). "
            "Run plan.py again")
    return name, idx[name]


def remember_campaign(ledger, camp):
    """The campaign's terms go into the ledger, so --earnings works from any folder."""
    keep = ("id", "name", "brand", "marketplace", "currency", "platforms", "min_payout", "min_views", "cap_per_clip",
            "budget_total", "fee_pct", "window_days", "window_from", "days_live", "submit_within_minutes",
            "engagement_min", "audience", "own_content")
    ledger["campaigns"][camp.get("id")] = {k: camp.get(k) for k in keep if camp.get(k) is not None}


def entry_for(r, camp, post_id, sid, now, zone=None):
    src = r.get("source") or {}
    return {"postId": post_id, "job_post": r["id"], "campaign": camp.get("id"), "account": r["name"],
            "handle": r["handle"], "platform": r["platform"], "socialAccountId": sid, "file": r["file"],
            "sha256": r["sha256"], "source_file": src.get("file"), "source_sha256": src.get("sha256"),
            "ranges": [list(x) for x in (src.get("ranges") or [])], "hook": r.get("hook"), "caption": r["text"],
            "submit_within": int(camp["submit_within_minutes"]), "recorded": iso(now), "url": None, "published_at": None,
            "timezone": zone}


def evidence_dirs(job_dir, posts):
    for p in posts:
        os.makedirs(os.path.join(job_dir, "proof", p), exist_ok=True)


def record_posted(job_path, request, post_id, ledger_file=None):
    post_id = (post_id or "").strip()
    if not post_id:
        die("give the post id that posts_create returned: --posted requests/<name>.json <postId>")
    m = check_job(job_path, ledger_file)
    job_dir, camp = m["job_dir"], m["campaign"]
    name, entry = index_entry(job_dir, request)
    rows = {r["id"]: r for r in m["rows"]}
    ledger = m["ledger"]
    now = now_utc()
    for x in entry["posts"]:
        r = rows.get(x.get("post"))
        if r is None or not r.get("sha256"):
            die(f"post {x.get('post')} of {name} is no longer in clipjob.json with its clip. Put it back as it was "
                "planned, then record it")
        key = f"{post_id}|{x['socialAccountId']}"
        if key in ledger["posts"]:
            die(f"{r['id']} on {r['name']} is already recorded as post {post_id}")
        if r["posted"]:
            die(f"{r['id']} on {r['name']} is already recorded as post {r['posted'].get('postId')}")
        ledger["posts"][key] = entry_for(r, camp, post_id, x["socialAccountId"], now, m["job"].get("timezone"))
        ledger["posts"][key]["request"] = name
    remember_campaign(ledger, camp)
    save_ledger(m["ledger_path"], ledger)
    evidence_dirs(job_dir, [x["post"] for x in entry["posts"]])
    print(f"recorded: {name} was sent as post {post_id} ({', '.join(x['account'] for x in entry['posts'])}) in the "
          f"ledger ({rel(m['ledger_path'])}). The {int(camp['submit_within_minutes'])} minutes to submit run from the "
          "moment each post is live.")
    print(f"next: posts_get {post_id} in a minute, save the reply as status.json, and run: plan.py "
          f"{rel(job_path)} --status status.json {post_id}  (links and deadlines)")
    write_sheet(m, ledger)


def unwrap(data):
    """A saved tool reply, wherever the post sits: {"data": ...}, {"result": ...}, {"structuredContent": ...},
    {"post": ...}, the MCP envelope {"content": [{"type": "text", "text": "{...}"}]} or the post itself."""
    for _ in range(4):
        data = unwrap_reply(data)
        if isinstance(data, dict) and not data.get("socialAccountPosts"):
            inner = next((data[k] for k in ("data", "result", "structuredContent", "post")
                          if isinstance(data.get(k), (dict, list))), None)
            if inner is None:
                break
            data = inner
        else:
            break
    return data


def apply_status(job_path, status_path, post_id=None, ledger_file=None):
    m = check_job(job_path, ledger_file)
    camp = m["campaign"]
    data = unwrap(read_json(status_path, "the saved posts_get reply"))
    items = post_items(data)
    if not items:
        die(f"{status_path} holds no per-account posts. Save the whole reply of posts_get as it came back")
    top = data.get("postId") or data.get("id") if isinstance(data, dict) else None
    pid = (post_id or "").strip() or (top if isinstance(top, str) else None)
    if not pid:
        die(f"{status_path} doesn't say which post it is about. Give the post id: --status {status_path} <postId> "
            "(the id posts_create returned)")
    if post_id and isinstance(top, str) and top != post_id:
        die(f"{status_path} is the reply for post {top}, not {post_id}. Save the posts_get reply of {post_id}")
    ledger = m["ledger"]
    mine = {k: e for k, e in ledger["posts"].items() if e.get("campaign") == camp.get("id") and e.get("postId") == pid}
    if not mine:
        die(f"the ledger has no post {pid} for campaign {camp.get('id')}. Record it first with --posted")
    by_url = {post_key(e["url"]): k for k, e in ledger["posts"].items() if e.get("url")}
    updated, failed, seen = 0, [], set()
    for it in items:
        if isinstance(it.get("postId"), str) and it["postId"] != pid:
            continue
        sid = it.get("socialAccountId")
        hits = [k for k, e in mine.items() if e.get("socialAccountId") == sid]
        if not hits:
            continue
        if len(hits) > 1 or sid in seen:
            die(f"{status_path} holds more than one post for account {sid}. Save the posts_get reply of post {pid} "
                "alone (not a list of the account's posts)")
        seen.add(sid)
        e = ledger["posts"][hits[0]]
        url = it.get("externalPostUrl").strip() if isinstance(it.get("externalPostUrl"), str) and \
            it["externalPostUrl"].strip() else None
        if url:
            other = by_url.get(post_key(url))
            if e.get("url") and post_key(e["url"]) != post_key(url):
                die(f"{e.get('job_post')} on {e.get('account')} already has the link {e['url']}, and this reply says "
                    f"{url}. Nothing was changed. Check which is right with posts_get before going on")
            if other and other != hits[0]:
                die(f"{url} is already in the ledger for another post ({ledger['posts'][other].get('job_post')}). "
                    "Nothing was changed")
            e["url"] = url
        st = it.get("deliveryStatus")
        if isinstance(st, str) and any(w in st.upper() for w in ("FAIL", "ERROR", "REJECT")):
            failed.append(f"{e.get('account')}: {st}")
        t = parse_time(it.get("deliveryCompletedAt"))
        if t:
            e["published_at"] = iso(t)
        if st:
            e["status"] = st
        updated += 1
    if not updated:
        die(f"{status_path} has no account of post {pid}. Save the posts_get reply of {pid} as it came back")
    save_ledger(m["ledger_path"], ledger)
    print(f"{updated} post(s) updated from {rel(status_path)}")
    for f in failed:
        print(f"  not published: {f}. Say why in plain words; nothing is resent without a new yes")
    write_sheet(m, ledger)


def record_by_hand(job_path, post, url, at=None, ledger_file=None):
    m = check_job(job_path, ledger_file)
    job_dir, camp = m["job_dir"], m["campaign"]
    r = next((r for r in m["rows"] if r["id"] == post), None)
    if r is None:
        die(f"there is no post \"{post}\" in the job ({', '.join(r['id'] for r in m['rows'])})")
    if not r.get("sha256"):
        die(f"post {post} has no clip file, so it can't be recorded")
    if not url.lower().startswith(("http://", "https://")):
        die("give the post's link as it shows in the app's share menu (https://...)")
    if short_link(url):
        die("that is a short share link, which doesn't show the post's id. Open it in a browser and copy the full "
            "link (tiktok.com/@<handle>/video/<number>)")
    link_platform = post_key(url).split(":")[0]
    if link_platform in LIMITS and link_platform != r["platform"]:
        die(f"that is a {LIMITS[link_platform]['label']} link, and {post} is the {LIMITS[r['platform']]['label']} post "
            f"on {r['name']}. Give the link of the post made on {r['name']}")
    ledger = m["ledger"]
    if any(post_key(e.get("url")) == post_key(url) for e in ledger["posts"].values() if e.get("url")):
        die(f"{url} is already in the ledger")
    if r["posted"]:
        die(f"{post} on {r['name']} is already recorded")
    now = now_utc()
    assumed = None
    if at:
        t, assumed, problem = parse_user_time(at, m["job"].get("timezone"))
        if problem:
            die(f"--at: {problem}")
        if t > now + datetime.timedelta(minutes=2):
            die(f"--at {at} is in the future ({clock(t, m['job'].get('timezone'))}). Give the time it went live")
    else:
        t = now
    key = f"hand:{post}|{r['name']}"
    e = entry_for(r, camp, "by hand", r["account"].get("socialAccountId"), now, m["job"].get("timezone"))
    e.update(byHand=True, url=url, published_at=iso(t))
    ledger["posts"][key] = e
    remember_campaign(ledger, camp)
    save_ledger(m["ledger_path"], ledger)
    evidence_dirs(job_dir, [post])
    print(f"recorded: {post} posted by hand on {r['name']}")
    if assumed:
        print(f"note: --at {at} has no time zone, so it was read as {assumed} time")
    write_sheet(m, ledger)


def release(job_path, post, ledger_file=None, checked=False):
    """--failed: take one post that never went live out of the ledger, so the next plan sends it again."""
    m = check_job(job_path, ledger_file)
    camp = m["campaign"]
    ledger = m["ledger"]
    hits = [k for k, e in ledger["posts"].items() if e.get("job_post") == post and e.get("campaign") == camp.get("id")]
    if not hits:
        ids = sorted({e.get("job_post") for e in ledger["posts"].values() if e.get("campaign") == camp.get("id")})
        die(f"the ledger has no post \"{post}\" for this campaign. --failed takes the job's post id"
            + (f" ({', '.join(ids)})" if ids else "") + ", not the WoopSocial post id")
    for k in hits:
        e = ledger["posts"][k]
        if e.get("url") or e.get("byHand") or any(s.get("post") == post and s.get("campaign") == camp.get("id")
                                                  for s in ledger["submissions"]):
            die(f"{post} on {e.get('account')} has a link or was submitted, so it went live. It is never released: "
                "posting the same edit again is a duplicate")
        st = str(e.get("status") or "").upper()
        if not any(w in st for w in ("FAIL", "ERROR", "REJECT")):
            die(f"{post} on {e.get('account')} isn't marked as failed (status: {e.get('status') or 'not read yet'}). "
                "A post still processing can go live minutes later. Call posts_get again, save the reply, run --status; "
                "release it only when its status says it failed")
    if not checked:
        e = ledger["posts"][hits[0]]
        die(f"before releasing: a post marked failed can still have been published on the platform. Call "
            f"social_account_posts_list for {e.get('account')} ({e.get('socialAccountId') or 'its account'}) and look at "
            "the last hour. Only when the clip isn't there, run this again with --checked")
    for k in hits:
        del ledger["posts"][k]
    save_ledger(m["ledger_path"], ledger)
    print(f"released: {post} is out of the ledger. Plan again: the new request holds it. Show the plan and wait "
          "for a new yes before posting it")


def left_text(due, now, live):
    if live > now:
        return "not live yet"
    secs = (due - now).total_seconds()
    if secs <= 0:
        return "the window has passed"
    if secs < 60:
        return "under a minute left"
    return f"{math.ceil(secs / 60)} min left"


def write_sheet(m, ledger):
    """submit.md and the same on screen: per post of this campaign not yet submitted, its link, the clock
    time the window closes, what to do in the apps before then, and when to take the proof screenshots."""
    camp, job_dir = m["campaign"], m["job_dir"]
    zone = m["job"].get("timezone")
    win = int(camp["submit_within_minutes"])
    now = now_utc()
    done = {post_key(s.get("url")) for s in ledger["submissions"]}
    rows = {r["id"]: r for r in m["rows"]}
    hours = shot_hours(camp)
    lines = [f"# Submit: {camp.get('name')}", "",
             f"Campaign `{camp.get('id')}`. One post goes into one campaign, once. Submit each link within {win} "
             "minutes of it going live; a late post can't be fixed. Times are in "
             + (zone if load_zone(zone) else "UTC") + ".", ""]
    n = 0
    mine = [e for e in ledger["posts"].values() if e.get("campaign") == camp.get("id")]
    for e in mine:
        if e.get("url") and post_key(e["url"]) in done:
            continue
        n += 1
        who = f"{e.get('account')}{' ' + e['handle'] if e.get('handle') else ''}"
        lines.append(f"{n}. **{who}** ({LIMITS.get(e.get('platform'), {}).get('label', e.get('platform'))}), post `{e.get('job_post')}`")
        if e.get("url"):
            lines.append(f"   - Link: {e['url']}")
        else:
            lines.append("   - Link: not there yet. Your agent checks again in a minute.")
        live = parse_time(e.get("published_at"))
        sent = parse_time(e.get("recorded"))
        mins = int(e.get("submit_within") or win)
        if live:
            due = live + datetime.timedelta(minutes=mins)
            if live > now:
                lines.append(f"   - Not live yet. When it is, you have {mins} minutes to submit.")
            else:
                lines.append(f"   - Live since {clock(live, zone)}. Submit by **{clock(due, zone)}** "
                             f"({left_text(due, now, live)}).")
        elif sent:
            # not confirmed live: no countdown, but the earliest the window can close, to be safe
            due = sent + datetime.timedelta(minutes=mins)
            lines.append(f"   - Sent {clock(sent, zone)}, not confirmed live yet. To be safe, submit by "
                         f"**{clock(due, zone)}**; your agent reads the exact time once it is live.")
        r = rows.get(e.get("job_post"))
        for s in (window_steps(r, camp) if r else []):
            lines.append(f"   - Before then: {s}")
        lines.append("   - After submitting: tell your agent it is submitted (with the submission id if the campaign "
                     "shows one).")
    if not n:
        lines.append("Nothing waiting: every recorded post of this campaign is submitted.")
    if mine:
        lines += ["", "## Proof to keep", "",
                  "Screenshot each post's analytics (views and audience countries) at these times, and save them in "
                  "its folder. Campaigns ask for them when a payout is checked." + (
                      f" The brief asks for: {'; '.join(camp['proof'])}." if camp.get("proof") else ""), ""]
        for e in mine:
            live = parse_time(e.get("published_at")) or parse_time(e.get("recorded"))
            if not live:
                continue
            when = "; ".join(f"{hours_label(h)} {clock(live + datetime.timedelta(hours=h), zone)}" for h in hours)
            names = ", ".join(f"{hours_label(h)}-analytics.png" for h in hours)
            lines.append(f"- `{e.get('job_post')}` ({e.get('account')}): {when}. Folder `proof/{e.get('job_post')}/`: "
                         f"{names}, submission.png (the campaign's confirmation).")
    lines += ["", "The skill never submits for you and never opens your logged-in browser: you paste each link into "
              "the campaign yourself.", ""]
    text = "\n".join(lines)
    write_text(os.path.join(job_dir, "submit.md"), text)
    print()
    print(text.rstrip())


def remember_accounts(job_path):
    """Save the job's accounts to <user_home>/accounts.json, keyed by platform and handle. Saved are the
    choices worth suggesting next time (comments, duets, stitches, YouTube visibility, made for kids,
    audience), never the WoopSocial id, the TikTok privacy choice or the marketplace verification:
    those are read or asked again for every campaign."""
    job = read_json(job_path, "the campaign job")
    accs = job.get("accounts") if isinstance(job, dict) else None
    if not isinstance(accs, list) or not accs:
        die(f"{rel(job_path)} has no accounts to save")
    keep = ("name", "platform", "handle", "allowComment", "allowDuet", "allowStitch", "privacy", "madeForKids", "audience")
    saved = {account_key(a): a for a in load_saved_accounts() if account_key(a)}
    n = 0
    for a in accs:
        k = account_key(a) if isinstance(a, dict) else None
        if not k:
            die(f"every account to save needs its platform and handle ({a.get('name') if isinstance(a, dict) else a} "
                "has none): saved accounts are matched on both")
        cur = dict(saved.get(k, {}))
        cur.update({x: a[x] for x in keep if x in a})
        cur["platform"] = str(a["platform"]).strip().upper()
        saved[k] = cur
        n += 1
    path = os.path.join(user_home(), "accounts.json")
    write_json(path, {"accounts": list(saved.values())})
    print(f"saved {n} account(s) to {path}. Next campaign, check_clips.py shows their choices as suggestions: confirm "
          "them with the user and write them into clipjob.json. The WoopSocial id comes from social_accounts_list each "
          "time, and TikTok's privacy choice and the marketplace verification are asked each time")


def main():
    ap = argparse.ArgumentParser(description="Plan a campaign batch, then record what went out.")
    ap.add_argument("job")
    ap.add_argument("--media", help="media.json: {clip file: {mediaId, sha256}} after uploading")
    ap.add_argument("--posted", nargs=2, metavar=("REQUEST", "POST_ID"), help="record a request that was sent")
    ap.add_argument("--status", nargs="+", metavar="ARG",
                    help="the saved posts_get reply, and the post id when the reply doesn't carry it")
    ap.add_argument("--posted-by-hand", nargs=2, metavar=("POST", "URL"), help="record a post made in the app")
    ap.add_argument("--at", help="with --posted-by-hand: when it went live. Without a zone it is read in the job's "
                                 "timezone (your clock): 2026-11-16T09:05; with one: 2026-11-16T14:05Z")
    ap.add_argument("--failed", metavar="JOB_POST_ID", help="a post that failed to publish: release it from the ledger")
    ap.add_argument("--checked", action="store_true", help="with --failed: social_account_posts_list shows the clip "
                                                           "isn't on the account")
    ap.add_argument("--remember-accounts", action="store_true", help="save the accounts for the next campaign")
    ap.add_argument("--ledger", help="the ledger file (default: AI_CLIPPING_LEDGER, else ~/.ai-clipping/ledger.json)")
    a = ap.parse_args()
    if a.status and len(a.status) > 2:
        die("--status takes the saved reply and, if it doesn't carry one, the post id: --status status.json <postId>")
    if a.posted:
        record_posted(a.job, *a.posted, ledger_file=a.ledger)
        if a.status:
            apply_status(a.job, a.status[0], a.status[1] if len(a.status) > 1 else a.posted[1], a.ledger)
    elif a.status:
        apply_status(a.job, a.status[0], a.status[1] if len(a.status) > 1 else None, a.ledger)
    elif a.posted_by_hand:
        record_by_hand(a.job, *a.posted_by_hand, at=a.at, ledger_file=a.ledger)
    elif a.failed:
        release(a.job, a.failed, a.ledger, a.checked)
    elif a.remember_accounts:
        remember_accounts(a.job)
    else:
        plan(a.job, a.media, a.ledger)


if __name__ == "__main__":
    guard(main)
