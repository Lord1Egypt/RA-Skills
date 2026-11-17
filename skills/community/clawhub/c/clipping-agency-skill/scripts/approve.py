#!/usr/bin/env python3
"""The client's approval: one small page per episode batch, and the client's plain-text reply recorded.

    python3 scripts/approve.py <batch.json>                       # check, then write approval/approve-<episode>.html
    python3 scripts/approve.py <batch.json> --clips-url URL       # the page links each clip at URL/<file>
                                                                  #   (a shared folder the agency already uses)
    python3 scripts/approve.py <batch.json> --embed               # put the clips inside the page (small batches)
    python3 scripts/approve.py <batch.json> --sent [--at TIME]    # the page went to the client now (or at TIME)
    python3 scripts/approve.py <batch.json> --apply reply.txt [--received TIME] [--page N] [--by NAME] [--partial]
    python3 scripts/approve.py <batch.json> --status              # each clip's decision

The page is one HTML file that works with no JavaScript: it opens as an email attachment, in a phone's
file preview or in any browser. Per clip: a cover picture linked to the clip, the hook, why it was
picked, each platform's caption and the YouTube title and settings, the planned time in the client's
time zone, anything to know (a paid label, possible music). At the bottom, the reply to write back by
any channel (email, chat, text), for example:

    Page 2
    1: yes
    2: change: start on the second sentence
    3: skip
    TikTok: everyone, comments on, duets off, stitches off
    Name: Jordan Example

`--apply` reads that text against the record of the page that was sent (approvals.json holds each
page's number, its batch fingerprint and every clip's fingerprint, and the approval rule printed on
it), so a decision only counts for a clip that is still exactly what the client saw. Safety over
convenience: it records a reply only when every line reads one way, and prints each line with what it
gave. It refuses, and shows what it understood, when a line could mean two things ("all yes but skip 3",
"1: yes but change the caption"), when a clip is named but not answered, and when a clip on the page has
no answer (--partial records the answers given; the rest wait). Any reply to a page, even a refused one,
ends approval on silence for that page. It also refuses a reply for an older page once a newer one was
sent, a reply from someone who isn't an approver, and a reply that changes nothing. A skip or change on a
clip already scheduled marks the post for cancelling and prints the posts_delete step, even when the
clip was edited after the page was made. On pages with JavaScript, an optional helper writes the reply
from buttons.

Files, next to batch.json: approval/approve-<episode>.html and approvals.json.
"""
import argparse, base64, datetime, email.utils, hashlib, html, json, math, os, re, sys, unicodedata, urllib.parse

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (LIMITS, MB, PRIV_WORDS, TIKTOK_PRIVACY, accounts_of, clear_requests, client_busy,  # noqa: E402
                       client_clock, clock, connected_id, die, guard, iso, now_utc, parse_time, parse_user_time,
                       plan_slots, plural, read_json, read_text, rel, save_ledger, write_json, write_text)
from check_clips import check_batch, summary  # noqa: E402

EMBED_LIMIT = 15 * MB   # --embed refuses more than this: a page that size doesn't open as an attachment
PRIV_LABEL = {"PUBLIC_TO_EVERYONE": "Everyone", "FOLLOWER_OF_CREATOR": "Followers",
              "MUTUAL_FOLLOW_FRIENDS": "Friends (followers you follow back)", "SELF_ONLY": "Only me"}
WORD_PRIV = {"everyone": "PUBLIC_TO_EVERYONE", "public": "PUBLIC_TO_EVERYONE", "followers": "FOLLOWER_OF_CREATOR",
             "friends": "MUTUAL_FOLLOW_FRIENDS", "only me": "SELF_ONLY", "just me": "SELF_ONLY", "private": "SELF_ONLY"}
# The plain-text reply. Safety over convenience: a reply is recorded only when every line of it is read one
# way; anything else is refused with what was understood, for the agency to confirm with the client.
APPROVE_PHRASES = ["no changes needed", "no change needed", "nothing to change", "change nothing", "no changes",
                   "no change", "no notes", "no edits", "looks good", "yes please", "yes", "yep", "yeah", "ok", "okay",
                   "approved", "approve", "good", "great", "perfect", "fine", "go"]
REVISE_PHRASES = ["change", "changes", "changed", "revise", "edit", "fix", "tweak"]
REJECT_PHRASES = ["do not post", "don't post", "dont post", "not this one", "leave it out", "leave out", "no thanks",
                  "no good", "no way", "skip", "nope", "no", "drop", "reject", "rejected", "stop", "pass"]
PHRASE = {**{p: "approve" for p in APPROVE_PHRASES}, **{p: "revise" for p in REVISE_PHRASES},
          **{p: "reject" for p in REJECT_PHRASES}}
_ALT = "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in sorted(PHRASE, key=len, reverse=True))
_NUM = r"(?:(?:clip|number|no\.)\s*#?\s*|#\s*)?\d{1,2}"
ANCHOR_RE = re.compile(r"(?i)(?<![\w'])(?<!\d[:.])(?P<nums>" + _NUM + r"(?:\s*(?:,|&|/|\band\b)\s*" + _NUM
                       + r")*)(?!\s*[:.]\s*\d)\s*(?:[:.)=\-]\s*)?(?P<dec>" + _ALT + r")(?![\w'])\s*:?")
LABEL_RE = re.compile(r"(?i)^\s*(?:(?:clip|number|no\.)\s*#?\s*(\d{1,2})|#\s*(\d{1,2})|(\d{1,2})(?=\s*[:.)=\-]|\s|$))"
                      r"(?!\s*[:.]\s*\d)\s*[:.)=\-]?\s*(.*)$")
META_RE = re.compile(r"(?i)^\s*(?:name|from|date|tik\s*tok|subject|to|cc|sent|re)\s*:")
NEUTRAL_RE = re.compile(r"(?i)\b(?:no\s+(?:problem|worries|rush)|thank(?:s|\s+you)(?:\s+so\s+much)?|no\s+changes?"
                        r"(?:\s+needed)?|no\s+notes|no\s+edits|nothing\s+to\s+change|change\s+nothing)\b")
CONTRAST_RE = re.compile(r"(?i)\b(?:but|except|apart|other\s+than|besides|however|unless|only\s+if|although|though|"
                         r"instead|otherwise|rest|others|maybe|perhaps|not\s+sure|unsure)\b|\?")
NEGATION_RE = re.compile(r"(?i)\b(?:not|don't|dont|do\s+not|never|no|nope)\b")
REVISE_RE = re.compile(r"(?i)\b(?:change[sd]?|revise|edits?|fix|tweak)\b")
REJECT_RE = re.compile(r"(?i)\b(?:skip|drop|reject(?:ed)?|remove|delete|pass|stop|kill|no|nope)\b")
APPROVE_RE = re.compile(r"(?i)\b(?:yes|yep|yeah|ok|okay|approved?|good|great|perfect|fine|go)\b")
UNIT = r"(?:sec|secs|seconds?|s|min|mins|minutes?|words?|sentences?|lines?|frames?|x|times?|st|nd|rd|th|%|am|pm|" \
       r"jan\w*|feb\w*|mar\w*|apr\w*|may|jun\w*|jul\w*|aug\w*|sep\w*|oct\w*|nov\w*|dec\w*)"
