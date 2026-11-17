#!/usr/bin/env python3
"""The campaign ledger: which post went into which campaign, a daily proof log, and what it may earn.

    python3 scripts/ledger.py --submitted <post url> --campaign <campaign id> [--submission-id ID]
                                                          # after pasting the link into the campaign
    python3 scripts/ledger.py --proof analytics.json      # the saved reply of
                                                          #   social_account_posts_list_analytics
    python3 scripts/ledger.py --earnings                  # views, estimated payout, days left
    python3 scripts/ledger.py --list                      # every post and submission

The ledger is one file for every campaign, whatever folder each campaign lives in:
~/.ai-clipping/ledger.json (AI_CLIPPING_HOME moves the folder, AI_CLIPPING_LEDGER or --ledger
names another file). plan.py adds every post that goes out; this script adds what happens after.
The proof log, proof.csv, sits next to the ledger and is one file for every campaign too (each row
names its campaign), so --proof and --earnings give the same answer from any folder.

Posts are matched by platform and post id, so the link from an app's share menu (with ?igsh=,
?si=, ?is_from_webapp=... or a youtu.be link) is the same post as the plain link.

--submitted records that the user pasted a post's link into a campaign. It refuses a link that was
already submitted (one post goes into one campaign, once), a post made for another campaign, a
TikTok short link (it hides the post id) and a time before the post went live. It never submits
anything itself: no marketplace has a submission API, and the skill never drives the user's
logged-in browser.

--proof appends one row per post and collection day to proof.csv: views, likes, comments, shares
and engagement as WoopSocial last collected them (about once a day), plus the submission id, and a
us_share column the user can fill from the app's audience countries. A daily snapshot for the
user's own records, never a replacement for the campaign's own tracker.

--earnings shows, per campaign: views, the estimated payout against the platform's minimum and cap
after the marketplace fee, and the days left in the counting window (from the day the clip crossed
the payout threshold, when the campaign counts that way). The campaign's own count decides what is
paid; Instagram "views" are times shown, which can differ from what the campaign counts.
"""
import argparse, csv, datetime, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cliplib import (place_name, LIMITS, SUBMIT_MINUTES, clock, die, guard, iso, ledger_path, load_ledger, money,  # noqa: E402
                     now_utc, parse_time, parse_user_time, payout, post_items, post_key, proof_path, read_json, rel,
                     save_ledger, short_link, terms, threshold_views, unwrap_reply, valid_id, with_defaults)

PROOF_COLUMNS = ["collected_at", "metrics_collected_at", "campaign", "post", "account", "platform", "url",
                 "views", "likes", "comments", "shares", "engagement", "published_at", "submission_id", "us_share"]
NEW_COLUMNS = ("submission_id", "us_share")
VIEW_KEYS = ("views", "videoViews", "video_views", "plays", "impressions")


def find_post(ledger, url):
    n = post_key(url)
    for k, e in ledger["posts"].items():
        if e.get("url") and post_key(e["url"]) == n:
            return k, e
    return None, None


def find_submission(ledger, url):
    n = post_key(url)
    return next((s for s in ledger["submissions"] if post_key(s.get("url")) == n), None)


