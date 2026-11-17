#!/usr/bin/env python3
"""The monthly report for one client, from the ledger and saved WoopSocial analytics. Never estimates.

    python3 scripts/report.py <client-id> --month 2026-11 analytics.json [more.json ...]
        [--followers account-analytics.json ...] [--notes notes.md] [--allow-unknown]

analytics.json is the saved reply of social_account_posts_list_analytics for the client's project and
the month (save it as it came back; several files are fine, the newest numbers per post win).
--followers takes saved replies of social_accounts_get_analytics (one per account, the month's days):
the follower change is shown only when those replies carry follower numbers.

Statuses are refreshed from the saved analytics, never trusted from the ledger: a post the analytics
show (matched by its link, its postId, or its account and a delivery time within 30 minutes of the
time it was scheduled for) counts as live. A post whose time has passed and that the analytics don't
show has an unknown status: the report stops and asks for posts_get and schedule.py --status first
(or --allow-unknown, which lists them as unknown). A saved reply with posts on accounts that aren't
this client's is the wrong project's reply: the report refuses it.

Writes three files in clients/<id>/reports/:
- <month>.md and <month>.html: for the client. Clips delivered against the agreed number and why any
  are missing, approval turnaround (from the time the client replied, when it is known), views per
  platform with what a view means there and how many days each clip had been live, the follower change
  when WoopSocial returned it, and last month next to this one when last month's report exists.
  Platforms are never added together. A missing number is shown as missing, never guessed.
- <month>-agency.md: for the agency only. What to chase, internal ids, unknown statuses and gaps.
- <month>.json: this month's totals, read next month for the comparison.
"""
import argparse, calendar, datetime, html, os, statistics, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (LIMITS, VIEW_MEANS, accounts_of, client_dir, connected_id, die, guard, iso,  # noqa: E402
                       ledger_path, load_ledger, load_zone, now_utc, parse_time, plural, post_items, post_key,
                       read_client, read_json, rel, unwrap_reply, workspace_of, write_json, write_text)
from approve import page_rule, silence_due  # noqa: E402

VIEW_KEYS = ("views", "videoViews", "video_views", "plays")
FOLLOW_KEYS = ("followers", "followerCount", "followersCount", "subscribers", "subscriberCount", "subscribersCount")
MATCH_MINUTES = 30


def num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        try:
            return int(float(v.replace(",", "")))
        except ValueError:
            return None
    return None


def metrics_of(item):
    m = item.get("metrics") if isinstance(item.get("metrics"), dict) else {}
    views = next((num(m[k]) for k in VIEW_KEYS if k in m and num(m[k]) is not None), None)
    return {"views": views, "likes": num(m.get("likes")), "comments": num(m.get("comments")),
            "shares": num(m.get("shares"))}


def month_range(month, zone):
    try:
        y, mo = map(int, month.split("-"))
        datetime.date(y, mo, 1)
    except ValueError:
        die("--month is like 2026-11")
    tz = load_zone(zone) or datetime.timezone.utc
    a = datetime.datetime(y, mo, 1, tzinfo=tz)
    b = datetime.datetime(y + (mo == 12), mo % 12 + 1, 1, tzinfo=tz)
    prev = f"{y - (mo == 1)}-{(mo - 2) % 12 + 1:02d}"
    return a.astimezone(datetime.timezone.utc), b.astimezone(datetime.timezone.utc), \
        f"{calendar.month_name[mo]} {y}", prev


def fmt(n):
    if n is None:
        return "no number"
    return f"{n:,.1f}" if isinstance(n, float) and n != int(n) else f"{n:,.0f}"


def hours(h):
    return f"{h:.1f} hours" if h < 48 else f"{h / 24:.1f} days"


def label_of(p):
    return LIMITS.get(p, {}).get("label", p or "?")


