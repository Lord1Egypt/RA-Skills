#!/usr/bin/env python3
"""Every client at a glance: what waits, and on whom.

    python3 scripts/status.py                 # every client in this folder
    python3 scripts/status.py <client-id>     # one client
    python3 scripts/status.py --json          # the same, for another tool

Per client: the episode queue (new episodes not started, an episode that is late against
expect_episode_every_days), and per episode batch where it stands: not cut, checks failing, page not
made or not sent, waiting for the client (and for how long), changes asked for, approved and not
scheduled, scheduled, live, failed. "Waits on" says who has to move: the agency, or the client. Reads
the files and the ledger only: it changes nothing and calls nothing.
"""
import argparse, json, os, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (client_dir, client_ids, clock, die, guard, ledger_path, load_ledger, now_utc,  # noqa: E402
                       parse_time, read_client, read_json, workspace_of)
from check_clips import check_batch  # noqa: E402
from approve import decisions, load_approvals, current_page  # noqa: E402


def hours_since(t, now):
    return (now - t).total_seconds() / 3600


def ago(h):
    return f"{h:.0f} h" if h < 48 else f"{h / 24:.0f} days"


def episode_state(batch_path, cid, ledger, lpath, now):
    """(lines, waits_on) for one episode batch."""
    try:
        m = check_batch(batch_path, lpath)
    except SystemExit as e:
        return [f"can't read: {str(e).replace('error: ', '')}"], "agency"
    rows = m["rows"]
    ep = m["episode"].get("id")
    if not rows:
        return ["no clips picked yet"], "agency"
    if not any(r.get("file") for r in rows):
        return ["picked, not cut (make_clips.py)"], "agency"
    errs = [i for i in m["issues"] if i[0] == "error"]
    appr = load_approvals(m)
    dec = decisions(m, appr, now)
    posts = {}
    for e in ledger["posts"].values():
        if e.get("client") == cid and e.get("episode") == ep:
            posts.setdefault(e.get("clip"), []).append(e)
    counts = {"published": 0, "scheduled": 0, "processing": 0, "failed": 0, "cancelled": 0}
    cancel = sorted({k.split("|")[0] for k, e in ledger["posts"].items() if e.get("client") == cid
                     and e.get("episode") == ep and e.get("status") == "cancel_requested"})
    for es in posts.values():
        for e in es:
            if e.get("status") in counts:
                counts[e["status"]] += 1
    lines, waits = [], set()
    late = sorted({e.get("postId") for e in ledger["posts"].values() if e.get("client") == cid and e.get("episode") == ep
                   and e.get("status") == "published" and e.get("live_after_cancel_request")})
    if late:
        lines.append(f"post {', '.join(late)} went live although the client said no: WoopSocial can't delete a live post; "
                     "tell the client and remove it in the app")
        waits.add("agency")
    if cancel:
        lines.append(f"cancel post {', '.join(cancel)} now (posts_delete, then schedule.py --cancelled): the client "
                     "said no after it was scheduled")
        waits.add("agency")
    planned = sorted((v.get("clip"), v.get("scheduledFor")) for v in ledger.get("planned", {}).values()
                     if v.get("client") == cid and v.get("episode") == ep)
    if planned:
        zone = m["client"].get("timezone")
        lines.append("requests written, not sent: " + ", ".join(
            f"clip {k} for {clock(parse_time(t), zone) if parse_time(t) else '?'}" for k, t in planned)
            + " (schedule.py --check each, then posts_create)")
        waits.add("agency")
    approved = [r["id"] for r in rows if (dec.get(r["id"]) or {}).get("decision") == "approve"]
    revise = [r["id"] for r in rows if (dec.get(r["id"]) or {}).get("decision") == "revise"]
    void = [r["id"] for r in rows if r["id"] in appr["decisions"] and r["id"] not in dec]
    undecided = [r["id"] for r in rows if r["id"] not in dec]
    pg = current_page(m, appr)
    if errs and not appr["pages"]:
        lines.append(f"{len(errs)} check error(s): check_clips.py")
        waits.add("agency")
    elif undecided:
        if not pg:
            lines.append("approval page not made for the clips as they are now (approve.py)")
            waits.add("agency")
        elif not pg.get("sent"):
            lines.append("approval page made, not sent (approve.py --sent once it is)")
            waits.add("agency")
        else:
            h = hours_since(parse_time(pg["sent"]), now)
            lines.append(f"waiting for the client on clip {', '.join(undecided)}: page sent {ago(h)} ago")
            waits.add("client")
    if void:
        lines.append(f"clip {', '.join(void)} changed after the client's decision: new page needed")
        waits.add("agency")
    if revise:
        lines.append(f"changes asked for on clip {', '.join(revise)}")
        waits.add("agency")
    todo = [k for k in approved if (k not in posts or all(e.get("status") == "failed" for e in posts[k]))
            and k not in {c for c, _ in planned}]
    if todo:
        lines.append(f"approved, not scheduled: clip {', '.join(todo)} (schedule.py)")
        waits.add("agency")
    bits = [f"{n} {k}" for k, n in counts.items() if n]
    if bits:
        lines.append(f"{len(posts)} clip(s) handed to WoopSocial, account posts: " + ", ".join(bits))
    if counts["failed"]:
        waits.add("agency")
    if not lines:
        lines.append("nothing waiting")
    return lines, ("agency" if "agency" in waits else "client" if "client" in waits else "nobody")