BARE_NUM_RE = re.compile(r"(?i)(?<![\w'#.:/+-])(?<!\d[:.])(\d{1,2})(?!\s*[:.]\s*\d)(?!\s*" + UNIT + r"\b)(?![\w%])")
REVERSED_RE = re.compile(r"(?i)\b(?:skip|drop|remove|cut|kill|lose|reject|not|except|apart\s+from|other\s+than|besides|"
                         r"but|change|edit|fix|yes(?:\s+to)?|approve|post)\s+(?:for\s+|on\s+)?(?:the\s+)?"
                         r"(?:clip|number|no\.|#)?\s*(\d{1,2})(?!\s*" + UNIT + r"\b)(?![\w%:])")
WORDNUM_RE = re.compile(r"(?i)\b(?:(?:clip|number|no\.?)\s+(?:one|two|three|four|five|six|seven|eight|nine|ten)|"
                        r"(?:first|second|third|fourth|fifth|last|other)\s+(?:one|clip|video))\b")
ALL_RE = re.compile(r"(?i)\b(?:(?:all|everything|every\s+clip|all\s+of\s+them|all\s+\w+\s+clips|them\s+all)\s+"
                    r"(?:(?:is|are|look|looks|seem|seems)\s+)?(?:yes|good|great|approved?|ok|okay|fine|perfect)|"
                    r"(?:yes|approved?|ok|okay|go)\s+(?:to\s+|for\s+|on\s+)?(?:all|everything|them\s+all))\b")
CUT_RE = re.compile(r"(?im)^\s*(?:-{2,}\s*original\s+message.*|_{5,}|on\s.{0,200}\swrote:\s*|-- ?)$")
SAID = {"approve": "approve", "revise": "change", "reject": "skip"}


def esc(s):
    return html.escape(str(s), quote=True)


def approvals_path(m):
    return os.path.join(m["bdir"], "approvals.json")


def load_approvals(m):
    p = approvals_path(m)
    if not os.path.exists(p):
        return {"pages": [], "decisions": {}, "tiktok": None, "replies": []}
    d = read_json(p, "the approvals record")
    if not isinstance(d, dict) or not isinstance(d.get("pages", []), list) or not isinstance(d.get("decisions", {}), dict):
        die(f"{rel(p)} is damaged. It was left as it is: it is the record of what the client approved")
    d.setdefault("pages", [])
    d.setdefault("decisions", {})
    d.setdefault("tiktok", None)
    d.setdefault("replies", [])
    for i, pg in enumerate(d["pages"]):
        pg.setdefault("seq", i + 1)
        pg.setdefault("order", list((pg.get("clips") or {}).keys()))
        first = next((r.get("at") for r in d["replies"] if r.get("page") == pg["seq"]), None)
        if first and not pg.get("answered"):
            pg["answered"] = first
    return d


def page_replied(appr, pg):
    """True once any reply to this page came in, recorded or refused."""
    return bool(pg.get("answered") or pg.get("held") or any(r.get("page") == pg.get("seq") for r in appr["replies"]))


def page_rule(pg):
    """The approval rule printed on this page. A page without one (or with an incomplete one) is hold."""
    r = pg.get("rule") if isinstance(pg.get("rule"), dict) else {}
    if (r.get("rule") == "auto_after_hours" and isinstance(r.get("hours"), (int, float)) and r["hours"] > 0
            and isinstance(r.get("agreed_in_writing"), str) and r["agreed_in_writing"].strip()):
        return r
    return {"rule": "hold"}


def rule_now(c):
    ap = c.get("approval") if isinstance(c.get("approval"), dict) else {}
    if ap.get("rule") == "auto_after_hours":
        return {"rule": "auto_after_hours", "hours": ap.get("hours"), "agreed_in_writing": ap.get("agreed_in_writing")}
    return {"rule": "hold"}


def silence_due(pg):
    """When silence starts to count for this page: the later of the date printed on the page and the agreed
    hours after it was sent. None when the page's rule is hold or it wasn't sent."""
    r = page_rule(pg)
    sent = parse_time(pg.get("sent"))
    if r["rule"] != "auto_after_hours" or not sent or pg.get("answered") or pg.get("held"):
        return None   # any reply to the page, even one only partly answered or refused, ends approval on silence
    due = sent + datetime.timedelta(hours=float(r["hours"]))
    shown = parse_time(pg.get("deadline"))
    return max(due, shown) if shown else due


def valid_approval(appr, row):
    """The client's decision for this clip, only while the clip is exactly what they decided on."""
    d = appr["decisions"].get(row["id"])
    if d and d.get("hash") == row.get("hash"):
        return d
    return None


def current_page(m, appr):
    return next((p for p in reversed(appr["pages"]) if p.get("fp") == m["fp"]), None) if m.get("fp") else None


def newest_page(appr):
    return max(appr["pages"], key=lambda p: p.get("seq", 0)) if appr["pages"] else None


def decisions(m, appr, now=None):
    """{clip id: decision} that hold right now: the client's recorded decision while the clip is exactly
    what they decided on, and, only when the page the client was sent printed an approval-on-silence rule
    agreed in writing, "approve" for a clip of that page they didn't answer, once its deadline passed."""
    now = now or now_utc()
    out = {}
    pg = current_page(m, appr)
    due = silence_due(pg) if pg else None
    for r in m["rows"]:
        if not r.get("hash"):
            continue
        d = valid_approval(appr, r)
        if d:
            out[r["id"]] = d
        elif due and now >= due and (pg["clips"].get(r["id"]) or {}).get("hash") == r["hash"]:
            rule = page_rule(pg)
            out[r["id"]] = {"decision": "approve", "hash": r["hash"], "sha256": r["sha256"], "fp": pg["fp"],
                            "page": pg.get("seq"), "at": iso(due),
                            "by": f"no reply by the deadline on page {pg.get('seq')}, as agreed in writing",
                            "agreement": rule["agreed_in_writing"].strip(), "how": "auto"}
    return out


def ledger_posts(m, clip_id=None):
    return [(k, e) for k, e in m["ledger"]["posts"].items()
            if e.get("client") == m["cid"] and e.get("episode") == m["episode"].get("id")
            and (clip_id is None or e.get("clip") == clip_id)]


def planned_times(m, appr=None):
    """{clip id: planned time} for the clips not decided against, after the client's other posts, and the
    time of each clip already scheduled."""
    c = m["client"]
    tt = connected_id(accounts_of(c).get("TIKTOK"))
    busy, tt_busy = client_busy(m["ledger"], m["cid"], tt, exclude_episode=m["episode"].get("id"))
    live = {e.get("clip") for _, e in ledger_posts(m) if e.get("status") not in ("cancelled", "failed", "cancel_requested")}
    todo = [r for r in m["rows"] if r["id"] not in live
            and not (appr and (valid_approval(appr, r) or {}).get("decision") == "reject")]
    nb = parse_time(m["episode"].get("published")) if m["episode"].get("not_before_published", True) else None
    slots = plan_slots(c, len(todo), busy, tt_busy, now=now_utc(), not_before=nb)
    out = {r["id"]: slots[i] for i, r in enumerate(todo) if i < len(slots)}
    for _, e in ledger_posts(m):
        if e.get("status") in ("scheduled", "processing") and parse_time(e.get("scheduledFor")):
            out[e.get("clip")] = parse_time(e["scheduledFor"])
    return out


