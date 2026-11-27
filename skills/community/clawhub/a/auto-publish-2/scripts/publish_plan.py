#!/usr/bin/env python3
"""Build, check and log a publishing plan for Synoclips (clips.synofex.com). Standard library only; Python 3.9+.

This script never posts anything. It turns finished clips plus posting slots into a plan that a person approves;
Claude then calls the Synoclips connector (schedule_clip / publish_clip_now) for each approved item.

Commands
  build  --clips CLIPS.json --accounts ID[,ID] (--calendar calendar.csv | --start YYYY-MM-DD --times 09:00,18:00)
         [--tz Asia/Karachi] [--per-day 2] [--platforms youtube,instagram,tiktok,facebook] [--min-score 0]
         [--max 10] [--min-gap-hours 4] [--blackout 2026-12-25,...] [--rules rules.json] [--out plan]
         -> plan.json + plan.md (one row per clip: accounts, time, title, hook, checks)
  check  PLAN.json [--rules rules.json] [--min-gap-hours 4]     re-check an edited plan
  log    PLAN.json --item N --status scheduled|posted|failed|cancelled [--post-id ID] [--note TEXT] [--log publish_log.csv]

CLIPS.json: the clips you chose, saved from the connector's list_clips / get_clip output. Either a list or
{"clips": [...]}; each clip needs video_id and clip_id; title, hook, description, hashtags, score are used if present.

Limits used (from the Synoclips connector): title 100 characters, hook 60, description 2,000, hashtags 30,
schedule up to 120 days ahead. Platform limits (for example a 100-character YouTube title) still apply on posting.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

LIMITS = {"title": 100, "hook": 60, "description": 2000, "hashtags": 30}
MAX_DAYS_AHEAD = 120
PLATFORMS = ("youtube", "instagram", "tiktok", "facebook")


class Fail(RuntimeError):
    pass


def tzinfo(name):
    if not ZoneInfo:
        raise Fail("Python's zoneinfo is missing; use Python 3.9+.")
    try:
        return ZoneInfo(name)
    except Exception:
        raise Fail(f"Unknown time zone '{name}'. Use an IANA name like Asia/Karachi (Windows: pip install tzdata).") from None


def load_clips(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        raise Fail(f"Cannot read clips file: {e}") from None
    clips = data.get("clips", data) if isinstance(data, dict) else data
    if not isinstance(clips, list) or not clips:
        raise Fail("The clips file has no clips.")
    out = []
    for i, c in enumerate(clips, 1):
        if not c.get("video_id") or not c.get("clip_id"):
            raise Fail(f"Clip {i} needs video_id and clip_id (copy them from list_clips).")
        tags = c.get("hashtags") or []
        if isinstance(tags, str):
            tags = [t for t in re.split(r"[\s,]+", tags) if t]
        out.append({"video_id": str(c["video_id"]), "clip_id": str(c["clip_id"]), "title": c.get("title") or "",
                    "hook": c.get("hook") or "", "description": c.get("description") or "", "hashtags": tags,
                    "score": c.get("score")})
    return out


def slots_from_calendar(path, platforms, tz_default):
    """Posting slots from social-media-calendar's calendar.csv (date, time, platform, timezone, status...)."""
    slots = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if (r.get("platform") or "").strip().lower() not in platforms:
                continue
            if (r.get("status") or "").strip().lower() in ("posted", "skipped", "scheduled"):
                continue
            d, t = (r.get("date") or "").strip(), (r.get("time") or "09:00").strip()
            try:
                when = dt.datetime.fromisoformat(f"{d}T{t}").replace(tzinfo=tzinfo(r.get("timezone") or tz_default))
            except ValueError:
                continue
            slots.append({"time": when, "source": f"calendar: {r.get('platform')} {r.get('title') or ''}".strip()})
    return sorted(slots, key=lambda s: s["time"])


def slots_from_rule(start, times, per_day, tz, count):
    zone = tzinfo(tz)
    try:
        day = dt.date.fromisoformat(start)
    except ValueError:
        raise Fail("--start must be YYYY-MM-DD.") from None
    hhmm = [t.strip() for t in times.split(",") if t.strip()][:max(1, per_day)]
    slots = []
    while len(slots) < count:
        for t in hhmm:
            h, m = (int(x) for x in t.split(":"))
            slots.append({"time": dt.datetime(day.year, day.month, day.day, h, m, tzinfo=zone), "source": "rule"})
        day += dt.timedelta(days=1)
    return slots[:count]