def submitted(lpath, url, campaign, at=None, submission_id=None):
    if not url.lower().startswith(("http://", "https://")):
        die("give the post's link as the app shows it (https://...)")
    if short_link(url):
        die("that is a short share link (vm.tiktok.com or tiktok.com/t/), which hides the post's id. Open it in a "
            "browser and give the full link (tiktok.com/@<handle>/video/<number>)")
    if not valid_id(campaign):
        die("--campaign is the campaign id from campaign.json (lowercase letters, digits and dashes)")
    ledger = load_ledger(lpath)
    s = find_submission(ledger, url)
    if s:
        if s.get("campaign") == campaign:
            die(f"this post was already submitted to {campaign} on {s.get('submitted_at')}. A post is "
                "submitted once; submitting it again can get the account flagged")
        die(f"this post was already submitted to campaign {s.get('campaign')}. One post goes into one campaign, "
            "once, ever. For this campaign, make a new edit and post it fresh")
    key, post = find_post(ledger, url)
    if not post:
        waiting = unread_posts(ledger, url)
        if waiting:
            die(f"the skill posted {', '.join(waiting)} and hasn't read its link yet, so it can't tell whether this link "
                "is that post (and which campaign it was made for). Run plan.py --status with a fresh posts_get reply "
                "first, then record the submission")
    if post and post.get("campaign") and post["campaign"] != campaign:
        die(f"this post was made for campaign {post['campaign']}, not {campaign}: its caption, disclosure and "
            "on-screen items follow that brief. Submit it there, or make a new edit for this campaign")
    zone = (post or {}).get("timezone")
    assumed = None
    if at:
        t, assumed, problem = parse_user_time(at, zone)
        if problem:
            die(f"--at: {problem}")
    else:
        t = now_utc()
    late = None
    if post:
        live = parse_time(post.get("published_at")) or parse_time(post.get("recorded"))
        if live and parse_time(post.get("published_at")) and t < live - datetime.timedelta(minutes=1):
            die(f"--at {at} is before the post went live ({clock(live, zone)}). Give the time you submitted it")
        if live:
            mins = (t - live).total_seconds() / 60
            limit = post.get("submit_within") or (ledger.get("campaigns", {}).get(campaign) or {}).get(
                "submit_within_minutes") or SUBMIT_MINUTES
            if mins > limit:
                late = (int(mins), int(limit))
    entry = {"url": url, "campaign": campaign, "submitted_at": iso(t), "post": post.get("job_post") if post else None,
             "account": post.get("account") if post else None, "platform": post.get("platform") if post else None}
    if submission_id:
        entry["submission_id"] = str(submission_id).strip()
    if late:
        entry["late_minutes"] = late[0]
    ledger["submissions"].append(entry)
    save_ledger(lpath, ledger)
    who = f" ({post['account']})" if post else ""
    print(f"recorded: {url}{who} submitted to {campaign} at {clock(t, zone)}")
    if assumed:
        print(f"note: --at {at} has no time zone, so it was read as {assumed} time")
    if not post:
        print("note: this link isn't a post the skill recorded (made outside it, or not recorded yet). It is "
              "recorded anyway, so it can't be submitted twice")
    if late:
        print(f"warning: submitted {late[0]} minutes after it went live. This campaign only accepts posts submitted "
              f"within {late[1]} minutes; it may be rejected")
    print("next: keep it public and unchanged for the whole campaign window, and take the proof screenshots at the "
          "times submit.md lists. Run ledger.py --proof with the saved analytics reply once a day, and ledger.py "
          "--earnings to see where it stands")


def unread_posts(ledger, url):
    """Recent posts of the same platform (and, for TikTok, the same handle) that went out through the
    skill but whose link hasn't been read yet: this link may be one of them."""
    plat = post_key(url).split(":")[0]
    if plat not in LIMITS:
        return []
    m = re.search(r"tiktok\.com/@([A-Za-z0-9_.]+)", url)
    handle = m.group(1).casefold() if m else None
    now = now_utc()
    out = []
    for e in ledger["posts"].values():
        if e.get("url") or e.get("platform") != plat:
            continue
        if any(w in str(e.get("status") or "").upper() for w in ("FAIL", "ERROR", "REJECT")):
            continue
        t = parse_time(e.get("recorded"))
        if not t or (now - t).total_seconds() > 2 * 86400:
            continue
        if handle and e.get("handle") and str(e["handle"]).lstrip("@").casefold() != handle:
            continue
        out.append(f"{e.get('job_post')} on {e.get('account')} for {e.get('campaign')}")
    return out


def num(v):
    if isinstance(v, bool):
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        try:
            return int(float(v.replace(",", "")))
        except ValueError:
            return 0
    return 0


