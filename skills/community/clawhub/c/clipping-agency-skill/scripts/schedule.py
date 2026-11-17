#!/usr/bin/env python3
"""Schedule the clips the client approved, on the client's own accounts, at the client's times.

    python3 scripts/schedule.py <batch.json>                      # what goes out when; the files to upload
    python3 scripts/schedule.py <batch.json> --media media.json   # with the uploads: one request per clip
    python3 scripts/schedule.py <batch.json> --check requests/clip-01.json
                                                                  # right before posts_validate: may it go?
    python3 scripts/schedule.py <batch.json> --posted requests/clip-01.json <postId>
                                                                  # right after posts_create: record it
    python3 scripts/schedule.py <batch.json> --cancelled <postId>  # after posts_delete: record it
    python3 scripts/schedule.py <batch.json> --status status.json [<postId>]
                                                                  # the saved posts_get reply: live, links

Only clips with a recorded approval for exactly the file and captions on the page go in: a clip cut again
or a caption edited after the client said yes waits for a new page. Each approved clip becomes one
WoopSocial post with a child for each of the client's connected accounts (its own caption per platform),
scheduled for later at the next free time of the client's cadence, in the client's time zone, never
closer than min_gap_hours to another of the client's posts and under TikTok's daily cap per account.
Every account comes from this client's file. --check (run it right before sending each request) and
--posted refuse a request that names an account another client's file or the ledger gives to someone
else, a request edited after it was written, a clip whose approval no longer matches, a client who
isn't active, a clip with a check error, and (--check) a post time less than 30 minutes away. The slots
of requests written but not sent yet are kept in the ledger, so two episodes never get the same slots;
any run that changes what was approved (a reply, a new page, a re-cut, offboarding) removes them.

Files, next to batch.json: schedule.md (every post, its time in the client's zone, the files to upload,
what is done by hand), requests/clip-NN.json (only with --media; each one is sent with posts_validate,
then posts_create, exactly as written) and requests/index.json (what each request was written from).
"""
import argparse, hashlib, json, os, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datetime  # noqa: E402
from agencylib import (LIMITS, MIN_SEND_MINUTES, TIKTOK_PRIVACY, account_owner, accounts_of, clear_requests,  # noqa: E402
                       client_busy, clock, connected_id, die, guard, iso, now_utc, parse_time, plan_slots, plural,
                       post_items, postable_id, read_json, rel, save_ledger, sha256, unwrap_reply, write_json,
                       write_text)
from check_clips import check_batch  # noqa: E402
from approve import decisions, load_approvals, approvals_path  # noqa: E402

MARK = "<!-- written by schedule.py; it replaces this file on every run -->"
STATUS = {"NOT_STARTED": "scheduled", "SENDING": "processing", "PUBLISHED": "published", "FAILED": "failed"}