def follower_series(files):
    """{socialAccountId or platform: [(day, followers)]} from saved social_accounts_get_analytics replies,
    read tolerantly: any list of dated entries carrying a follower or subscriber number."""
    out = {}

    def walk(x, owner, depth=0):
        if depth > 7:
            return
        if isinstance(x, dict):
            owner = x.get("socialAccountId") if isinstance(x.get("socialAccountId"), str) else owner
            day = next((x[k] for k in ("date", "day", "metricDate", "collectedAt") if isinstance(x.get(k), str)), None)
            n = next((num(x[k]) for k in FOLLOW_KEYS if k in x and num(x[k]) is not None), None)
            if n is None and isinstance(x.get("metrics"), dict):
                n = next((num(x["metrics"][k]) for k in FOLLOW_KEYS if num(x["metrics"].get(k)) is not None), None)
            if day and n is not None and owner:
                out.setdefault(owner, []).append((day[:10], n))
            for v in x.values():
                walk(v, owner, depth + 1)
        elif isinstance(x, list):
            for v in x:
                walk(v, owner, depth + 1)
    for f in files:
        data = read_json(f, "the saved account analytics reply")
        for _ in range(3):
            data = unwrap_reply(data)
        walk(data, None)
    return out


def gather(ws, cid, month, files, ledger, follow_files=(), allow_unknown=False):
    c = read_client(ws, cid)
    zone = c.get("timezone")
    a, b, label, prev = month_range(month, zone)
    now = now_utc()
    cdir = client_dir(ws, cid)
    mine = {connected_id(x) for x in accounts_of(c).values() if connected_id(x)}
    mine |= {sid for sid, o in ledger["accounts"].items() if o == cid}
    for r in c.get("revoked") or []:
        if isinstance(r, dict) and r.get("socialAccountId"):
            mine.add(r["socialAccountId"])
    posts = {k: dict(e) for k, e in ledger["posts"].items() if e.get("client") == cid}
    by_url = {post_key(e["url"]): k for k, e in posts.items() if e.get("url")}
    stats, foreign, unknown, seen_files = {}, [], [], 0
    for f in files:
        data = read_json(f, "the saved analytics reply")
        seen_files += 1
        for _ in range(3):
            data = unwrap_reply(data)
        for it in post_items(data):
            sid = it.get("socialAccountId")
            url = it.get("externalPostUrl") if isinstance(it.get("externalPostUrl"), str) else None
            done_t = parse_time(it.get("deliveryCompletedAt"))
            key = by_url.get(post_key(url)) if url else None
            if not key and isinstance(it.get("postId"), str) and f"{it['postId']}|{sid}" in posts:
                key = f"{it['postId']}|{sid}"
            has_pid = isinstance(it.get("postId"), str) and it["postId"].strip()
            if not key and done_t and sid and not has_pid:   # no postId: the account and the delivery time near the slot
                near = [k for k, e in posts.items() if k.endswith("|" + sid) and parse_time(e.get("scheduledFor"))
                        and e.get("status") not in ("cancelled", "failed")   # a cancelled slot is never "delivered"
                        and abs((done_t - parse_time(e["scheduledFor"])).total_seconds()) <= MATCH_MINUTES * 60]
                key = near[0] if len(near) == 1 else None
            if not key:
                if sid in mine:
                    unknown.append(url or sid)
                else:
                    foreign.append(sid or url or "?")
                continue
            when = parse_time(it.get("metricsCollectedAt"))
            old = stats.get(key)
            if not old or (when and (not old["collected"] or when >= old["collected"])):
                stats[key] = {"collected": when, **metrics_of(it)}
            if url and not posts[key].get("url"):
                posts[key]["url"] = url
            if done_t and not parse_time(posts[key].get("deliveryCompletedAt")):
                posts[key]["deliveryCompletedAt"] = iso(done_t)
            posts[key]["seen"] = True
    if foreign:
        die(f"{plural(len(foreign), 'post')} in the saved analytics {'is' if len(foreign) == 1 else 'are'} on accounts "
            f"that aren't {cid}'s ({', '.join(sorted(set(foreign))[:3])}). That is another project's reply: save "
            "social_account_posts_list_analytics again with this client's projectId")
    # refresh: what the analytics show is live; a past post they don't show is unknown
    live, unconfirmed = [], []
    for k, e in posts.items():
        t = parse_time(e.get("deliveryCompletedAt"))
        if e.get("seen") or e.get("status") == "published":
            if t and a <= t < b:
                live.append((k, e, t))
            elif not t and e.get("status") == "published":
                unconfirmed.append((k, e))
        elif e.get("status") in ("scheduled", "processing", "cancel_requested"):
            when = parse_time(e.get("scheduledFor"))
            if when and a <= when < min(b, now):
                unconfirmed.append((k, e))
    if unconfirmed and not allow_unknown:
        die(f"{plural(len(unconfirmed), 'post')} should have gone out by now but the saved analytics don't show "
            f"{'it' if len(unconfirmed) == 1 else 'them'}: " + ", ".join(sorted({k.split("|")[0] for k, _ in unconfirmed})[:5])
            + ". Run posts_get for each, save the reply, and schedule.py <batch> --status reply.json; then the report "
            "again. (--allow-unknown makes the report with them listed as unknown.)")
    later = [(k, e) for k, e in posts.items() if not e.get("seen") and e.get("status") in ("scheduled", "processing")
             and (parse_time(e.get("scheduledFor")) or now) >= max(now, a)]
    failed = [(k, e) for k, e in posts.items() if not e.get("seen") and e.get("status") == "failed"
              and a <= (parse_time(e.get("scheduledFor")) or a) < b]
    # clips, pages, decisions
    clipinfo, pages, skipped, pending_change, waiting = {}, [], 0, 0, 0
    edir = os.path.join(cdir, "episodes")
    for ep in sorted(os.listdir(edir)) if os.path.isdir(edir) else []:
        bp = os.path.join(edir, ep, "batch.json")
        if not os.path.isfile(bp):
            continue
        batch = read_json(bp, "the batch")
        title = (batch.get("episode") or {}).get("title") or ep
        for cl in batch.get("clips") or []:
            if isinstance(cl, dict) and cl.get("id") is not None:
                clipinfo[(ep, str(cl["id"]).zfill(2))] = {"hook": cl.get("hook") or cl.get("title") or "",
                                                         "episode": title}
        ap = os.path.join(edir, ep, "approvals.json")
        if not os.path.isfile(ap):
            continue
        appr = read_json(ap, "the approvals record")
        replies = appr.get("replies") or []
        decs = appr.get("decisions") or {}
        for d in decs.values():
            when = parse_time(d.get("received") or d.get("at"))
            if when and a <= when < b:
                skipped += d.get("decision") == "reject"
            pending_change += d.get("decision") == "revise"
        for pg in appr.get("pages") or []:
            sent = parse_time(pg.get("sent"))
            if not sent or not (a <= sent < b):
                continue
            mine_r = [r for r in replies if r.get("page") == pg.get("seq")]
            got = sorted(t for t in (parse_time(r.get("received")) for r in mine_r) if t and t >= sent)
            answers = {}
            for r in mine_r:
                answers.update(r.get("answers") or {})
            due = silence_due(pg)
            silent, unanswered = [], []
            for k, c_ in (pg.get("clips") or {}).items():
                dk = decs.get(k) or {}
                same = dk.get("hash") == c_.get("hash")
                if k in answers:
                    continue
                if same and dk.get("how") == "auto" and dk.get("page") == pg.get("seq"):
                    silent.append(k)
                elif same:
                    continue   # decided on an earlier page, unchanged since
                elif due and now >= due:
                    silent.append(k)
                else:
                    unanswered.append(k)
            waiting += len(unanswered)
            pages.append({"episode": ep, "title": title, "seq": pg.get("seq"), "sent": sent,
                          "reply": got[0] if got else None, "replied": bool(mine_r), "clips": len(pg.get("clips") or {}),
                          "approve": sum(v == "approve" for v in answers.values()), "auto": len(silent),
                          "revise": sum(v == "change" for v in answers.values()),
                          "reject": sum(v == "skip" for v in answers.values()), "open": len(unanswered),
                          "rule": page_rule(pg)["rule"]})
    # episodes expected
    qp = os.path.join(cdir, "queue.json")
    queue = read_json(qp, "the episode queue") if os.path.isfile(qp) else []
    eps_month = sum(1 for q in queue if isinstance(q, dict) and (lambda t: t and a <= t < b)(
        parse_time(q.get("published") or q.get("found"))))
    prev_path = os.path.join(cdir, "reports", f"{prev}.json")
    prev_data = read_json(prev_path, "last month's report data") if os.path.isfile(prev_path) else None
    return {"c": c, "cid": cid, "zone": zone, "label": label, "month": month, "prev": prev, "prev_data": prev_data,
            "a": a, "b": b, "now": now, "posts": posts, "stats": stats, "live": live, "later": later, "failed": failed,
            "unknown": unknown, "unconfirmed": unconfirmed, "clipinfo": clipinfo, "pages": pages, "files": seen_files,
            "skipped": skipped, "pending_change": pending_change, "waiting": waiting, "eps_month": eps_month,
            "followers": follower_series(follow_files), "follow_files": len(follow_files)}