def data_uri(path, mime):
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#14171c;--mute:#5b6472;--line:#e3e6eb;--acc:#2457d6;--on-acc:#fff;--ok:#137a3a;--warn:#9a5b00;--chip:#eef1f5}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a20;--ink:#e9ecf1;--mute:#a1a9b6;--line:#2a2f38;--acc:#7aa2ff;--on-acc:#0f1115;--ok:#5fd18d;--warn:#f0b35a;--chip:#232833}}
a{color:var(--acc)}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:680px;margin:0 auto;padding:20px 16px 64px}h1{font-size:23px;line-height:1.25;margin:0 0 6px}h2{font-size:18px;margin:26px 0 8px}
.sub{color:var(--mute);margin:0 0 14px}.banner{border:1px solid var(--line);background:var(--card);border-radius:12px;padding:12px 14px;margin:0 0 12px}
.example{border-color:var(--warn)}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin:0 0 16px}
.top{display:flex;gap:14px;align-items:flex-start}.vid{flex:0 0 132px}.vid img,.vid video{width:132px;aspect-ratio:9/16;border-radius:10px;background:#000;object-fit:cover;display:block}
.vid a{font-size:14px;display:block;margin-top:4px}
.k{font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);font-weight:650;margin:10px 0 2px}.n{font-size:20px;font-weight:750;margin:0}
.hook{font-weight:700;font-size:17px;margin:2px 0 0}.cap{white-space:pre-wrap;margin:0;font-size:15px;overflow-wrap:anywhere}.when{font-weight:600;margin:0}
.flag{color:var(--warn);font-size:14px;margin:6px 0 0}.small{font-size:14px;color:var(--mute)}.done{color:var(--ok);font-weight:650}
pre{white-space:pre-wrap;background:var(--chip);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,Consolas,monospace;margin:8px 0}
.btn{display:inline-block;padding:12px 16px;border:0;border-radius:12px;background:var(--acc);color:var(--on-acc);font:inherit;font-weight:700;text-decoration:none;cursor:pointer}
.helper .choice{display:flex;gap:6px;margin-top:10px}.helper .choice button{flex:1;padding:9px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:inherit;font:inherit;font-weight:600}
.helper .choice button[aria-pressed=true]{border-color:var(--acc);color:var(--acc);background:var(--chip)}
textarea{width:100%;font:inherit;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px}
@media (max-width:480px){.vid{flex-basis:104px}.vid img,.vid video{width:104px}h1{font-size:21px}}
"""


def deadline_text(pg, zone):
    t = parse_time(pg.get("deadline"))
    return client_clock(t, zone) if t else None


def reply_template(m, seq, n):
    lines = [f"Page {seq}, {m['client'].get('name')} {m['episode'].get('id')}"]
    lines += [f"{i}:" for i in range(1, n + 1)]
    if "TIKTOK" in m["plats"]:
        lines.append("TikTok:")
    lines.append("Name:")
    return "\n".join(lines)


def page(m, appr, pg, times, media):
    """The page as HTML. pg is the page record (seq, rule, deadline). media: {clip id: (kind, src)}."""
    c, ep = m["client"], m["episode"]
    zone = c.get("timezone")
    tz_on = "TIKTOK" in m["plats"]
    sponsored = any(r.get("sponsor") for r in m["rows"])
    acc = accounts_of(c).get("TIKTOK") or {}
    opts = [o for o in (acc.get("privacyOptions") or TIKTOK_PRIVACY) if o in TIKTOK_PRIVACY]
    agency = c.get("agency") if isinstance(c.get("agency"), dict) else {}
    yt = c.get("youtube") if isinstance(c.get("youtube"), dict) else {}
    seq, n = pg["seq"], len(m["rows"])
    rule = page_rule(pg)
    title = f"Clips to approve: {c.get('name')}, page {seq}"
    out = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
           f"<title>{esc(title)}</title><style>{CSS}</style></head><body><main>",
           f"<h1>{esc(c.get('name'))}: clips to approve</h1>",
           f"<p class=\"sub\">Page {seq}. {esc(ep.get('title') or ep.get('id'))}"
           + (f" (recorded {esc(ep['recorded'])})" if ep.get("recorded") else "") + ". "
           + plural(n, "clip") + " for " + esc(", ".join(LIMITS[p]["label"] for p in m["plats"])) + ".</p>"]
    if c.get("example") is True:
        out.append("<div class=\"banner example\"><strong>EXAMPLE ONLY.</strong> A made-up client on NASA archive footage: "
                   "the show, the accounts and the times are invented, nothing here is posted, and NASA endorses "
                   "nothing.</div>")
    if rule["rule"] == "auto_after_hours":
        when = deadline_text(pg, zone)
        rtext = (f"<strong>If we haven't heard from you by {esc(when)}</strong>, the clips you haven't answered go out "
                 f"around their planned times, as agreed in writing ({esc(rule['agreed_in_writing'])}); we always "
                 f"give you at least {esc(rule['hours'])} hours from when we send this page. A clip you mark change or "
                 "skip never goes out as it is.")
    else:
        rtext = ("<strong>Nothing is posted until you reply.</strong> A clip you mark change or skip never goes out as "
                 "it is.")
    out.append(f"<div class=\"banner\">Watch each clip, then reply with one line per clip number: <strong>yes</strong>, "
               f"<strong>change:</strong> and what to change, or <strong>skip</strong>. The reply to copy is at the "
               f"bottom. {rtext} Times can move to the next free slot if your reply comes later.</div>")
    for i, r in enumerate(m["rows"], 1):
        clip = r["clip"]
        kind, src = media.get(r["id"], ("none", ""))
        poster = data_uri(r["cover"], "image/jpeg") if r.get("cover") else ""
        out.append(f"<section class=\"card\" id=\"c{i}\"><div class=\"top\"><div class=\"vid\">")
        if kind == "embed":
            out.append(f"<video controls playsinline preload=\"none\" poster=\"{poster}\" src=\"{esc(src)}\"></video>")
        elif kind == "url":
            out.append(f"<a href=\"{esc(src)}\"><img src=\"{poster}\" alt=\"Clip {i}, tap to watch\"></a>"
                       f"<a href=\"{esc(src)}\">Watch clip {i}</a>")
        else:
            out.append(f"<a href=\"{esc(src)}\"><img src=\"{poster}\" alt=\"Clip {i}\"></a>"
                       f"<a href=\"{esc(src)}\">{esc(os.path.basename(src))}</a>")
        out.append("</div><div>")
        out.append(f"<p class=\"n\">Clip {i}</p><div class=\"small\">"
                   + (f"{r['info']['duration']:.0f} seconds" if r.get("info") else "") + "</div>")
        if clip.get("hook"):
            out.append(f"<p class=\"hook\">{esc(clip['hook'])}</p>")
        out.append(f"<div class=\"k\">Why this moment</div><p class=\"cap\">{esc(clip.get('why'))}</p>")
        sched = [e for _, e in ledger_posts(m, r["id"]) if e.get("status") in ("scheduled", "processing")]
        live = [e for _, e in ledger_posts(m, r["id"]) if e.get("status") == "published"]
        when = times.get(r["id"])
        if live:
            state = "Already live."
        elif sched:
            state = (f"Already scheduled for {client_clock(when, zone)}. Reply \"{i}: skip\" to stop it before then."
                     if when else "Already scheduled.")
        else:
            state = f"Planned around {client_clock(when, zone)}" if when else "Planned after your reply"
        out.append(f"<div class=\"k\">When</div><p class=\"when\">{esc(state)}</p>")
        out.append("</div></div>")
        prior = valid_approval(appr, r)
        if prior:
            d, pgn = prior.get("decision"), prior.get("page")
            day = (parse_time(prior.get("at")) or now_utc())
            on = f" on page {pgn}" if pgn else ""
            if prior.get("how") == "auto":
                pg_old = next((p for p in appr["pages"] if p.get("seq") == pgn), {})
                dl = deadline_text(pg_old, zone) or client_clock(day, zone)
                out.append(f"<p class=\"small done\">No reply by {esc(dl)}, so this clip went ahead as agreed in writing "
                           f"({esc(prior.get('agreement') or '')}). It hasn't changed since.</p>")
            elif d == "approve":
                out.append(f"<p class=\"small done\">You approved this clip{on} ({esc(client_clock(day, zone)[:10])}); it "
                           "hasn't changed since. Write a new answer only if you changed your mind.</p>")
            else:
                out.append(f"<p class=\"small\">You chose {SAID.get(d, d)}{on}"
                           + (f" ({esc(prior.get('note'))})" if prior.get("note") else "") + ".</p>")
        caps = {k.upper(): v for k, v in (clip.get("captions") or {}).items()}
        for p in m["plats"]:
            out.append(f"<div class=\"k\">{esc(LIMITS[p]['label'])}</div>")
            if p == "YOUTUBE" and clip.get("title"):
                out.append(f"<p class=\"cap\"><strong>{esc(clip['title'])}</strong></p>")
            out.append(f"<p class=\"cap\">{esc(caps.get(p, ''))}</p>")
            if p == "YOUTUBE":
                out.append(f"<p class=\"small\">{esc(str(yt.get('privacy') or '').capitalize())}, "
                           + ("made for kids" if yt.get("madeForKids") else "not made for kids")
                           + (", tags: " + esc(", ".join(clip["tags"])) if clip.get("tags") else "") + "</p>")
        if clip.get("promotes_client_business") is True:
            out.append("<p class=\"flag\">Promotes your own business: TikTok shows it with the \"Your brand\" label.</p>")
        if r.get("sponsor"):
            out.append(f"<p class=\"flag\">Includes the sponsor segment for {esc(r['sponsor'])}: it goes out labelled as a "
                       "paid partnership.</p>")
        if r.get("music"):
            out.append("<p class=\"flag\">We may hear music in this clip. If it isn't music you have the rights to, "
                       "reply change and tell us.</p>")
        if clip.get("no_go_reviewed"):
            out.append(f"<p class=\"flag\">Touches a topic on your no-go list; our note: {esc(clip['no_go_reviewed'])}</p>")
        out.append(f"<div class=\"helper\" hidden><div class=\"choice\" data-i=\"{i}\"><button type=\"button\" "
                   "data-v=\"yes\">Yes</button><button type=\"button\" data-v=\"change\">Change</button><button "
                   "type=\"button\" data-v=\"skip\">Skip</button></div><textarea rows=\"2\" hidden "
                   f"aria-label=\"What should change in clip {i}\" placeholder=\"What should change?\"></textarea></div>")
        out.append("</section>")
    if tz_on:
        out.append("<h2>TikTok settings</h2><div class=\"card\"><p class=\"small\" style=\"margin:0\">TikTok asks you to "
                   "choose these yourself; we never choose them for you. Write them on the TikTok line of your reply: who "
                   "can see the posts (" + esc(", ".join(PRIV_WORDS[o] for o in opts if not (sponsored and o == "SELF_ONLY")))
                   + "), and comments, duets and stitches, each on or off."
                   + (" Only me isn't possible for a paid partnership." if sponsored and "SELF_ONLY" in opts else "") + "</p>")
        last = appr.get("tiktok") if isinstance(appr.get("tiktok"), dict) else None
        if last and last.get("privacyLevel") in PRIV_WORDS:
            out.append(f"<p class=\"small\">Your choice from page {esc(last.get('page') or '?')}: "
                       f"{esc(PRIV_WORDS[last['privacyLevel']])}, comments {'on' if last.get('allowComment') else 'off'}, "
                       f"duets {'on' if last.get('allowDuet') else 'off'}, stitches {'on' if last.get('allowStitch') else 'off'}. "
                       "It applies to these clips too unless your reply has a new TikTok line.</p>")
        out.append("</div>")
    tmpl = reply_template(m, seq, n)
    out.append("<h2>Your reply</h2><div class=\"card\"><p class=\"small\" style=\"margin:0\">Copy this into an email or a "
               "message to us and fill it in. After each number: <strong>yes</strong>, <strong>change:</strong> and what to "
               "change, or <strong>skip</strong>. Keep the page number at the top.</p>"
               f"<pre id=\"tmpl\">{esc(tmpl)}</pre>")
    if agency.get("reply_to"):
        href = ("mailto:" + urllib.parse.quote(agency["reply_to"], safe="@") + "?subject="
                + urllib.parse.quote(f"Clips: {c.get('name')}, page {seq}") + "&body=" + urllib.parse.quote(tmpl + "\n"))
        out.append(f"<p><a class=\"btn\" id=\"mail\" href=\"{esc(href)}\">Reply by email to {esc(agency.get('name') or agency['reply_to'])}"
                   "</a></p>")
    out.append("<div class=\"helper\" hidden><p class=\"small\">Or tap the buttons on each clip and this box fills in:</p>"
               "<textarea id=\"reply\" rows=\"7\"></textarea></div></div>")
    names = [a.get("name") for a in c.get("approvers") or [] if isinstance(a, dict)]
    out.append("<p class=\"small\">Made for " + esc(", ".join(x for x in names if x) or "the client")
               + ". Please don't forward this page.</p>")
    cfg = {"n": n, "seq": seq, "head": tmpl.splitlines()[0], "tiktok": tz_on}
    js = json.dumps(cfg).replace("</", "<\\/")
    out.append("<script>var C=" + js + ";" + r"""