def body_sha(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def posted_clips(ledger, cid, episode):
    """{clip id: [ledger entries]} of this episode's posts that are scheduled, processing or live."""
    out = {}
    for k, e in ledger["posts"].items():
        if e.get("client") == cid and e.get("episode") == episode and e.get("status") not in ("cancelled", "failed"):
            out.setdefault(e.get("clip"), []).append(e)
    return out


def child(p, acc, clip, row, c, tiktok, media_id):
    caps = {k.upper(): v for k, v in (clip.get("captions") or {}).items()}
    t = {"platform": p, "socialAccountId": postable_id(acc)}
    if p == "TIKTOK":
        # The client chose who sees the posts and what people may do on the approval page; nothing is defaulted.
        # A clip with a sponsor segment carries TikTok's paid partnership label, one that promotes the client's
        # own business the "Your brand" label. autoAddMusic is required by WoopSocial's schema: always false.
        t.update(postType="VIDEO", postMode="DIRECT_POST", privacyLevel=tiktok["privacyLevel"],
                 allowComment=tiktok["allowComment"], allowDuet=tiktok["allowDuet"], allowStitch=tiktok["allowStitch"],
                 isYourBrand=clip.get("promotes_client_business") is True, isBrandedContent=bool(row.get("sponsor")),
                 autoAddMusic=False)
    elif p == "INSTAGRAM":
        t.update(postType="REEL")
    elif p == "YOUTUBE":
        yt = c.get("youtube") or {}
        t.update(title=clip.get("title"), privacy=yt.get("privacy"), madeForKids=yt.get("madeForKids") is True)
        if clip.get("tags"):
            t["tags"] = clip["tags"]
    t["contentOverride"] = [{"text": caps.get(p, ""), "media": [{"type": "MEDIA_LIBRARY", "mediaId": media_id}]}]
    return t


def load_media(arg, bdir, files):
    """media.json: {"clips/clip-01.mp4": {"mediaId": "...", "sha256": "<the fingerprint schedule.md lists>"}}."""
    path = arg if os.path.isfile(arg) else os.path.join(bdir, arg)
    media = read_json(path, "the uploaded media ids")
    form = "{\"clips/clip-01.mp4\": {\"mediaId\": \"<mediaId>\", \"sha256\": \"<its fingerprint>\"}}"
    if not isinstance(media, dict):
        die(f"{arg} must be {form}")
    for k, v in media.items():
        if not isinstance(v, dict) or not isinstance(v.get("mediaId"), str) or not v["mediaId"].strip():
            die(f"{arg} must be {form}; {k} has no mediaId")
        if not isinstance(v.get("sha256"), str) or len(v["sha256"].strip()) < 12:
            die(f"{arg}: {k} needs \"sha256\", the fingerprint schedule.md lists for it (12 characters or more)")
    missing = [f for f in files if f not in media]
    if missing:
        die(f"{arg} has no mediaId for {', '.join(missing)}. Upload each file under \"Files to upload\" once, add its "
            "mediaId, and run this again")
    for f in files:
        if not files[f].startswith(media[f]["sha256"].strip().lower()):
            die(f"{f} changed after it was uploaded (its fingerprint isn't the uploaded one). It needs the client's "
                "approval again before anything is uploaded or posted")
    up = os.path.join(bdir, "uploaded.json")
    if os.path.isfile(up):   # upload_parts.py records the fingerprint of the bytes it really sent
        sent = read_json(up, "the upload record")
        for f in files:
            rec = sent.get(os.path.basename(f)) if isinstance(sent, dict) else None
            if isinstance(rec, dict) and rec.get("sha256") and rec["sha256"] != files[f]:
                die(f"{f}: the bytes upload_parts.py sent ({rec['sha256'][:16]}) aren't this file. Upload it again")
    return media


def plan(batch_path, media_arg=None, ledger_file=None):
    m = check_batch(batch_path, ledger_file)
    c, cid, bdir, ep = m["client"], m["cid"], m["bdir"], m["episode"]
    zone = c.get("timezone")
    client_errs = [i for i in m["issues"] if i[0] == "error" and i[1] in ("client.json", "episode.id",
                                                                          "episode.guest_release", "episode.music",
                                                                          "episode.sponsor_segments")]
    if client_errs:
        die("; ".join(f"{w}: {msg}" for _, w, msg in client_errs))
    appr = load_approvals(m)
    now = now_utc()
    dec = decisions(m, appr, now)
    ledger = m["ledger"]
    done = posted_clips(ledger, cid, ep.get("id"))
    accs = accounts_of(c)
    connected = [p for p in m["plats"] if postable_id(accs.get(p))]
    by_hand = [p for p in m["plats"] if p not in connected]
    relink = [p for p in m["plats"] if connected_id(accs.get(p)) and not postable_id(accs.get(p))]
    tiktok = appr.get("tiktok")
    go, waiting, blocked = [], [], []
    for r in m["rows"]:
        d = dec.get(r["id"])
        if r["id"] in done:
            continue
        if not d:
            prior = appr["decisions"].get(r["id"])
            waiting.append((r, "changed after the client approved it: needs a new page" if prior and
                            prior.get("decision") == "approve" else "waiting for the client"))
            continue
        if d["decision"] != "approve":
            waiting.append((r, "the client asked for a change" if d["decision"] == "revise" else "the client skipped it"))
            continue
        errs = [msg for lv, msg in r["issues"] if lv == "error"]
        if errs:
            blocked.append((r, errs))
            continue
        go.append((r, d))
    # the auto rule: record what silence approved, so posting always rests on a recorded approval
    changed = False
    for r, d in go:
        if d.get("how") == "auto" and appr["decisions"].get(r["id"], {}).get("hash") != d["hash"]:
            appr["decisions"][r["id"]] = dict(d)
            changed = True
    if changed:
        write_json(approvals_path(m), appr)
    tt_plat = "TIKTOK" in connected
    tt_note = None
    if tt_plat and go:
        if not tiktok:
            tt_note = ("TikTok waits: the client hasn't chosen who can see the posts and whether people may comment, duet "
                       "or stitch (the TikTok line of their reply). Ask them; nothing is chosen for them")
        else:
            opts = (accs["TIKTOK"].get("privacyOptions") or list(TIKTOK_PRIVACY))
            if tiktok["privacyLevel"] not in opts:
                tt_note = (f"TikTok waits: the client chose {tiktok['privacyLevel']}, which this account doesn't offer now "
                           f"({', '.join(opts)}). Ask them again")
    tt_id = connected_id(accs.get("TIKTOK"))
    busy, tt_busy = client_busy(ledger, cid, tt_id, exclude_episode=ep.get("id"))
    nb = parse_time(ep.get("published")) if ep.get("not_before_published", True) else None
    slots = plan_slots(c, len(go), busy, tt_busy, now=now, not_before=nb)
    if len(slots) < len(go):
        die(f"only {len(slots)} free posting times in the next 180 days for {len(go)} clips: check cadence in client.json")
    files = {}
    posts = []
    for (r, d), when in zip(go, slots):
        plats = [p for p in connected if not (p == "TIKTOK" and tt_note)]
        if r.get("sponsor") and tiktok and tiktok.get("privacyLevel") == "SELF_ONLY":
            plats = [p for p in plats if p != "TIKTOK"]
        try:
            relf = os.path.relpath(r["file"], bdir).replace(os.sep, "/")
        except ValueError:   # another drive on Windows
            relf = os.path.abspath(r["file"]).replace(os.sep, "/")
        files[relf] = r["sha256"]
        posts.append({"row": r, "decision": d, "when": when, "plats": plats, "file": relf})
    media = load_media(media_arg, bdir, files) if media_arg and posts else None
    clear_requests(bdir, ledger, cid, ep.get("id"))
    rdir = os.path.join(bdir, "requests")
    index = {"client": cid, "episode": ep.get("id"), "written": iso(now), "requests": {}}
    for p in posts:
        r = p["row"]
        if not media or not p["plats"]:
            continue
        mid = media[p["file"]]["mediaId"]
        kids = [child(pl, accs[pl], r["clip"], r, c, tiktok, mid) for pl in p["plats"]]
        body = {"content": [dict(kids[0]["contentOverride"][0])],
                "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": iso(p["when"])}, "socialAccounts": kids}
        name = f"clip-{r['id']}.json"
        write_json(os.path.join(rdir, name), body)
        index["requests"][name] = {"clip": r["id"], "hash": r["hash"], "sha256": r["sha256"], "body_sha256": body_sha(body),
                                   "scheduledFor": iso(p["when"]), "accounts": {k["socialAccountId"]: k["platform"]
                                                                                for k in kids}}
        ledger["planned"][f"{cid}|{ep.get('id')}|{r['id']}"] = {
            "client": cid, "episode": ep.get("id"), "clip": r["id"], "scheduledFor": iso(p["when"]),
            "sha256": r["sha256"], "accounts": [k["socialAccountId"] for k in kids], "written": iso(now)}
    if index["requests"]:
        write_json(os.path.join(rdir, "index.json"), index)
    save_ledger(m["lpath"], ledger)
    # schedule.md
    L = [MARK, f"# Schedule: {c.get('name')}, {ep.get('title') or ep.get('id')}", ""]
    if c.get("example") is True:
        L += ["**EXAMPLE ONLY: a made-up client on NASA footage. The accounts, ids and times are invented; nothing here "
              "was posted.**", ""]
    L += [f"Times are the client's ({zone}). Accounts: " + (", ".join(f"{LIMITS[p]['label']} {accs[p].get('handle') or ''}"
                                                                       .strip() for p in connected) or "none connected"), ""]
    if posts:
        L += ["| Clip | Goes out | Where | Approved |", "|---|---|---|---|"]
        for p in posts:
            d = p["decision"]
            L.append(f"| {p['row']['id']} | {clock(p['when'], zone)} | "
                     + (", ".join(LIMITS[x]["label"] for x in p["plats"]) or "by hand only")
                     + f" | {d.get('by')} ({d.get('how')}, {d.get('at', '')[:10]}) |")
        L.append("")
    else:
        L += ["Nothing to schedule: no approved clip that isn't scheduled already.", ""]
    for k, es in sorted(done.items()):
        e = es[0]
        t = parse_time(e.get("scheduledFor"))
        if e.get("status") == "cancel_requested":
            L.append(f"- clip {k}: **CANCEL post `{e.get('postId')}` now** ({e.get('cancel_reason')}): `posts_delete`, then "
                     f"`schedule.py <batch> --cancelled {e.get('postId')}`" + (f". It goes out {clock(t, zone)}" if t else ""))
        else:
            L.append(f"- clip {k}: {e.get('status')} as post `{e.get('postId')}`" + (f", {clock(t, zone)}" if t else ""))
    if done:
        L.append("")
    if waiting:
        L += ["## Not scheduled", ""] + [f"- clip {r['id']}: {why}" for r, why in waiting] + [""]
    if blocked:
        L += ["## Blocked by a check", ""] + [f"- clip {r['id']}: {'; '.join(e)}" for r, e in blocked] + [""]
    if tt_note:
        L += [tt_note + ".", ""]
    sponsored = [p for p in posts if p["row"].get("sponsor")]
    if posts:
        L += ["## Files to upload", "", "Once each, before the requests are written: `media_uploads_create_session` with the "
              f"client's projectId ({(c.get('woopsocial') or {}).get('projectId')}) and the byte size, "
              "`upload_parts.py session.json <file>`, `media_uploads_complete_session`. Then save media.json as "
              "`{\"<file>\": {\"mediaId\": \"...\", \"sha256\": \"<fingerprint>\"}}` and run `schedule.py <batch> --media "
              "media.json`.", ""]
        for f, s in files.items():
            L.append(f"- `{f}` ({os.path.getsize(os.path.join(bdir, f))} bytes), fingerprint `{s[:16]}`")
        L.append("")
    if index["requests"]:
        L += ["## Send", "", "For each request, in this order, one at a time: `schedule.py <batch> --check requests/<name>` "
              "(never send a request it refuses), `posts_validate` with the body exactly as written, `posts_create`, then at "
              "once `schedule.py <batch> --posted requests/<name> <postId>`.", ""]
        L += [f"- `requests/{n}`: clip {v['clip']}, {clock(parse_time(v['scheduledFor']), zone)}"
              for n, v in index["requests"].items()] + [""]
    if by_hand and posts:
        L += ["## By hand", "", "Not connected through WoopSocial: " + ", ".join(LIMITS[p]["label"] for p in by_hand)
              + ". Post the same file and that platform's caption from the approval page at the time above, from the "
              "client's account, or ask the client to connect it (client.py connect)."
              + (" Connected but needing a new link: " + ", ".join(LIMITS[p]["label"] for p in relink) + "." if relink else ""),
              ""]
    if posts and "YOUTUBE" in connected:
        L += ["## Optional, after each Short is live", "", "In YouTube Studio, link the full episode as the Short's related "
              "video, if the client wants viewers sent to it (a step in the app).", ""]
    if sponsored:
        L += ["## After each sponsored clip is live (in the apps; WoopSocial can't set these)", ""]
        for p in sponsored:
            L.append(f"- clip {p['row']['id']} ({p['row']['sponsor']}): Instagram, turn on the paid partnership label "
                     "(edit the Reel, add the label and the sponsor). YouTube, tick \"includes paid promotion\" in YouTube "
                     "Studio. TikTok's label goes on with the post.")
        L.append("")
    out = os.path.join(bdir, "schedule.md")
    write_text(out, "\n".join(L))
    print("\n".join(L[1:]))
    print(f"-> {rel(out)}" + (f", {len(index['requests'])} request(s) in {rel(rdir)}" if index["requests"] else ""))