def shortfall(d, n_live, agreed):
    """Why fewer clips went live than agreed, from what the files show."""
    why = []
    later = {(e.get("episode"), e.get("clip")) for _, e in d["later"]}
    if later:
        why.append(f"{plural(len(later), 'clip')} {'is' if len(later) == 1 else 'are'} approved and scheduled for later")
    if d["waiting"]:
        why.append(f"{plural(d['waiting'], 'clip')} {'waits' if d['waiting'] == 1 else 'wait'} for your reply")
    if d["pending_change"]:
        why.append(f"{plural(d['pending_change'], 'clip')} {'is' if d['pending_change'] == 1 else 'are'} being changed "
                   "as you asked")
    if d["skipped"]:
        why.append(f"you skipped {plural(d['skipped'], 'clip')}")
    if d["failed"]:
        why.append(f"{plural(len(d['failed']), 'post')} failed to publish (see below)")
    every = d["c"].get("expect_episode_every_days")
    if isinstance(every, (int, float)) and every > 0:
        days = (d["b"] - d["a"]).days or 30
        expected = max(1, int(days // every))
        if not d["eps_month"]:
            why.append("no new episode reached us this month")
        elif d["eps_month"] < expected:
            why.append(f"{plural(d['eps_month'], 'new episode')} reached us this month, where {expected} "
                       f"{'was' if expected == 1 else 'were'} expected (one every {every:g} days)")
    return why or ["we fell short this month; the reason isn't in our records, and we'll explain it separately"]


def build(d):
    c = d["c"]
    zone = load_zone(d["zone"]) or datetime.timezone.utc
    plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str) and p.upper() in LIMITS]
    accs = accounts_of(c)
    live = d["live"]
    clips_live = sorted({(e.get("episode"), e.get("clip")) for _, e, _ in live})
    agreed = c.get("agreed_clips_per_month")
    R = {"title": f"{c.get('name')}: {d['label']}", "example": c.get("example") is True, "sections": []}
    A = []    # agency notes
    data = {"month": d["month"], "clips_live": len(clips_live), "agreed": agreed, "platforms": {}}

    def sec(title, paras=None, table=None):
        R["sections"].append({"title": title, "paras": paras or [], "table": table})
    # delivery
    paras = []
    if isinstance(agreed, int):
        paras.append(f"{plural(len(clips_live), 'clip')} went live, against {agreed} agreed for the month"
                     + (" (on target)." if len(clips_live) >= agreed else "."))
        if len(clips_live) < agreed:
            paras.append("Why fewer: " + "; ".join(shortfall(d, len(clips_live), agreed)) + ".")
    else:
        paras.append(f"{plural(len(clips_live), 'clip')} went live.")
    per = {p: sum(1 for _, e, _ in live if e.get("platform") == p) for p in plats}
    paras.append("Posts: " + ", ".join(f"{label_of(p)} {per[p]}" for p in plats) + ".")
    later = {(e.get("episode"), e.get("clip")) for _, e in d["later"]}
    if later and not (isinstance(agreed, int) and len(clips_live) < agreed):
        paras.append(f"{plural(len(later), 'more clip')} {'is' if len(later) == 1 else 'are'} scheduled and not live "
                     "yet; they count in the month they go live.")
    if d["failed"]:
        paras.append(f"{plural(len(d['failed']), 'post')} failed to publish: " + "; ".join(
            f"\"{d['clipinfo'].get((e.get('episode'), e.get('clip')), {}).get('hook', 'a clip')}\" on "
            f"{label_of(e.get('platform'))}" for _, e in d["failed"]) + ". We post these again or explain why not.")
    pv = d["prev_data"]
    if pv:
        paras.append(f"Last month ({pv.get('label', d['prev'])}): {plural(pv.get('clips_live', 0), 'clip')} went live.")
    sec("Clips delivered", paras)
    # approval
    pg = d["pages"]
    if pg:
        turn = [(p["reply"] - p["sent"]).total_seconds() / 3600 for p in pg if p["reply"]]
        paras = [f"{plural(len(pg), 'approval page')} sent."]
        if turn:
            paras.append(f"You replied in {hours(statistics.median(turn))} at the median"
                         + (f", {hours(max(turn))} at the slowest." if len(turn) > 1 else "."))
        unk = sum(1 for p in pg if p["replied"] and not p["reply"])
        if unk:
            paras.append(f"For {plural(unk, 'page')} we didn't record when your reply arrived, so "
                         f"{'it is' if unk == 1 else 'they are'} left out of the reply time.")
            A.append(f"{plural(unk, 'page')} answered without the time the client's reply was sent: next time pass "
                     "approve.py --apply ... --received \"<the email's time>\".")
        auto = sum(p["auto"] for p in pg)
        if auto:
            paras.append(f"{plural(auto, 'clip')} went out with no reply by the deadline printed on the page, as agreed "
                         "in writing. Those weren't approved by you; tell us if any should come down.")
        rows = [[p["title"], p["sent"].astimezone(zone).strftime("%d %b"),
                 hours((p["reply"] - p["sent"]).total_seconds() / 3600) if p["reply"] else
                 ("time not recorded" if p["replied"] else "no reply"),
                 str(p["approve"]), str(p["auto"]), str(p["revise"]), str(p["reject"])] for p in pg]
        sec("Approval", paras, (["Episode", "Sent", "Reply after", "Approved", "No reply, posted as agreed",
                                 "Changes", "Skipped"], rows))
    else:
        sec("Approval", ["No approval page was sent this month."])
    # views
    gaps = []
    end = min(d["b"], d["now"])
    for p in plats:
        mine = [(k, e, t) for k, e, t in live if e.get("platform") == p]
        label = label_of(p)
        if not mine:
            if not connected_id(accs.get(p)):
                gaps.append(f"{label} isn't connected, so there are no {label} numbers here.")
                A.append(f"{label}: not connected; ask the client for a screenshot of the app's numbers if they want it.")
            sec(label, ["No posts this month."])
            continue
        withn = [(k, e, t, d["stats"][k]) for k, e, t in mine if k in d["stats"] and d["stats"][k]["views"] is not None]
        missing = [(k, e) for k, e, _ in mine if not (k in d["stats"] and d["stats"][k]["views"] is not None)]
        paras, table = [], None
        if withn:
            vs = [s["views"] for *_, s in withn]
            when = max((s["collected"] for *_, s in withn if s["collected"]), default=None)
            paras.append(f"{fmt(sum(vs))} views on {plural(len(withn), 'post')}. A view here is {VIEW_MEANS[p]}. "
                         + (f"Counted on {when.astimezone(zone).strftime('%d %b')}, from the day each clip went live."
                            if when else "The date the numbers were counted is unknown."))
            top = max(withn, key=lambda x: x[3]["views"])
            info = d["clipinfo"].get((top[1].get("episode"), top[1].get("clip")), {})
            line = f"Top clip: \"{info.get('hook', '')}\", {fmt(top[3]['views'])} views."
            med = statistics.median(vs) if len(vs) >= 3 else None
            if med is not None:
                line += f" Median clip: {fmt(med)} views."
            paras.append(line)
            pvp = ((pv or {}).get("platforms") or {}).get(p) or {}
            if pvp.get("median") is not None and med is not None:
                paras.append(f"Last month's median on {label}: {fmt(pvp['median'])} views.")
            rows = []
            for k, e, t, s in sorted(withn, key=lambda x: -x[3]["views"]):
                inf = d["clipinfo"].get((e.get("episode"), e.get("clip")), {})
                days = max(0, ((s["collected"] or end) - t).days)
                rows.append([inf.get("hook", ""), inf.get("episode", ""), str(days), fmt(s["views"]), fmt(s["likes"]),
                             fmt(s["comments"]), fmt(s["shares"]), e.get("url") or ""])
            table = (["Clip", "Episode", "Days live", "Views", "Likes", "Comments", "Shares", "Link"], rows)
            data["platforms"][p] = {"posts": len(withn), "views": sum(vs), "median": med}
        if missing:
            paras.append(f"{plural(len(missing), 'post')} {'has' if len(missing) == 1 else 'have'} no numbers yet and "
                         f"{'is' if len(missing) == 1 else 'are'} left out of the total, not guessed.")
            A.append(f"{label}: no numbers for post " + ", ".join(k.split("|")[0] for k, _ in missing)
                     + ". Numbers are collected about once a day: save the analytics again tomorrow; if one is still "
                     "missing, ask the client for the figure from the app.")
        sec(label, paras, table)
    # followers
    fl = []
    for p in plats:
        sid = connected_id(accs.get(p))
        series = sorted(x for x in d["followers"].get(sid, []) if d["month"] <= x[0][:7] <= d["month"]) if sid else []
        if len(series) >= 2:
            first, last = series[0], series[-1]
            fl.append(f"{label_of(p)}: {fmt(first[1])} on {first[0]} to {fmt(last[1])} on {last[0]} "
                      f"({last[1] - first[1]:+,d}).")
    if fl:
        sec("Followers", fl + ["As WoopSocial reported them for each account."])
    elif d["follow_files"]:
        A.append("The saved account analytics carry no follower numbers for this month, so the report has none. "
                 "TikTok returns followers only for TikTok for Business accounts.")
    else:
        A.append("No follower change in the report: save social_accounts_get_analytics per account and pass "
                 "--followers to show it.")
    if d["unknown"]:
        one = len(d["unknown"]) == 1
        gaps.append(f"{plural(len(d['unknown']), 'post')} on your accounts {'wasn' if one else 'weren'}'t made by us and "
                    f"{'isn' if one else 'aren'}'t in these numbers.")
        A.append("Not made through this skill: " + ", ".join(d["unknown"][:10]))
    if d["unconfirmed"]:
        gaps.append(f"For {plural(len(d['unconfirmed']), 'post')} we couldn't confirm yet whether it went live; "
                    "they aren't counted.")
        A.append("Status unknown (posts_get, then schedule.py --status): " + ", ".join(
            f"{k.split('|')[0]} ({e.get('platform')}, {e.get('episode')}/{e.get('clip')})" for k, e in d["unconfirmed"]))
    if not d["files"]:
        gaps.append("No view numbers were available for this report.")
        A.append("No analytics were passed: save social_account_posts_list_analytics for the project and month.")
    gaps.append("Views from different platforms count different things and are never added together.")
    sec("How to read this", gaps)
    data["label"] = d["label"]
    return R, A, data