(function(){var d={},notes={};document.querySelectorAll('.helper').forEach(function(h){h.hidden=false});
var box=document.getElementById('reply'),mail=document.getElementById('mail'),base=mail?mail.getAttribute('href').split('&body=')[0]:'';
function write(){var L=[C.head];for(var i=1;i<=C.n;i++){var v=d[i]||'';L.push(i+': '+(v=='change'?'change: '+(notes[i]||''):v))}
 if(C.tiktok)L.push('TikTok:');L.push('Name:');box.value=L.join('\n');if(mail)mail.setAttribute('href',base+'&body='+encodeURIComponent(box.value+'\n'))}
document.querySelectorAll('.choice').forEach(function(g){var i=+g.getAttribute('data-i'),ta=g.parentNode.querySelector('textarea');
 g.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){d[i]=b.getAttribute('data-v');
  g.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});ta.hidden=d[i]!='change';write()})});
 ta.addEventListener('input',function(){notes[i]=ta.value.replace(/\s+/g,' ').trim();write()})});write()})();
</script></main></body></html>""")
    return "\n".join(out)


def media_for(m, mode, clips_url, pdir):
    out = {}
    for r in m["rows"]:
        if mode == "embed":
            out[r["id"]] = ("embed", data_uri(r["file"], "video/mp4"))
        elif clips_url:
            out[r["id"]] = ("url", clips_url.rstrip("/") + "/" + urllib.parse.quote(os.path.basename(r["file"])))
        else:
            try:
                src = os.path.relpath(r["file"], pdir).replace(os.sep, "/")
            except ValueError:   # another drive on Windows
                src = "file:///" + os.path.abspath(r["file"]).replace(os.sep, "/")
            out[r["id"]] = ("file", src)
    return out


def build(batch_path, ledger_file=None, embed=False, clips_url=None):
    m = check_batch(batch_path, ledger_file)
    lines, errs, warns = summary(m)
    if errs:
        print("\n".join(lines))
        die(f"{errs} error(s): fix them and run this again. No page was made (the client only sees clips that pass)")
    if clips_url and not re.match(r"(?i)^https://", clips_url):
        die("--clips-url is the https link of the shared folder that holds the clip files")
    appr = load_approvals(m)
    times = planned_times(m, appr)
    total = sum(os.path.getsize(r["file"]) for r in m["rows"])
    if embed and total > EMBED_LIMIT:
        die(f"the clips are {total / MB:.0f} MB together: too big to put inside one page that still opens as an "
            "attachment. Share the clips folder and pass --clips-url, or send the clips with the page")
    now = now_utc()
    rule = rule_now(m["client"])
    last = newest_page(appr)
    deadline = None
    if rule["rule"] == "auto_after_hours":
        deadline = now + datetime.timedelta(hours=float(rule["hours"]))
        deadline = deadline.replace(minute=0, second=0) + datetime.timedelta(hours=1) if deadline.minute or deadline.second else deadline
    record = {"fp": m["fp"], "made": iso(now), "sent": None, "rule": rule, "deadline": iso(deadline) if deadline else None,
              "clips": {r["id"]: {"hash": r["hash"], "sha256": r["sha256"]} for r in m["rows"]},
              "order": [r["id"] for r in m["rows"]], "planned": {k: iso(v) for k, v in times.items()}}
    if last and last.get("fp") == m["fp"] and not last.get("sent") and page_rule(last) == page_rule(record):
        last.update({k: v for k, v in record.items() if k not in ("made",)})
        pg = last
    elif last and last.get("fp") == m["fp"] and last.get("sent") and page_rule(last) == page_rule(record):
        pg = last   # the page already sent: write the same page again, nothing new for the client
    else:
        record["seq"] = (last.get("seq", 0) if last else 0) + 1
        record["page"] = None
        appr["pages"].append(record)
        pg = record
    pdir = os.path.join(m["bdir"], "approval")
    path = os.path.join(pdir, f"approve-{m['episode'].get('id')}.html")
    pg["page"] = rel(path, m["bdir"])
    mode = "embed" if embed else ("url" if clips_url else "file")
    pg["media"] = mode if mode != "url" else clips_url
    write_text(path, page(m, appr, pg, times, media_for(m, mode, clips_url, pdir)))
    write_json(approvals_path(m), appr)
    ledger = m["ledger"]
    for r in m["rows"]:   # each clip file now belongs to this client: no other client can get the same file
        ledger["clips"].setdefault(r["sha256"], {"client": m["cid"], "episode": m["episode"].get("id"), "clip": r["id"],
                                                 "at": iso(now)})
    gone = clear_requests(m["bdir"], ledger, m["cid"], m["episode"].get("id"))
    save_ledger(m["lpath"], ledger)
    if warns:
        print("\n".join(l for l in lines if not l.startswith("note")))
    if gone:
        print(f"removed {plural(len(gone), 'unsent request')} written before this page: run schedule.py again after the reply")
    size = os.path.getsize(path)
    print(f"approval page {pg['seq']}: {rel(path)} ({size / 1000:.0f} kB, {plural(len(m['rows']), 'clip')}, batch {m['fp'][:8]})")
    if mode == "file":
        print("the page links the clip files next to it (../clips/). Send the clips with it (attach them, or share the "
              "episode folder), or share the clips folder you already use and make the page again with --clips-url")
    if deadline:
        print(f"the page says: no reply by {client_clock(deadline, m['client'].get('timezone'))} counts as a yes "
              "(at least the agreed hours after sending). Send it now, or make it again on the day you send it")
    print(f"send it to {', '.join(a.get('name') for a in m['client'].get('approvers') or [] if isinstance(a, dict))}, "
          "then run approve.py --sent. When the reply comes back: approve.py --apply reply.txt")


def mark_sent(batch_path, ledger_file=None, at=None):
    m = check_batch(batch_path, ledger_file)
    appr = load_approvals(m)
    if not appr["pages"]:
        die("no approval page yet: run approve.py on the batch first")
    pg = newest_page(appr)
    if pg.get("fp") != m["fp"]:
        die("the batch changed after the last page was made: make a new page (approve.py) and send that one")
    if at:
        t, _, prob = parse_user_time(at, m["client"].get("timezone"))
        if prob:
            die(prob)
    else:
        t = now_utc()
    pg["sent"] = iso(t)
    write_json(approvals_path(m), appr)
    zone = m["client"].get("timezone")
    extra = ""
    due = silence_due(pg)
    if due:
        shown = parse_time(pg.get("deadline"))
        extra = f"; clips not answered count as approved from {clock(due, zone)} (agreed in writing)"
        if shown and due > shown:
            extra += (f". The page says {client_clock(shown, zone)}; it was sent later, so silence counts only from "
                      "the agreed hours after sending")
    print(f"page {pg['seq']} ({pg['fp'][:8]}) sent {clock(t, zone)}{extra}")


def strip_quoted(text):
    """The reply without quoted lines ("> ...") from the message it answers."""
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(">"))


def normalize_reply(text):
    """The reply as plain lines: the same characters whatever app it was typed in (non-breaking and full-width
    spaces, full-width colons, curly quotes, en and em dashes, bullets, markdown, zero-width marks)."""
    t = unicodedata.normalize("NFKC", text.replace("\r\n", "\n").replace("\r", "\n"))
    t = re.sub(r"[​-‍⁠﻿]", "", t)
    t = re.sub(r"[‘’‚‛′`´]", "'", t)
    t = re.sub(r"[“”„‟«»″\"]", "", t)
    t = re.sub(r"[‐-―−﹘﹣]", "-", t)
    t = re.sub(r"[ \t  -   　]+", " ", t)
    t = re.sub(r"\*\*|__|~~|\*", "", t)
    t = re.sub(r"(?m)^\s*(?:[-+>•·◦▪▫‣⁃●○■□]\s+)+", "", t)
    mt = CUT_RE.search(t)   # the message this reply answers, or a signature, starts here
    return t[:mt.start()] if mt else t


def _scan(text, n, allow):
    """Words in a stretch of reply text that make an answer unclear. allow: the classes that may appear."""
    t = NEUTRAL_RE.sub(" ", text)
    out = []
    if "contrast" not in allow:
        out += [x.group(0) for x in CONTRAST_RE.finditer(t)]
    if "negation" not in allow:
        out += [x.group(0) for x in NEGATION_RE.finditer(t)]
    if "revise" not in allow:
        out += [x.group(0) for x in REVISE_RE.finditer(t)]
    if "reject" not in allow:
        out += [x.group(0) for x in REJECT_RE.finditer(t)]
    if "approve" not in allow:
        out += [x.group(0) for x in APPROVE_RE.finditer(t)]
    if "numbers" not in allow:
        out += [x.group(1) for x in BARE_NUM_RE.finditer(t) if 1 <= int(x.group(1)) <= max(n, 1) + 9]
    out += [x.group(0) for x in REVERSED_RE.finditer(t)] + [x.group(0) for x in WORDNUM_RE.finditer(t)]
    seen, keep = set(), []
    for w in out:
        if w.lower() not in seen:
            seen.add(w.lower())
            keep.append(w)
    return keep


def read_reply(text, n, drop=()):
    """Read a plain-text reply. Returns (answers {number: (decision, note)}, problems, lines read).

    Safety over convenience: an answer counts only when its line can be read one way. "All yes" counts only
    when nothing else in the reply hedges, skips, changes or names a clip. Any problem means nothing is
    recorded. lines read: [(the line as written, what it gave)] for the agency to see."""
    t = normalize_reply(text)
    found, probs, seen = {}, [], []
    note_for, note_open, all_hit = None, False, []

    def answer(nums, dec, note, line):
        for num in nums:
            if num < 1 or num > n:
                probs.append(f"the reply answers clip {num}, but the page has {plural(n, 'clip')}")
                continue
            if num in found and (found[num][0] != dec or (dec == "revise" and note and found[num][1] != note)):
                probs.append(f"clip {num} is answered twice ({SAID[found[num][0]]} and {SAID[dec]})")
                continue
            found[num] = (dec, note)

    def unclear(where, words, line):
        probs.append(f"unclear: \"{line.strip()}\"{where} also says {', '.join(repr(w) for w in words)}, so it could "
                     "mean more than one thing")

    def loose(chunk, line):
        if not chunk.strip(" ,;:.-!"):
            return
        hits = ALL_RE.findall(chunk)
        rest = ALL_RE.sub(" ", chunk)
        if hits:
            all_hit.append(line.strip())
        words = _scan(rest, n, allow={"approve"})
        if words:
            unclear("", words, line)

    for raw in t.split("\n"):
        if META_RE.match(raw):
            note_for = None
            continue
        line = re.sub(r"(?i)\bpage\s*#?\s*\d{1,3}\b", " ", raw)
        line = re.sub(r"(?i)\bep(?:isode)?\s*[-#.]?\s*\d+\b", " ", line)
        for d in drop:
            if d:
                line = re.sub(re.escape(d), " ", line, flags=re.I)
        if not line.strip(" ,;:.-!"):
            if note_for and note_open and found.get(note_for[0], ("", ""))[1]:
                note_for = None   # a blank line ends a change note
            continue
        ms = list(ANCHOR_RE.finditer(line))
        if not ms:
            lab = LABEL_RE.match(line)
            if lab:
                num = int(next(g for g in lab.groups()[:3] if g))
                rest = lab.group(4).strip(" ,;:.-")
                note_for = None
                if rest:
                    probs.append(f"clip {num}: couldn't read \"{rest}\" as yes, change: or skip")
                    seen.append((raw.strip(), "not read"))
                else:
                    seen.append((raw.strip(), f"clip {num}: no answer"))
                continue
            if note_for:
                words = [w for w in _scan(line, n, allow={"approve", "reject", "revise", "contrast", "negation",
                                                          "numbers"})]
                if words:
                    unclear(" (read as part of a change note)", words, line)
                for num in note_for:
                    if num in found:
                        dec, note = found[num]
                        found[num] = (dec, (note + " " + line.strip()).strip())
                note_open = True
                seen.append((raw.strip(), f"more of the change note for clip {', '.join(map(str, note_for))}"))
                continue
            loose(line, raw)
            seen.append((raw.strip(), "all yes" if ALL_RE.search(line) else "no answer in it"))
            continue
        loose(line[:ms[0].start()], raw)
        got = []
        note_for = None
        for k, mt in enumerate(ms):
            nums = [int(x) for x in re.findall(r"\d{1,2}", mt.group("nums"))]
            dec = PHRASE[re.sub(r"\s+", " ", mt.group("dec").lower())]
            end = ms[k + 1].start() if k + 1 < len(ms) else len(line)
            rest = line[mt.end():end]
            note = ""
            if dec == "approve":
                words = _scan(rest, n, allow=set())
                words = [w for w in words if not APPROVE_RE.fullmatch(w)]
                if words:
                    unclear(f" (clip {', '.join(map(str, nums))})", words, raw)
            elif dec == "reject":
                words = _scan(rest, n, allow={"reject", "negation"})
                if words:
                    unclear(f" (clip {', '.join(map(str, nums))})", words, raw)
            else:
                note = re.sub(r"(?i)\s*(?:,|;|\band)\s*$", "", rest.strip(" \t,;:-")).strip()
                words = _scan(note, n, allow={"approve", "reject", "revise", "contrast", "negation", "numbers"})
                if words:
                    unclear(f" (the change note for clip {', '.join(map(str, nums))})", words, raw)
                if k + 1 == len(ms):
                    note_for, note_open = nums, bool(note)
            answer(nums, dec, note, raw)
            got.append(f"clip {', '.join(map(str, nums))} {SAID[dec]}" + (f" ({note})" if note else ""))
        seen.append((raw.strip(), "; ".join(got)))
    for i, (dec, note) in sorted(found.items()):
        if dec == "revise" and not note:
            probs.append(f"clip {i}: change, but what should change? Ask the client and add it after \"change:\"")
    if all_hit:
        others = sorted(k for k, (d, _) in found.items() if d != "approve")
        if others or probs:
            probs.insert(0, "the reply says yes to all, but also " + (
                f"answers clip {', '.join(map(str, others))} another way" if others else "says something else")
                + "; ask the client which clips to post")
        else:
            for i in range(1, n + 1):
                found.setdefault(i, ("approve", ""))
    return found, probs, seen


def parse_reply(text, n, drop=()):
    """({number: (decision, note)}, problems) from a client's plain-text reply."""
    found, probs, _ = read_reply(text, n, drop)
    return found, probs