def verify(m, request, sending=False):
    """Every check a request must pass to be sent (sending=True) or recorded: (meta, body, decision, row)."""
    c, cid, bdir = m["client"], m["cid"], m["bdir"]
    rdir = os.path.join(bdir, "requests")
    rpath = request if os.path.isfile(request) else os.path.join(bdir, request)
    name = os.path.basename(rpath)
    idx_path = os.path.join(rdir, "index.json")
    if not os.path.isfile(idx_path) or not os.path.isfile(rpath):
        die(f"{request} isn't a request schedule.py wrote for this episode as it is now (requests are removed when a "
            "reply, a new page, a re-cut or offboarding changes things). Run schedule.py --media again")
    idx = read_json(idx_path, "the request index")
    meta = (idx.get("requests") or {}).get(name)
    if idx.get("client") != cid or not meta:
        die(f"{name} wasn't written for client {cid}'s episode {m['episode'].get('id')}")
    body = read_json(rpath, "the request")
    after = " If it was sent, delete it at once with posts_delete while it is NOT_STARTED."
    if body_sha(body) != meta["body_sha256"]:
        die(f"{name} was edited after schedule.py wrote it. Nothing is recorded: if it was sent like that, check the post "
            "with posts_get, and change client.json or batch.json instead of a request")
    if c.get("status", "active") != "active":
        die(f"client {cid} is {c.get('status')}: nothing is sent or recorded for them." + after)
    mine = {connected_id(a) for a in accounts_of(c).values() if connected_id(a)}
    for k in body.get("socialAccounts") or []:
        sid = k.get("socialAccountId")
        owners = account_owner(m["ws"], sid, m["ledger"]) - {cid}
        if sid not in mine or owners:
            die(f"account {sid} in {name} isn't one of {c.get('name')}'s accounts"
                + (f" (it belongs to client {', '.join(sorted(owners))})" if owners else "") + ". Nothing was recorded." + after)
    appr = load_approvals(m)
    row = next((r for r in m["rows"] if r["id"] == meta["clip"]), None)
    d = (decisions(m, appr) or {}).get(meta["clip"])
    if not row or row.get("hash") != meta["hash"] or not d or d.get("decision") != "approve" or d.get("hash") != meta["hash"]:
        die(f"clip {meta['clip']} has no recorded approval for exactly this file and these captions. Nothing was recorded."
            + after + " Then send the client a new page")
    errs = [msg for lv, msg in row["issues"] if lv == "error"]
    ep_errs = [f"{w}: {msg}" for lv, w, msg in m["issues"] if lv == "error" and not w.startswith("clip ")]
    if errs or ep_errs:
        die(f"clip {meta['clip']} fails a check now: " + "; ".join(errs + ep_errs) + ". Nothing was recorded." + after)
    for e in m["ledger"]["posts"].values():
        if (e.get("client") == cid and e.get("episode") == m["episode"].get("id") and e.get("clip") == meta["clip"]
                and e.get("status") not in ("cancelled", "failed")):
            die(f"clip {meta['clip']} is already handed to WoopSocial as post {e.get('postId')} ({e.get('status')}). "
                "Nothing goes out twice." + (after if not sending else ""))
    if sending:
        when = parse_time(meta["scheduledFor"])
        if when < now_utc() + datetime.timedelta(minutes=MIN_SEND_MINUTES):
            die(f"{name} is for {clock(when, c.get('timezone'))}, less than {MIN_SEND_MINUTES} minutes from now: no time "
                "to cancel it if something changes. Run schedule.py --media again for a new time")
    return meta, body, d, row