def to_md(R, notes):
    L = [f"# {R['title']}", ""]
    if R["example"]:
        L += ["**EXAMPLE ONLY: a made-up client on NASA footage. Every account, link and number here is invented.**", ""]
    for s in R["sections"]:
        L += [f"## {s['title']}", ""] + [p + "\n" for p in s["paras"]]
        if s["table"]:
            head, rows = s["table"]
            L.append("| " + " | ".join(head) + " |")
            L.append("|" + "---|" * len(head))
            for r in rows:
                L.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
            L.append("")
    if notes:
        L += ["## From us", "", notes.strip(), ""]
    return "\n".join(L)


CSS = """:root{--bg:#f6f7f9;--card:#fff;--ink:#14171c;--mute:#5b6472;--line:#e3e6eb;--acc:#2457d6;--warn:#9a5b00}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a20;--ink:#e9ecf1;--mute:#a1a9b6;--line:#2a2f38;--acc:#7aa2ff;--warn:#f0b35a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}h1{font-size:26px;line-height:1.2;margin:0 0 16px}h2{font-size:18px;margin:0 0 8px}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:0 0 14px}p{margin:0 0 8px}
.example{border:1px solid var(--warn);border-radius:12px;padding:10px 14px;margin:0 0 14px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:7px 8px;border-top:1px solid var(--line);vertical-align:top}
th{color:var(--mute);font-weight:600;border-top:0}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}a{color:var(--acc)}
@media (max-width:640px){table,tbody,tr,td{display:block;width:100%}tr:first-child{display:none}tr{border-top:1px solid var(--line);padding:6px 0}
td,td.n{border:0;padding:2px 0;text-align:left;white-space:normal}td[data-h]::before{content:attr(data-h) ": ";color:var(--mute)}td.lead{font-weight:600}}"""