def parse_tiktok(text):
    """(choice dict or None, problem or None) from a "TikTok: ..." line."""
    mt = re.search(r"(?im)^[ \t]*tik[ \t]*tok[ \t]*:?[ \t]*(.*)$", text)
    if not mt or not mt.group(1).strip():
        return None, None
    line = mt.group(1).lower()
    aud = next((v for k, v in sorted(WORD_PRIV.items(), key=lambda x: -len(x[0])) if re.search(r"\b" + k + r"\b", line)), None)
    got = {}
    for key, word in (("allowComment", "comment"), ("allowDuet", "duet"), ("allowStitch", "stitch")):
        w = re.search(word + r"e?s?[ \t]*:?[ \t]*(on|off|yes|no|allowed|not allowed)\b", line)
        if w:
            got[key] = w.group(1) in ("on", "yes", "allowed")
        elif re.search(r"\bno " + word, line):
            got[key] = False
    missing = ([] if aud else ["who can see the posts"]) + [w for k, w in (("allowComment", "comments"), ("allowDuet", "duets"),
                                                                        ("allowStitch", "stitches")) if k not in got]
    if missing:
        return None, ("the TikTok line doesn't say " + ", ".join(missing) + ": nothing is chosen for the client, so "
                      "TikTok waits until they say it")
    return dict(privacyLevel=aud, **got), None