def metrics_of(item):
    m = item.get("metrics") if isinstance(item.get("metrics"), dict) else (
        item.get("analytics") if isinstance(item.get("analytics"), dict) else item)
    views = next((num(m[k]) for k in VIEW_KEYS if k in m), None)
    return views, num(m.get("likes")), num(m.get("comments")), num(m.get("shares"))


def read_proof(path):
    """The rows of proof.csv. A file from before the submission_id and us_share columns is read too."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:   # utf-8-sig: Excel saves with a BOM
        reader = csv.DictReader(fh)
        rows = list(reader)
        cols = reader.fieldnames or []
    if set(PROOF_COLUMNS) - set(cols) - set(NEW_COLUMNS):
        die(f"{rel(path)} doesn't have the columns this skill writes. Move it away and run --proof again")
    for r in rows:
        for k in NEW_COLUMNS:
            r.setdefault(k, "")
            if r[k] is None:
                r[k] = ""
    return rows


def write_proof(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PROOF_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    os.replace(tmp, path)


def proof(lpath, path):
    data = unwrap_reply(read_json(path, "the saved analytics reply"))
    items = post_items(data)
    if not items:
        die(f"{path} holds no posts. Save the whole reply of social_account_posts_list_analytics as it came back")
    ledger = load_ledger(lpath)
    ppath = proof_path(lpath)
    rows = read_proof(ppath)
    seen = {(post_key(r["url"]), r["metrics_collected_at"] or r["collected_at"][:10]) for r in rows}
    now = now_utc()
    new, skipped, no_views = [], 0, 0
    for it in items:
        url = it.get("externalPostUrl")
        if not isinstance(url, str) or not url.strip():
            skipped += 1
            continue
        _, post = find_post(ledger, url)
        sub = find_submission(ledger, url)
        if not post and not sub:
            skipped += 1
            continue
        views, likes, comments, shares = metrics_of(it)
        if views is None:
            no_views += 1
            continue
        mc = it.get("metricsCollectedAt") if isinstance(it.get("metricsCollectedAt"), str) else ""
        key = (post_key(url), mc or iso(now)[:10])
        if key in seen:
            continue
        seen.add(key)
        eng = (likes + comments + shares) / views if views else 0.0
        published = (post or {}).get("published_at") or (it.get("deliveryCompletedAt") if isinstance(
            it.get("deliveryCompletedAt"), str) else "")
        new.append({"collected_at": iso(now), "metrics_collected_at": mc,
                    "campaign": (post or {}).get("campaign") or (sub or {}).get("campaign") or "",
                    "post": (post or {}).get("job_post") or "", "account": (post or {}).get("account") or "",
                    "platform": (post or {}).get("platform") or it.get("platform") or "", "url": url,
                    "views": views, "likes": likes, "comments": comments, "shares": shares,
                    "engagement": f"{eng:.4f}", "published_at": published,
                    "submission_id": (sub or {}).get("submission_id") or "", "us_share": ""})
        if post and not post.get("published_at") and parse_time(it.get("deliveryCompletedAt")):
            post["published_at"] = iso(parse_time(it["deliveryCompletedAt"]))
    write_proof(ppath, rows + new)
    save_ledger(lpath, ledger)
    print(f"{len(new)} snapshot(s) added to {rel(ppath)}; {skipped} post(s) skipped (not in the ledger)"
          + (f"; {no_views} without a view count yet" if no_views else ""))
    print("note: WoopSocial collects these about once a day, so this is a daily snapshot. Instagram counts times "
          "shown. The campaign's own tracker decides what is paid. Keep the screenshots submit.md lists; you can type "
          "each post's audience share for the brief's country into the us_share column (0.42 for 42%)")


def load_campaigns(folder, files, ledger):
    """Campaign terms by id: the campaign files given (or campaign.json here), then the copies the
    ledger keeps of every campaign it recorded a post for."""
    out = {cid: with_defaults(c) for cid, c in (ledger.get("campaigns") or {}).items() if isinstance(c, dict)}
    paths = files or [p for p in ("campaign.json",) if os.path.isfile(os.path.join(folder, p))]
    for p in paths:
        full = p if os.path.isabs(p) or os.path.isfile(p) else os.path.join(folder, p)
        c = read_json(full, "a campaign file")
        if isinstance(c, dict) and isinstance(c.get("id"), str):
            out[c["id"]] = with_defaults(c)
    return out


def share(v):
    try:
        x = float(str(v).strip().rstrip("%"))
    except ValueError:
        return None
    return x / 100 if x > 1 else x


def earnings(folder, lpath, campaign_files):
    ledger = load_ledger(lpath)
    camps = load_campaigns(folder, campaign_files, ledger)
    rows = read_proof(proof_path(lpath))
    now = now_utc()
    by_camp = {}
    for k, e in ledger["posts"].items():
        by_camp.setdefault(e.get("campaign") or "(none)", []).append(e)
    for s in ledger["submissions"]:
        if not find_post(ledger, s["url"])[1]:
            by_camp.setdefault(s.get("campaign") or "(none)", []).append(
                {"url": s["url"], "account": s.get("account") or f"Not made here: {s['url']}",
                 "platform": s.get("platform") or (post_key(s["url"]).split(":")[0] if post_key(s["url"]).split(":")[0]
                                                   in LIMITS else None),
                 "job_post": "", "campaign": s.get("campaign")})
    if not by_camp:
        print("The ledger has no posts yet.")
        return
    low_eng = False
    for cid, posts in by_camp.items():
        c = camps.get(cid)
        known = c is not None
        c = c or with_defaults({})
        cur = c["currency"]
        window, fee = int(c["window_days"]), c["fee_pct"]
        print(f"\n{c.get('name') or cid} ({cid})" + ("" if known else ": campaign terms not found, so no rates. Pass "
                                                    "--campaign-file <its campaign.json>"))
        total_views, total_paid = 0, 0.0
        for e in posts:
            url = e.get("url")
            sub = find_submission(ledger, url) if url else None
            plat = e.get("platform")
            rate, mn, cap, mv = terms(c, plat)
            snaps = [r for r in rows if url and post_key(r["url"]) == post_key(url)]

            def when(r):
                return parse_time(r["metrics_collected_at"]) or parse_time(r["collected_at"])
            snaps.sort(key=lambda r: when(r) or now)
            live = parse_time(e.get("published_at")) or parse_time(e.get("recorded"))
            start, waiting = live, None
            if c.get("window_from") == "threshold":
                need = threshold_views(c, plat) if known else 0
                crossed = next((when(r) for r in snaps if num(r["views"]) >= need), None) if need else live
                start = crossed
                waiting = need if crossed is None else None
            end = start + datetime.timedelta(days=window) if start else None
            if end:
                inside = [r for r in snaps if (when(r) or now) <= end]
                snaps = inside or snaps[:0]
            last = snaps[-1] if snaps else None
            views = num(last["views"]) if last else 0
            gross, paid, why = payout(views, rate, mn, cap, fee, mv, cur)
            label = LIMITS.get(plat, {}).get("label", plat or "?")
            who = f"{e.get('account')}{' ' + e['handle'] if e.get('handle') else ''}"
            who += "" if e.get("account") == label or not plat else f" ({label})"
            if waiting:
                days = f"its {window}-day window starts when it reaches {waiting:,} views"
            elif end:
                left = (end - now).total_seconds() / 86400
                days = f"{left:.0f} day(s) left" if left > 0 else "window closed"
            else:
                days = "live time unknown"
            state = "submitted" if sub else "NOT SUBMITTED: earns nothing"
            line = f"  {who}: {views:,} views, est. {money(paid, cur)} after {fee:g}% fee"
            if why:
                line += f" ({why})"
            line += f", {days}, {state}"
            if not url:
                line += ", link not recorded yet"
            print(line)
            if last:
                eng = float(last["engagement"] or 0)
                if c.get("engagement_min") and views and eng < c["engagement_min"]:
                    low_eng = True
                    print(f"    engagement {eng:.1%} is under the campaign's {c['engagement_min']:.0%}; the clip can be "
                          "rejected")
                aud = c.get("audience") if isinstance(c.get("audience"), dict) else None
                us = share(last.get("us_share") or "")
                if aud and us is not None and aud.get("min_share") and us < aud["min_share"]:
                    print(f"    audience: {us:.0%} in {place_name(aud.get('geo'))} (from your screenshot); the campaign needs "
                          f"{aud['min_share']:.0%}, so expect this clip to be rejected")
                if plat == "INSTAGRAM":
                    print("    Instagram views are times shown (repeats included); the campaign may count differently")
            if sub:
                total_views += views
                total_paid += paid
        print(f"  submitted total: {total_views:,} views, est. {money(total_paid, cur)}")
        if c.get("budget_total"):
            print(f"  the campaign's total budget is {money(c['budget_total'], cur)}; when it runs out, views stop paying")
        if isinstance(c.get("audience"), dict):
            print(f"  audience rule: at least {c['audience']['min_share']:.0%} of viewers in {place_name(c['audience']['geo'])}. "
                  "WoopSocial doesn't report countries: read them in the app and keep the screenshots")
    if low_eng:
        print("\nLow engagement is fixed with better hooks and replies to comments, never with bought or arranged "
              "engagement: that is a permanent ban.")
    print("\nEstimates only. The campaign's own view count decides what is paid, and most clips earn little.")


def show(lpath):
    ledger = load_ledger(lpath)
    print(f"{len(ledger['posts'])} post(s), {len(ledger['submissions'])} submission(s) in {rel(lpath)}")
    for e in ledger["posts"].values():
        print(f"  {e.get('campaign')}: {e.get('job_post')} on {e.get('account')} {e.get('url') or '(no link yet)'}")
    for s in ledger["submissions"]:
        print(f"  submitted {s['url']} to {s['campaign']} at {s.get('submitted_at')}"
              + (f" (submission {s['submission_id']})" if s.get("submission_id") else ""))


def main():
    ap = argparse.ArgumentParser(description="Submissions, proof log and earnings for clipping campaigns.")
    ap.add_argument("--dir", default=".", help="with --earnings: the folder whose campaign.json to read (default: here)")
    ap.add_argument("--ledger", help="the ledger file (default: AI_CLIPPING_LEDGER, else ~/.ai-clipping/ledger.json)")
    ap.add_argument("--submitted", metavar="URL")
    ap.add_argument("--campaign", help="with --submitted: the campaign id")
    ap.add_argument("--submission-id", help="with --submitted: the id the campaign gave the submission, if any")
    ap.add_argument("--at", help="with --submitted: when (default now). Without a zone it is your computer's clock")
    ap.add_argument("--proof", metavar="ANALYTICS_JSON")
    ap.add_argument("--earnings", action="store_true")
    ap.add_argument("--campaign-file", action="append", default=[], help="a campaign.json (repeat for several)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        die(f"{a.dir} is not a folder")
    lpath = ledger_path(a.ledger)
    if a.submitted:
        if not a.campaign:
            die("--submitted needs --campaign <campaign id>")
        submitted(lpath, a.submitted, a.campaign, a.at, a.submission_id)
    elif a.proof:
        proof(lpath, a.proof)
    elif a.earnings:
        earnings(a.dir, lpath, a.campaign_file)
    elif a.list:
        show(lpath)
    else:
        die("say what to do: --submitted <url> --campaign <id>, --proof <analytics.json>, --earnings or --list")


if __name__ == "__main__":
    guard(main)