def check_request(batch_path, request, ledger_file=None):
    m = check_batch(batch_path, ledger_file)
    meta, body, d, _ = verify(m, request, sending=True)
    print(f"ok to send: {os.path.basename(request)} (clip {meta['clip']}, "
          f"{clock(parse_time(meta['scheduledFor']), m['client'].get('timezone'))}, {'approved by ' + str(d.get('by')) if d.get('how') != 'auto' else str(d.get('by'))}). "
          "Now posts_validate, then posts_create, then --posted")


def record_posted(batch_path, request, post_id, ledger_file=None):
    post_id = (post_id or "").strip()
    if not post_id:
        die("give the post id that posts_create returned: --posted requests/clip-NN.json <postId>")
    m = check_batch(batch_path, ledger_file)
    cid = m["cid"]
    meta, body, d, _ = verify(m, request)
    ledger = m["ledger"]
    now = iso(now_utc())
    for k in body["socialAccounts"]:
        key = f"{post_id}|{k['socialAccountId']}"
        if key in ledger["posts"]:
            die(f"post {post_id} is already recorded")
    for k in body["socialAccounts"]:
        key = f"{post_id}|{k['socialAccountId']}"
        ledger["posts"][key] = {"postId": post_id, "client": cid, "episode": m["episode"].get("id"), "clip": meta["clip"],
                                "platform": k["platform"], "socialAccountId": k["socialAccountId"],
                                "sha256": meta["sha256"], "hash": meta["hash"], "scheduledFor": meta["scheduledFor"],
                                "status": "scheduled", "recorded": now, "request": os.path.basename(request), "url": None,
                                "approved_by": d.get("by"), "approved_at": d.get("at")}
        ledger["accounts"][k["socialAccountId"]] = cid
    ledger["planned"].pop(f"{cid}|{m['episode'].get('id')}|{meta['clip']}", None)
    ledger["clips"].setdefault(meta["sha256"], {"client": cid, "episode": m["episode"].get("id"), "clip": meta["clip"],
                                                "at": now})
    save_ledger(m["lpath"], ledger)
    print(f"recorded: clip {meta['clip']} is post {post_id}, scheduled {clock(parse_time(meta['scheduledFor']), m['client'].get('timezone'))} "
          f"on {', '.join(k['platform'] for k in body['socialAccounts'])}")