def hold_page(m, appr, pg, why, rec_t=None):
    """A reply came in for this page but couldn't be recorded: silence no longer approves anything on it."""
    pg.setdefault("held", []).append({"at": iso(now_utc()), "received": iso(rec_t) if rec_t else None, "why": why[:300]})
    write_json(approvals_path(m), appr)


def apply_reply(batch_path, reply, by=None, ledger_file=None, page_no=None, received=None, again=False, partial=False):
    m = check_batch(batch_path, ledger_file)
    zone = m["client"].get("timezone")
    text = read_text(reply) if os.path.isfile(reply) else reply
    body = strip_quoted(text)
    appr = load_approvals(m)
    if not appr["pages"]:
        die("no approval page was made for this episode yet")
    named = {int(x) for x in re.findall(r"(?i)\bpage[ \t ]*#?[ \t ]*(\d{1,3})\b", unicodedata.normalize("NFKC", body))}
    if len(named) > 1:
        die(f"the reply names more than one page ({', '.join(map(str, sorted(named)))}); apply one page's answers at a time")
    seq = page_no or (named.pop() if named else None)
    if seq is None:
        if len(appr["pages"]) > 1:
            die("the reply doesn't say which page it answers, and this episode has more than one. Check with the client "
                "and pass --page N")
        seq = appr["pages"][0]["seq"]
    pg = next((p for p in appr["pages"] if p.get("seq") == seq), None)
    if not pg:
        die(f"this episode ({m['episode'].get('id')} for {m['client'].get('name')}) has no page {seq}. Is the reply "
            "for another episode or another client?")
    top = newest_page(appr)
    newer = [p for p in appr["pages"] if p.get("seq", 0) > seq]
    unsent_newer = newer and all(not p.get("sent") and not page_replied(appr, p) for p in newer)
    if newer and not unsent_newer:
        die(f"the reply answers page {seq}, but page {top['seq']} is newer and was sent (made {top.get('made', '')[:10]}). "
            f"Nothing was recorded. Ask the client to answer page {top['seq']}; an older page's answers never overwrite "
            "newer ones")
    order = pg.get("order") or list(pg["clips"])
    drop = [m["client"].get("name"), m["client"].get("show"), m["episode"].get("id")]
    found, probs, seen = read_reply(body, len(order), drop=[x for x in drop if isinstance(x, str)])
    tk, tk_prob = parse_tiktok(body) if "TIKTOK" in m["plats"] else (None, None)
    rows = {r["id"]: r for r in m["rows"]}

    def refuse(msg):
        hold_page(m, appr, pg, msg)
        if seen:
            print("the reply, line by line, as read:")
            for line, got in seen:
                print(f"  {line[:90]}  ->  {got}")
        die(msg + f". Nothing was recorded, and silence no longer counts for page {seq}: its clips wait for a clear "
            "answer. Confirm with the client what they meant, then apply their clear answer (or pass --page and the "
            "answers as they confirmed them)")

    if probs:
        refuse("; ".join(probs))
    if not found and not tk:
        refuse("no answers found in that reply. Each clip's answer is its number, then yes, change: ..., or skip "
               "(\"1: yes\"). Paste the client's whole reply")
    open_clips = [i for i, k in enumerate(order, 1) if i not in found
                  and not (rows.get(k) and rows[k].get("hash") == pg["clips"][k]["hash"] and valid_approval(appr, rows[k]))]
    if open_clips and not partial:
        refuse(f"clip {', '.join(map(str, open_clips))} on page {seq} {'has' if len(open_clips) == 1 else 'have'} no answer "
               "in this reply. Ask the client about "
               + ("it" if len(open_clips) == 1 else "them") + ", or pass --partial to record only the answers given "
               "(the others then wait for an answer: silence won't approve them)")
    # who
    who, how_by = by, "entered by the agency (--by)" if by else None
    mby = re.search(r"(?im)^[ \t]*(?:from|name)[ \t]*:[ \t]*(.+?)[ \t]*$", body)
    if not who and mby:
        who, how_by = mby.group(1), "the Name or From line of the reply"
    if not who:
        die("who replied? The reply has no \"Name:\" or \"From:\" line; pass --by \"Name\"")
    who = re.sub(r"\s*<[^>]*>\s*$", "", who).strip().strip('"')
    approvers = [a for a in m["client"].get("approvers") or [] if isinstance(a, dict) and a.get("name")]
    match = next((a["name"].strip() for a in approvers if who.casefold() in (a["name"].strip().casefold(),
                                                                          str(a.get("contact") or "").strip().casefold())), None)
    if not match:
        die(f"{who} isn't one of {m['client'].get('name')}'s approvers ({', '.join(a['name'] for a in approvers)}). Ask the "
            "client, or add them to approvers in client.json if they now approve")
    who = match
    # when the client replied
    rec_t = None
    if received:
        rec_t, _, prob = parse_user_time(received, zone)
        if prob:
            die("--received: " + prob)
    else:
        dl = re.search(r"(?im)^[ \t]*date[ \t]*:[ \t]*(.+?)[ \t]*$", body)
        if dl:
            try:
                rec_t = email.utils.parsedate_to_datetime(dl.group(1)).astimezone(datetime.timezone.utc)
            except (TypeError, ValueError):
                rec_t = parse_time(dl.group(1))
    key = hashlib.sha256(json.dumps([seq, sorted((k, v[0], v[1]) for k, v in found.items()), tk], sort_keys=True)
                         .encode("utf-8")).hexdigest()[:16]

    def same_now(num, dec, note):
        k = order[num - 1]
        r = rows.get(k)
        if not r or r.get("hash") != pg["clips"][k]["hash"]:
            return False
        cur = valid_approval(appr, r)
        return bool(cur) and cur.get("decision") == dec and (dec != "revise" or (cur.get("note") or "") == note)
    last_tk = appr.get("tiktok") if isinstance(appr.get("tiktok"), dict) else {}
    tk_same = not tk or all(last_tk.get(x) == tk[x] for x in tk)
    if not again and tk_same and all(same_now(num, d_, n_) for num, (d_, n_) in found.items()):
        die(f"this reply for page {seq} changes nothing: every answer in it is already the decision on record (applied "
            "before). (--again records it once more)")
    now = iso(now_utc())
    done, void, changed = [], [], []
    for num, (dec, note) in sorted(found.items()):
        k = order[num - 1]
        r = rows.get(k)
        if not r or r.get("hash") != pg["clips"][k]["hash"]:
            void.append((num, k, dec))
            continue
        old = valid_approval(appr, r)
        if old and old.get("decision") != dec:
            changed.append(f"clip {num} ({k}): {SAID.get(old['decision'], old['decision'])} -> {SAID[dec]}")
        appr["decisions"][k] = {"decision": dec, "hash": r["hash"], "sha256": r["sha256"], "fp": pg["fp"], "page": seq,
                                "at": now, "received": iso(rec_t) if rec_t else None, "by": who, "by_source": how_by,
                                "how": "reply"}
        if note:
            appr["decisions"][k]["note"] = note
        done.append((num, k, dec, note))
    tk_rec = None
    if tk:
        acc = accounts_of(m["client"]).get("TIKTOK") or {}
        opts = acc.get("privacyOptions") or list(TIKTOK_PRIVACY)
        sponsored = any(r.get("sponsor") for r in m["rows"])
        if tk["privacyLevel"] not in opts:
            tk_prob = f"the client chose {PRIV_WORDS[tk['privacyLevel']]} on TikTok, which their account doesn't offer; ask again"
        elif sponsored and tk["privacyLevel"] == "SELF_ONLY":
            tk_prob = "only me isn't possible for a paid partnership on TikTok; ask the client again"
        else:
            tk_rec = dict(tk, fp=pg["fp"], page=seq, at=now, by=who)
            appr["tiktok"] = tk_rec
    pg.setdefault("answered", now)
    appr["replies"].append({"page": seq, "key": key, "at": now, "received": iso(rec_t) if rec_t else None, "by": who,
                            "by_source": how_by, "answers": {order[n_ - 1]: SAID[d_] for n_, (d_, _) in found.items()},
                            "recorded": [k for _, k, _, _ in done], "void": [k for _, k, _ in void],
                            "unanswered": [order[i - 1] for i in open_clips], "tiktok": bool(tk_rec)})
    write_json(approvals_path(m), appr)
    # anything not approved any more that is already handed to WoopSocial; a no on a clip edited since the page
    # was made still stops the post that went out from the version the client saw
    ledger = m["ledger"]
    cancels = []
    for num, k, dec in [(a_, b_, c_) for a_, b_, c_, _ in done] + void:
        if dec == "approve":
            continue
        for lk, e in ledger_posts(m, k):
            if e.get("status") in ("scheduled", "processing", "cancel_requested"):
                e["status"] = "cancel_requested"
                e["cancel_reason"] = f"client said {SAID[dec]} on page {seq}"
                e["cancel_dec"] = dec
                cancels.append(e)
            elif e.get("status") == "published":
                print(f"clip {num} ({k}) is already live on {e.get('platform')} ({e.get('url') or 'post ' + e.get('postId')}); "
                      "WoopSocial can't delete a live post. Tell the client today; it is removed in the app on that "
                      "account")
    gone = clear_requests(m["bdir"], ledger, m["cid"], m["episode"].get("id"))
    save_ledger(m["lpath"], ledger)
    rdir = os.path.join(m["bdir"], "requests")
    print("the reply, line by line, as read:")
    for line, got in seen:
        print(f"  {line[:90]}  ->  {got}")
    for pid in sorted({e["postId"] for e in cancels}):
        write_json(os.path.join(rdir, f"cancel-{pid}.json"), {"tool": "posts_delete", "postId": pid,
                                                             "why": next(e["cancel_reason"] for e in cancels if e["postId"] == pid)})
    for num, k, dec, note in done:
        print(f"clip {num} ({k}): {SAID[dec]}" + (f" ({note})" if note else ""))
    for c in changed:
        print(f"changed: {c}")
    for num, k, dec in void:
        print(f"clip {num} ({k}): no decision recorded: it changed after page {seq} was made (cut again or a caption "
              "edited). Make a new page for it" + (". Its scheduled post is cancelled all the same (below)" if dec != "approve"
                                                     and any(e.get("clip") == k for e in cancels) else ""))
    if open_clips:
        print(f"no answer yet (--partial): clip {', '.join(map(str, open_clips))}; they wait for the client, silence won't "
              "approve them")
    if tk_rec:
        print(f"TikTok: {PRIV_WORDS[tk_rec['privacyLevel']]}; comments {'on' if tk_rec['allowComment'] else 'off'}, duets "
              f"{'on' if tk_rec['allowDuet'] else 'off'}, stitches {'on' if tk_rec['allowStitch'] else 'off'}")
    elif tk_prob:
        print(f"TikTok: {tk_prob}")
    elif "TIKTOK" in m["plats"]:
        last = appr.get("tiktok")
        print(f"TikTok: no TikTok line in this reply; the client's choice from page {last.get('page')} still holds" if last
              else "TikTok: the client hasn't chosen yet, so TikTok waits; nothing is chosen for them")
    print(f"replied by {who} ({how_by}); "
          + (f"received {clock(rec_t, zone)}" if rec_t else "time the client replied: unknown (pass --received to record it)"))
    if unsent_newer:
        print(f"note: page {', '.join(str(p.get('seq')) for p in newer)} was made after page {seq} but never sent, so it "
              "doesn't count. Make the page again (approve.py) so it shows these answers, and send that one")
    if not pg.get("sent"):
        print(f"note: page {seq} was never marked sent; run approve.py --sent --at <time> so the turnaround is right")
    for pid in sorted({e["postId"] for e in cancels}):
        e = next(x for x in cancels if x["postId"] == pid)
        t = parse_time(e.get("scheduledFor"))
        print(f"CANCEL NOW: post {pid} (clip {e.get('clip')}, {clock(t, zone) if t else 'time unknown'}) is still "
              f"scheduled and the client said {SAID[e.get('cancel_dec', 'reject')]}. "
              f"posts_delete with postId {pid}, then: schedule.py {rel(m['batch_path'])} --cancelled {pid}")
    if gone:
        print(f"removed {plural(len(gone), 'unsent request')}; run schedule.py again to write new ones")
    revise = [str(num) for num, _, d, _ in done if d == "revise"]
    if revise:
        print(f"to change: clip {', '.join(revise)}. Make the change, run check_clips.py and approve.py again, and send "
              "the new page")
    if any(d == "approve" for _, _, d, _ in done):
        print("next: schedule.py on this batch")