def client_state(ws, cid, ledger, lpath, now):
    c = read_client(ws, cid)
    out = {"client": cid, "name": c.get("name"), "status": c.get("status", "active"), "episodes": [], "notes": []}
    if out["status"] in ("offboarded",):
        out["waits_on"] = "nobody"
        return out
    zone = c.get("timezone")
    cdir = client_dir(ws, cid)
    qp = os.path.join(cdir, "queue.json")
    queue = read_json(qp, "the episode queue") if os.path.isfile(qp) else []
    new = [q for q in queue if isinstance(q, dict) and q.get("status") == "new"]
    if new:
        out["notes"].append(f"{len(new)} new episode(s) in the queue, not started: " + ", ".join(
            f"{q.get('id')} \"{q.get('title')}\"" for q in new[:3]))
    waits = {"agency"} if new else set()
    dates = [parse_time(q.get("published") or q.get("found")) for q in queue if isinstance(q, dict)]
    dates = [d for d in dates if d]
    every = c.get("expect_episode_every_days")
    if isinstance(every, (int, float)) and every > 0 and out["status"] == "active":
        if not dates:
            out["notes"].append("no episode yet: sources.py check, or ask the client for the first file")
            waits.add("client")
        else:
            last = max(dates)
            late = (now - last).days - every
            if late > 1:
                out["notes"].append(f"episode late: the last one is from {clock(last, zone)[:10]}, one is expected every "
                                    f"{every} days. Ask the client")
                waits.add("client")
    edir = os.path.join(cdir, "episodes")
    for ep in sorted(os.listdir(edir)) if os.path.isdir(edir) else []:
        bp = os.path.join(edir, ep, "batch.json")
        if os.path.isfile(bp):
            lines, w = episode_state(bp, cid, ledger, lpath, now)
            out["episodes"].append({"episode": ep, "state": lines, "waits_on": w})
            if w != "nobody":
                waits.add(w)
    if out["status"] == "offboarding":
        out["notes"].append("offboarding: client.py offboard " + cid)
        waits.add("agency")
    out["waits_on"] = "agency" if "agency" in waits else "client" if "client" in waits else "nobody"
    return out


def main():
    ap = argparse.ArgumentParser(description="What waits, and on whom, for every client.")
    ap.add_argument("client", nargs="?")
    ap.add_argument("--workspace")
    ap.add_argument("--ledger")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ws = os.path.abspath(a.workspace) if a.workspace else (workspace_of(os.getcwd()) or os.getcwd())
    ids = [a.client] if a.client else client_ids(ws)
    if not ids:
        die(f"no clients in {ws}/clients. Start with client.py new <client-id> --name \"Show\"")
    lpath = ledger_path(a.ledger)
    ledger = load_ledger(lpath)
    now = now_utc()
    states = [client_state(ws, cid, ledger, lpath, now) for cid in ids]
    if a.json:
        print(json.dumps(states, indent=2, ensure_ascii=False))
        return
    for s in states:
        print(f"{s['name']} ({s['client']}, {s['status']}): waits on {s['waits_on']}")
        for n in s["notes"]:
            print(f"  {n}")
        for e in s["episodes"]:
            print(f"  {e['episode']}: " + "; ".join(e["state"]))
    on_us = [s["client"] for s in states if s["waits_on"] == "agency"]
    on_them = [s["client"] for s in states if s["waits_on"] == "client"]
    print(f"\non the agency: {', '.join(on_us) or 'nothing'}. On clients: {', '.join(on_them) or 'nothing'}")


if __name__ == "__main__":
    guard(main)