def record_cancelled(batch_path, post_id, ledger_file=None):
    m = check_batch(batch_path, ledger_file)
    ledger = m["ledger"]
    keys = [k for k, e in ledger["posts"].items() if e.get("postId") == post_id]
    if not keys:
        die(f"post {post_id} isn't in the ledger")
    if any(ledger["posts"][k].get("client") != m["cid"] for k in keys):
        die(f"post {post_id} belongs to another client, not {m['cid']}")
    for k in keys:
        if ledger["posts"][k].get("status") == "published":
            die(f"post {post_id} is already live on {ledger['posts'][k].get('platform')}; only the client can delete a "
                "live post, in the app")
    for k in keys:
        ledger["posts"][k]["status"] = "cancelled"
        ledger["posts"][k]["cancelled_at"] = iso(now_utc())
    save_ledger(m["lpath"], ledger)
    note = os.path.join(m["bdir"], "requests", f"cancel-{post_id}.json")
    if os.path.isfile(note):
        os.remove(note)
    print(f"recorded as cancelled: post {post_id} ({plural(len(keys), 'account')})")


def unwrap(data):
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


def apply_status(batch_path, status_path, post_id=None, ledger_file=None):
    m = check_batch(batch_path, ledger_file)
    cid = m["cid"]
    data = unwrap(read_json(status_path, "the saved posts_get reply"))
    items = post_items(data)
    if not items:
        die(f"{status_path} holds no per-account posts. Save the whole posts_get reply as it came back")
    top = (data.get("postId") or data.get("id")) if isinstance(data, dict) else None
    pid = (post_id or "").strip() or (top if isinstance(top, str) else None)
    if not pid:
        die(f"{status_path} doesn't say which post it is about: --status {status_path} <postId>")
    if post_id and isinstance(top, str) and top != post_id:
        die(f"{status_path} is the reply for post {top}, not {post_id}")
    ledger = m["ledger"]
    mine = {k: e for k, e in ledger["posts"].items() if e.get("postId") == pid}
    if not mine:
        die(f"the ledger has no post {pid}. Record it first with --posted")
    if any(e.get("client") != cid for e in mine.values()):
        die(f"post {pid} belongs to another client, not {cid}")
    n, failed, too_late, still = 0, [], [], []
    for it in items:
        if isinstance(it.get("postId"), str) and it["postId"] != pid:
            continue
        key = f"{pid}|{it.get('socialAccountId')}"
        if key not in mine:
            continue
        e = ledger["posts"][key]
        st = str(it.get("deliveryStatus") or "").upper()
        if st:
            if e.get("status") == "cancel_requested" and st not in ("PUBLISHED", "FAILED"):
                still.append(e)   # the cancel still waits: a refresh never turns it back into "scheduled"
            else:
                if e.get("status") == "cancel_requested" and st == "PUBLISHED":
                    e["live_after_cancel_request"] = True
                    too_late.append(e)
                e["status"] = STATUS.get(st, e.get("status"))
            e["deliveryStatus"] = st
        if isinstance(it.get("externalPostUrl"), str) and it["externalPostUrl"].strip():
            e["url"] = it["externalPostUrl"].strip()
        t = parse_time(it.get("deliveryCompletedAt"))
        if t:
            e["deliveryCompletedAt"] = iso(t)
        if st == "FAILED":
            failed.append(f"{e.get('platform')}: {it.get('errorMessage') or it.get('error') or 'no reason given'}")
        n += 1
    if not n:
        die(f"{status_path} has no account of post {pid}")
    left = [e for e in ledger["posts"].values() if e.get("postId") == pid and e.get("status") == "cancel_requested"]
    note = os.path.join(m["bdir"], "requests", f"cancel-{pid}.json")
    if not left and os.path.isfile(note):
        os.remove(note)
    save_ledger(m["lpath"], ledger)
    zone = m["client"].get("timezone")
    for e in mine.values():
        print(f"clip {e.get('clip')} on {e.get('platform')}: {e.get('status')}" + (f" {e['url']}" if e.get("url") else ""))
    if still and not too_late:
        t = parse_time(still[0].get("scheduledFor"))
        print(f"CANCEL NOW: post {pid} (clip {still[0].get('clip')}, {clock(t, zone) if t else 'time unknown'}) is still "
              f"waiting to go out: the {still[0].get('cancel_reason') or 'client said no'}. "
              f"posts_delete with postId {pid}, then: schedule.py {rel(m['batch_path'])} --cancelled {pid}")
    for e in too_late:
        print(f"LIVE, NOT CANCELLED: clip {e.get('clip')} went live on {e.get('platform')}"
              + (f" ({e['url']})" if e.get("url") else "") + " before it was cancelled, although the client said no. "
              "WoopSocial can't delete a published post (posts_delete answers POST_NOT_DELETABLE). Tell the client "
              "today, and remove it in the app on that account (the client, or whoever has the login)")
    if too_late and still:
        print(f"  the other accounts of post {pid} haven't gone out yet, but a post with a live part can't be deleted "
              "through WoopSocial either: they will go out too. Remove each one in its app once it is live, and tell "
              "the client")
    for f in failed:
        print(f"  failed: {f}. Check with social_account_posts_list that it isn't live after all before anything is "
              "sent again; a new post needs the same approval, which still holds while the clip is unchanged")


def main():
    ap = argparse.ArgumentParser(description="Schedule the approved clips on the client's own accounts.")
    ap.add_argument("batch")
    ap.add_argument("--media")
    ap.add_argument("--posted", nargs=2, metavar=("REQUEST", "POSTID"))
    ap.add_argument("--check", metavar="REQUEST")
    ap.add_argument("--cancelled", metavar="POSTID")
    ap.add_argument("--status", nargs="+", metavar="STATUS")
    ap.add_argument("--ledger")
    a = ap.parse_args()
    if a.check:
        return check_request(a.batch, a.check, a.ledger)
    if a.cancelled:
        return record_cancelled(a.batch, a.cancelled, a.ledger)
    if a.posted:
        return record_posted(a.batch, a.posted[0], a.posted[1], a.ledger)
    if a.status:
        return apply_status(a.batch, a.status[0], a.status[1] if len(a.status) > 1 else None, a.ledger)
    plan(a.batch, a.media, a.ledger)


if __name__ == "__main__":
    guard(main)