def show(batch_path, ledger_file=None):
    m = check_batch(batch_path, ledger_file)
    appr = load_approvals(m)
    zone = m["client"].get("timezone")
    last = newest_page(appr)
    if last:
        print(f"page {last['seq']} ({last['fp'][:8]}) made {last['made']}, "
              + (f"sent {clock(parse_time(last['sent']), zone)}" if last.get("sent") else "not sent yet")
              + ("; rule: silence counts after " + clock(silence_due(last), zone) if silence_due(last) else
                 "; silence no longer counts: the client replied to this page" if page_rule(last)["rule"] ==
                 "auto_after_hours" and page_replied(appr, last) else "; rule: nothing posts without a reply"))
    now_d = decisions(m, appr)
    for r in m["rows"]:
        d = appr["decisions"].get(r["id"])
        posts = [e for _, e in ledger_posts(m, r["id"]) if e.get("status") == "cancel_requested"]
        if r["id"] in now_d and now_d[r["id"]].get("how") == "auto":
            state = "approve (" + now_d[r["id"]]["by"] + ")"
        elif not d:
            state = "waiting for the client"
        elif d.get("hash") != r.get("hash"):
            pg = current_page(m, appr)
            was = f"{d['decision']} by {d.get('by')}, then the clip changed: that decision no longer counts"
            state = was + ("; waiting for the client on the new page" if pg and pg.get("sent") else
                           "; send the client a new page" if pg else "; make a new page")
        else:
            state = (f"{d['decision']} by {d.get('by')} ({d.get('how')}" + (f", page {d['page']}" if d.get("page") else "")
                     + ")" + (f": {d['note']}" if d.get("note") else ""))
        if posts:
            state += f"; CANCEL post {posts[0].get('postId')} (posts_delete, then schedule.py --cancelled)"
        print(f"clip {r['id']}: {state}")


def main():
    ap = argparse.ArgumentParser(description="The client's approval page, and their reply recorded.")
    ap.add_argument("batch")
    ap.add_argument("--embed", action="store_true", help="put the clips inside the page (small batches only)")
    ap.add_argument("--clips-url", help="https link of a shared folder holding the clip files")
    ap.add_argument("--link", action="store_true", help=argparse.SUPPRESS)   # the default now
    ap.add_argument("--sent", action="store_true")
    ap.add_argument("--at")
    ap.add_argument("--apply", metavar="REPLY")
    ap.add_argument("--page", type=int)
    ap.add_argument("--received", help="when the client sent the reply (their email's time)")
    ap.add_argument("--again", action="store_true")
    ap.add_argument("--partial", action="store_true", help="record a reply that leaves some clips unanswered")
    ap.add_argument("--by")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--ledger")
    a = ap.parse_args()
    if a.apply:
        return apply_reply(a.batch, a.apply, a.by, a.ledger, a.page, a.received, a.again, a.partial)
    if a.sent:
        return mark_sent(a.batch, a.ledger, a.at)
    if a.status:
        return show(a.batch, a.ledger)
    build(a.batch, a.ledger, a.embed, a.clips_url)


if __name__ == "__main__":
    guard(main)