def to_html(R, notes):
    e = lambda s: html.escape(str(s), quote=True)  # noqa: E731
    out = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
           f"content=\"width=device-width,initial-scale=1\"><title>{e(R['title'])}</title><style>{CSS}</style></head>"
           f"<body><main><h1>{e(R['title'])}</h1>"]
    if R["example"]:
        out.append("<div class=\"example\"><strong>EXAMPLE ONLY.</strong> A made-up client on NASA footage. Every account, "
                   "link and number here is invented, and NASA endorses nothing.</div>")
    for s in R["sections"]:
        out.append(f"<section><h2>{e(s['title'])}</h2>" + "".join(f"<p>{e(p)}</p>" for p in s["paras"]))
        if s["table"]:
            head, rows = s["table"]
            numeric = {i for i, h in enumerate(head) if h in ("Views", "Likes", "Comments", "Shares", "Approved",
                                                                "Changes", "Skipped", "Days live",
                                                                "No reply, posted as agreed")}
            out.append("<table><tr>" + "".join(
                f"<th{' class=n' if i in numeric else ''}>{e(h)}</th>" for i, h in enumerate(head)) + "</tr>")
            for r in rows:
                cells = []
                for i, x in enumerate(r):
                    if head[i] == "Link":
                        cells.append(f"<td><a href=\"{e(x)}\">open the post</a></td>" if x else "<td></td>")
                    elif i == 0:
                        cells.append(f"<td class=\"lead\">{e(x)}</td>")
                    else:
                        cells.append(f"<td{' class=n' if i in numeric else ''} data-h=\"{e(head[i])}\">{e(x)}</td>")
                out.append("<tr>" + "".join(cells) + "</tr>")
            out.append("</table>")
        out.append("</section>")
    if notes:
        out.append("<section><h2>From us</h2>" + "".join(f"<p>{e(p)}</p>" for p in notes.strip().split("\n\n")) + "</section>")
    out.append("</main></body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="The monthly report for one client.")
    ap.add_argument("client")
    ap.add_argument("analytics", nargs="*", help="saved social_account_posts_list_analytics replies")
    ap.add_argument("--month", required=True)
    ap.add_argument("--followers", nargs="+", default=[], help="saved social_accounts_get_analytics replies")
    ap.add_argument("--notes")
    ap.add_argument("--allow-unknown", action="store_true")
    ap.add_argument("--workspace")
    ap.add_argument("--ledger")
    a = ap.parse_intermixed_args()
    ws = os.path.abspath(a.workspace) if a.workspace else (workspace_of(os.getcwd()) or os.getcwd())
    ledger = load_ledger(ledger_path(a.ledger))
    d = gather(ws, a.client, a.month, a.analytics, ledger, a.followers, a.allow_unknown)
    notes = None
    if a.notes:
        with open(a.notes, encoding="utf-8-sig") as fh:
            notes = fh.read()
    R, A, data = build(d)
    rdir = os.path.join(client_dir(ws, a.client), "reports")
    md, hp = os.path.join(rdir, f"{a.month}.md"), os.path.join(rdir, f"{a.month}.html")
    ag, js = os.path.join(rdir, f"{a.month}-agency.md"), os.path.join(rdir, f"{a.month}.json")
    write_text(md, to_md(R, notes))
    write_text(hp, to_html(R, notes))
    write_text(ag, "\n".join([f"# {R['title']}: agency notes (not for the client)", ""]
                             + [f"- {x}" for x in A] + ([""] if A else ["Nothing to chase.", ""])))
    write_json(js, data)
    print(to_md(R, notes))
    print("Agency notes:" + "".join(f"\n- {x}" for x in A) if A else "Agency notes: nothing to chase.")
    print(f"-> {rel(md)}, {rel(hp)} (for the client) and {rel(ag)} (agency only)")


if __name__ == "__main__":
    guard(main)