def check_plan(plan, rules=None, min_gap_hours=4, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    rules = rules or {}
    banned = [b.lower() for b in rules.get("banned", [])]
    blackout = set(plan.get("blackout", []))
    issues, seen = [], set()
    last_by_account = {}
    for n, it in enumerate(plan["items"], 1):
        def add(level, msg):
            issues.append({"item": n, "level": level, "text": msg})
        key = (it["video_id"], it["clip_id"])
        if key in seen:
            add("FAIL", "The same clip appears twice.")
        seen.add(key)
        if not it.get("account_ids"):
            add("FAIL", "No account ids (use list_accounts).")
        when = dt.datetime.fromisoformat(it["time"])
        if when <= now:
            add("FAIL", "Time is in the past.")
        if when > now + dt.timedelta(days=MAX_DAYS_AHEAD):
            add("FAIL", f"More than {MAX_DAYS_AHEAD} days ahead (Synoclips limit).")
        if when.date().isoformat() in blackout:
            add("FAIL", f"{when.date()} is a blackout date.")
        for field in ("title", "hook", "description"):
            v = it.get(field) or ""
            if len(v) > LIMITS[field]:
                add("FAIL", f"{field} is {len(v)} characters (limit {LIMITS[field]}).")
        if not it.get("title"):
            add("WARN", "Empty title: the platform post will use a default; set one with rename_or_retitle_clip.")
        if len(it.get("hashtags") or []) > LIMITS["hashtags"]:
            add("FAIL", f"{len(it['hashtags'])} hashtags (limit {LIMITS['hashtags']}).")
        text = " ".join([it.get("title", ""), it.get("hook", ""), it.get("description", "")]).lower()
        for b in banned:
            if re.search(rf"(?<!\w){re.escape(b)}(?!\w)", text):
                add("FAIL", f"Banned by the brand rules: '{b}'.")
        if it.get("score") is not None and it["score"] < plan.get("min_score", 0):
            add("WARN", f"Score {it['score']} is below the plan's minimum {plan.get('min_score')}.")
    # spacing per account, in time order (an edited plan may not be sorted)
    order = sorted(range(len(plan["items"])), key=lambda k: plan["items"][k]["time"])
    for k in order:
        it = plan["items"][k]
        when = dt.datetime.fromisoformat(it["time"])
        for acc in it.get("account_ids", []):
            prev = last_by_account.get(acc)
            if prev and (when - prev) < dt.timedelta(hours=min_gap_hours):
                issues.append({"item": k + 1, "level": "WARN",
                               "text": f"Less than {min_gap_hours:g} h after the previous post on {acc}."})
            last_by_account[acc] = when
    return sorted(issues, key=lambda i: i["item"])


def write_outputs(plan, issues, base):
    base = Path(base)
    base.parent.mkdir(parents=True, exist_ok=True)
    plan = dict(plan, issues=issues)
    base.with_suffix(".json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    L = [f"# Publishing plan ({len(plan['items'])} posts)", "",
         "Nothing has been posted. Approve this list (or edit plan.json and run `check`), then each item is "
         "scheduled with the Synoclips connector.", "",
         "| # | When | Accounts | Clip | Title | Hook | Score | Checks |", "|---|---|---|---|---|---|---|---|"]
    by_item = {}
    for i in issues:
        by_item.setdefault(i["item"], []).append(f"{i['level']}: {i['text']}")
    for n, it in enumerate(plan["items"], 1):
        chk = "<br>".join(by_item.get(n, [])) or "OK"
        L.append(f"| {n} | {it['time']} | {', '.join(it['account_ids'])} | {it['video_id']}/{it['clip_id']} | "
                 f"{it.get('title', '')[:60]} | {it.get('hook', '')} | {it.get('score') if it.get('score') is not None else '-'} | {chk} |")
    base.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return base.with_suffix(".json"), base.with_suffix(".md")


def report(issues):
    fails = sum(1 for i in issues if i["level"] == "FAIL")
    warns = sum(1 for i in issues if i["level"] == "WARN")
    for i in issues:
        print(f"[{i['level']}] item {i['item']}: {i['text']}")
    print(f"{fails} fail, {warns} warn. Fix every FAIL before asking for approval.")
    return 1 if fails else 0


def load_rules(path):
    if not path:
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Fail(f"Cannot read rules file: {e}") from None


def cmd_build(a):
    clips = load_clips(a.clips)
    if a.min_score:
        clips = [c for c in clips if c["score"] is None or c["score"] >= a.min_score]
    clips = clips[:a.max]
    if not clips:
        raise Fail("No clips left after --min-score / --max.")
    platforms = tuple(p.strip().lower() for p in a.platforms.split(",") if p.strip())
    if a.calendar:
        slots = slots_from_calendar(a.calendar, platforms, a.tz)
        now = dt.datetime.now(dt.timezone.utc)
        slots = [s for s in slots if s["time"] > now]
        if len(slots) < len(clips):
            print(f"[NOTE] The calendar has {len(slots)} future slot(s) for {', '.join(platforms)}; "
                  f"{len(clips) - len(slots)} clip(s) are left out. Add slots or use --start/--times.")
    elif a.start:
        slots = slots_from_rule(a.start, a.times, a.per_day, a.tz, len(clips))
    else:
        raise Fail("Give --calendar calendar.csv (from social-media-calendar) or --start and --times.")
    accounts = [x.strip() for x in a.accounts.split(",") if x.strip()]
    items = []
    for c, s in zip(clips, slots):
        items.append(dict(c, account_ids=accounts, time=s["time"].isoformat(), slot=s["source"]))
    plan = {"created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "min_score": a.min_score,
            "blackout": [d.strip() for d in (a.blackout or "").split(",") if d.strip()], "items": items}
    issues = check_plan(plan, load_rules(a.rules), a.min_gap_hours)
    j, m = write_outputs(plan, issues, a.out)
    print(f"Wrote {j} and {m} ({len(items)} posts).")
    return report(issues)


def cmd_check(a):
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    issues = check_plan(plan, load_rules(a.rules), a.min_gap_hours)
    base = Path(a.plan).with_suffix("")
    write_outputs(plan, issues, base)
    print(f"Re-checked {a.plan}; updated {base.with_suffix('.md')}.")
    return report(issues)


def cmd_log(a):
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    if not 1 <= a.item <= len(plan["items"]):
        raise Fail(f"--item must be 1 to {len(plan['items'])}.")
    it = plan["items"][a.item - 1]
    log = Path(a.log)
    new = not log.exists()
    with open(log, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["logged_at", "item", "video_id", "clip_id", "accounts", "time", "title", "status", "post_id", "note"])
        w.writerow([dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), a.item, it["video_id"], it["clip_id"],
                    " ".join(it["account_ids"]), it["time"], it.get("title", ""), a.status, a.post_id or "", a.note or ""])
    print(f"Logged item {a.item} as {a.status} in {log}.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--clips", required=True)
    b.add_argument("--accounts", required=True, help="account ids from list_accounts, comma-separated")
    b.add_argument("--calendar", help="calendar.csv exported by social-media-calendar")
    b.add_argument("--start", help="first day, YYYY-MM-DD (when not using --calendar)")
    b.add_argument("--times", default="09:00,18:00", help="posting times per day, HH:MM, comma-separated")
    b.add_argument("--per-day", type=int, default=2)
    b.add_argument("--tz", default="Asia/Karachi")
    b.add_argument("--platforms", default=",".join(PLATFORMS), help="calendar rows to use")
    b.add_argument("--min-score", type=int, default=0)
    b.add_argument("--max", type=int, default=10)
    b.add_argument("--min-gap-hours", type=float, default=4)
    b.add_argument("--blackout", help="dates to avoid, YYYY-MM-DD, comma-separated")
    b.add_argument("--rules", help="brand-voice rules.json (banned words are checked)")
    b.add_argument("--out", default="plan")
    b.set_defaults(fn=cmd_build)
    c = sub.add_parser("check")
    c.add_argument("plan")
    c.add_argument("--rules")
    c.add_argument("--min-gap-hours", type=float, default=4)
    c.set_defaults(fn=cmd_check)
    lg = sub.add_parser("log")
    lg.add_argument("plan")
    lg.add_argument("--item", type=int, required=True)
    lg.add_argument("--status", required=True, choices=["scheduled", "posted", "failed", "cancelled"])
    lg.add_argument("--post-id")
    lg.add_argument("--note")
    lg.add_argument("--log", default="publish_log.csv")
    lg.set_defaults(fn=cmd_log)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
