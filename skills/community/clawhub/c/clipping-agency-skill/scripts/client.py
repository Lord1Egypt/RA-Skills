#!/usr/bin/env python3
"""The client file: create it, check it, connect the client's accounts, list clients, offboard.

    python3 scripts/client.py new <client-id> --name "Show Name"   # clients/<id>/client.json to fill in
    python3 scripts/client.py check <client-id>                    # every field checked, the checklist
    python3 scripts/client.py list                                 # every client and where it stands
    python3 scripts/client.py connect <client-id>                  # the connect steps, per platform
    python3 scripts/client.py project <client-id> <projectId>      # the client's own WoopSocial project
    python3 scripts/client.py accounts <client-id> accounts.json [inputs.json ...]
                                  # the saved social_accounts_list reply (and TikTok's platform inputs):
                                  # each connected account goes into the client's file
    python3 scripts/client.py offboard <client-id>                 # what to cancel and what to revoke
    python3 scripts/client.py offboard <client-id> --cancelled <postId> [<postId> ...]
    python3 scripts/client.py offboard <client-id> --revoked <PLATFORM> [<PLATFORM> ...]
    python3 scripts/client.py offboard <client-id> --done --nothing-waiting
    python3 scripts/client.py release <socialAccountId>             # an offboarded client's account, freed for
                                                                   #   a new client (after a new connect)

Run from the agency's folder (the one holding clients/), or pass --workspace. Every client has its own
folder: clients/<id>/client.json, its episodes, its reports. One WoopSocial project per client keeps
each client's accounts apart, and the account guard refuses an account that another client's file or
the ledger already names. Nothing here asks for, stores or uses a password: the client connects each
account in their own browser through a link.
"""
import argparse, os, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (APPROVAL_RULES, CLIENT_STATUS, DAYS, HEX, HHMM, LIMITS, MAX_CLIPS, PLATFORMS,  # noqa: E402
                       TIKTOK_DAILY_CAP, TIKTOK_PRIVACY, YT_PRIVACY, accounts_of, client_dir, client_ids,
                       connected_id, die, guard, is_num, ledger_path, load_ledger, load_zone, now_utc, iso,
                       placeholder_id, read_json, rel, save_ledger, unwrap_reply, valid_id, workspace_of, write_json,
                       write_text, clock, parse_time)

PLATFORM_NAMES = {p: LIMITS[p]["label"] for p in PLATFORMS}


def template(cid, name):
    return {
        "id": cid, "name": name, "status": "active", "example": False, "show": name,
        "sources": [],
        "platforms": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
        "clips_per_episode": 4, "agreed_clips_per_month": None,
        "cadence": {"days": ["mon", "tue", "wed", "thu", "fri"], "times": ["12:00"], "max_per_day": 1,
                    "min_gap_hours": 3, "start_after_hours": 2},
        "timezone": None,
        "brand": {"accent": "#FFD43B", "text": "#FFFFFF", "hook_bg": "#FFFFFF", "hook_text": "#000000",
                  "uppercase": False, "font": None, "logo": None, "logo_position": "top-right", "end_card": None},
        "names": {}, "no_go": [], "approvers": [],
        "approval": {"rule": "hold"},
        "guest_release": "per_episode",
        "youtube": {"privacy": None, "madeForKids": None},
        "woopsocial": {"projectId": None, "accounts": {}},
        "report": {"recipients": []},
        "expect_episode_every_days": 7,
    }


def project_of(c):
    ws = c.get("woopsocial") if isinstance(c.get("woopsocial"), dict) else {}
    pid = ws.get("projectId")
    return pid.strip() if isinstance(pid, str) and pid.strip() and not placeholder_id(pid) else None


def other_clients(ws, cid):
    """{client id: client dict} for every other client in this folder."""
    out = {}
    for o in client_ids(ws):
        if o != cid:
            try:
                d = read_json(os.path.join(client_dir(ws, o), "client.json"))
            except SystemExit:
                continue
            if isinstance(d, dict):
                out[o] = d
    return out


def validate(c, ws, cid, ledger=None):
    """Every problem with a client file: [(level, field, message)]. Errors stop clips, pages and posts."""
    out = []

    def bad(field, msg, level="error"):
        out.append((level, field, msg))
    if c.get("id") != cid:
        bad("id", f"must be \"{cid}\", the client's folder name")
    if not valid_id(cid):
        bad("id", "use lowercase letters, digits and single dashes (it is a folder name)")
    if not isinstance(c.get("name"), str) or not c["name"].strip():
        bad("name", "the client's name, as the approval page and the report show it")
    if c.get("status", "active") not in CLIENT_STATUS:
        bad("status", "is " + ", ".join(CLIENT_STATUS))
    plats = c.get("platforms")
    if not isinstance(plats, list) or not plats or not all(isinstance(p, str) and p.upper() in PLATFORMS for p in plats):
        bad("platforms", "a list of TIKTOK, INSTAGRAM and YOUTUBE: the client's own accounts the clips go to")
        plats = []
    plats = [p.upper() for p in plats]
    if len(set(plats)) != len(plats):
        bad("platforms", "names a platform twice")
    n = c.get("clips_per_episode")
    if not (isinstance(n, int) and not isinstance(n, bool) and 1 <= n <= MAX_CLIPS):
        bad("clips_per_episode", f"a whole number from 1 to {MAX_CLIPS}: the clips agreed per episode")
    elif n < 3:
        bad("clips_per_episode", f"{n} per episode; most retainers agree 3 to 12. Fine if that is the deal", "note")
    m = c.get("agreed_clips_per_month")
    if m is None:
        bad("agreed_clips_per_month", "not set: the monthly report can't show agreed against delivered without it",
            "warning")
    elif not (isinstance(m, int) and not isinstance(m, bool) and m >= 0):
        bad("agreed_clips_per_month", "a whole number of clips")
    cad = c.get("cadence") if isinstance(c.get("cadence"), dict) else None
    if cad is None:
        bad("cadence", "the posting days and times: {\"days\": [\"mon\", ...], \"times\": [\"12:00\"], \"max_per_day\": 1}")
    else:
        days = cad.get("days")
        if not isinstance(days, list) or not days or not all(isinstance(d, str) and d.lower()[:3] in DAYS for d in days):
            bad("cadence.days", "a list like [\"mon\", \"wed\", \"fri\"]")
        times = cad.get("times")
        if not isinstance(times, list) or not times or not all(isinstance(t, str) and HHMM.fullmatch(t) for t in times):
            bad("cadence.times", "a list of clock times in the client's time zone, like [\"12:00\", \"18:30\"]")
        mpd = cad.get("max_per_day", 1)
        if not (isinstance(mpd, int) and not isinstance(mpd, bool) and 1 <= mpd <= TIKTOK_DAILY_CAP):
            bad("cadence.max_per_day", f"a whole number from 1 to {TIKTOK_DAILY_CAP} (TikTok's daily cap per account)")
        for k, lo, hi in (("min_gap_hours", 0, 48), ("start_after_hours", 1, 168)):
            if k in cad and not (is_num(cad[k], lo) and cad[k] <= hi):
                bad(f"cadence.{k}", f"hours, {lo} to {hi}" + (" (at least an hour, so a post can still be cancelled)"
                                                            if k == "start_after_hours" else ""))
    tz = c.get("timezone")
    if not isinstance(tz, str) or not tz.strip():
        bad("timezone", "the client's time zone, like America/Chicago or Europe/Amsterdam: posting times are theirs")
    elif load_zone(tz) is None:
        bad("timezone", f"\"{tz}\" isn't a time zone this computer knows (a name like America/Chicago; on Windows, "
            "pip install tzdata)")
    b = c.get("brand")
    if not isinstance(b, dict):
        bad("brand", "the brand kit: colours, font, logo, end card")
    else:
        for k in ("accent", "text", "hook_bg", "hook_text"):
            if b.get(k) is not None and not (isinstance(b[k], str) and HEX.fullmatch(b[k])):
                bad(f"brand.{k}", "a colour like #FFD43B")
        cdir = client_dir(ws, cid)
        for k in ("logo", "font"):
            if b.get(k):
                path = b[k] if os.path.isabs(str(b[k])) else os.path.join(cdir, str(b[k]))
                if not os.path.isfile(path):
                    bad(f"brand.{k}", f"{b[k]} isn't there (paths are from the client's folder)")
        if not b.get("logo"):
            bad("brand.logo", "no logo: the clips carry none", "note")
        ec = b.get("end_card")
        if ec is not None and not (isinstance(ec, dict) and isinstance(ec.get("text"), str)):
            bad("brand.end_card", "{\"text\": \"Full episode: <show>\", \"seconds\": 1.5, \"bg\": \"#101820\"} or null")
    names = c.get("names")
    if not isinstance(names, dict) or not all(isinstance(k, str) and isinstance(v, list) and all(isinstance(x, str) for x in v)
                                              for k, v in names.items()):
        bad("names", "the names dictionary: {\"Right Spelling\": [\"wrong one\", \"another wrong one\"]}")
    elif not names:
        bad("names", "empty: add the host, recurring guests, sponsors and jargon, spelled right", "warning")
    if not isinstance(c.get("no_go"), list) or not all(isinstance(x, str) for x in c.get("no_go") or []):
        bad("no_go", "a list of topics or words the client never wants clipped ([] when none)")
    appr = c.get("approvers")
    if not isinstance(appr, list) or not appr or not all(isinstance(a, dict) and isinstance(a.get("name"), str)
                                                         and a["name"].strip() for a in appr):
        bad("approvers", "who approves clips: [{\"name\": \"...\", \"contact\": \"email or phone\"}]")
    ap = c.get("approval") if isinstance(c.get("approval"), dict) else {}
    rule = ap.get("rule", "hold")
    if rule not in APPROVAL_RULES:
        bad("approval.rule", "\"hold\" (silence means nothing posts; the default) or \"auto_after_hours\"")
    elif rule == "auto_after_hours":
        if not (is_num(ap.get("hours"), 1) and ap["hours"] <= 336):
            bad("approval.hours", "1 to 336: how long after the page is sent silence counts as approval")
        if not isinstance(ap.get("agreed_in_writing"), str) or len(ap["agreed_in_writing"].strip()) < 8:
            bad("approval.agreed_in_writing", "auto-posting on silence needs the client's written agreement: say where "
                "and when (\"email from Sam, 2 Nov 2026\"). Without it the rule is \"hold\"")
    gr = c.get("guest_release", "per_episode")
    if gr not in ("per_episode", "covered_by_contract"):
        bad("guest_release", "\"per_episode\" (each episode says whether guest releases are on file) or "
            "\"covered_by_contract\"")
    elif gr == "covered_by_contract" and not (isinstance(c.get("guest_release_note"), str) and c["guest_release_note"].strip()):
        bad("guest_release_note", "say which clause or document covers guests' video and social clips")
    if "YOUTUBE" in plats:
        yt = c.get("youtube") if isinstance(c.get("youtube"), dict) else {}
        if yt.get("privacy") not in YT_PRIVACY:
            bad("youtube.privacy", "public, unlisted or private: the client's choice")
        if not isinstance(yt.get("madeForKids"), bool):
            bad("youtube.madeForKids", "true or false: the channel owner's declaration. Ask the client; never guess")
    # accounts and the guard
    pid = project_of(c)
    accs = accounts_of(c)
    others = other_clients(ws, cid)
    if pid:
        for o, oc in others.items():
            if project_of(oc) == pid:
                bad("woopsocial.projectId", f"{pid} is also client {o}'s project. Each client gets its own project")
    seen = {}
    for p, a in accs.items():
        if p not in PLATFORMS:
            bad(f"woopsocial.accounts.{p}", "only TIKTOK, INSTAGRAM and YOUTUBE")
            continue
        sid = connected_id(a)
        if not sid:
            continue
        if sid in seen:
            bad(f"woopsocial.accounts.{p}", f"the same account id as {seen[sid]}")
        seen[sid] = p
        for o, oc in others.items():
            if any(connected_id(x) == sid for x in accounts_of(oc).values()):
                bad(f"woopsocial.accounts.{p}", f"{sid} is in client {o}'s file too. An account belongs to one client")
        owner = (ledger or {}).get("accounts", {}).get(sid)
        if owner and owner != cid:
            bad(f"woopsocial.accounts.{p}", f"the ledger records {sid} as client {owner}'s account. An account belongs "
                "to one client")
        if p == "TIKTOK":
            opts = a.get("privacyOptions")
            if opts is not None and not (isinstance(opts, list) and opts and all(o in TIKTOK_PRIVACY for o in opts)):
                bad("woopsocial.accounts.TIKTOK.privacyOptions", "the audiences TikTok offers this account "
                    "(social_accounts_get_platform_inputs), from " + ", ".join(TIKTOK_PRIVACY))
            if a.get("max_video_s") is not None and not is_num(a.get("max_video_s"), 3):
                bad("woopsocial.accounts.TIKTOK.max_video_s", "seconds")
    for p in plats:
        if p in accs and connected_id(accs[p]) and not pid:
            bad("woopsocial.projectId", "accounts are listed but no project: run client.py connect")
            break
    return out


def checklist(c, issues, cid):
    """The numbered checklist for the client file: what is set, what is still to do."""
    plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str)]
    accs = accounts_of(c)
    lines = [f"# {c.get('name') or cid}: client checklist", ""]
    if c.get("example") is True:
        lines += ["**EXAMPLE ONLY: a made-up client. Its accounts, ids and numbers are invented.**", ""]
    cad = c.get("cadence") if isinstance(c.get("cadence"), dict) else {}
    ap = c.get("approval") if isinstance(c.get("approval"), dict) else {}
    rule = ("silence means hold: nothing posts without a recorded approval" if ap.get("rule", "hold") == "hold" else
            f"silence for {ap.get('hours')} hours after the page is sent counts as approval "
            f"(agreed in writing: {ap.get('agreed_in_writing')})")
    items = [
        ("Platforms", ", ".join(PLATFORM_NAMES.get(p, p) for p in plats) or "not set"),
        ("Clips", f"{c.get('clips_per_episode')} per episode, {c.get('agreed_clips_per_month') or 'no'} agreed per month"),
        ("Posting", f"{', '.join(cad.get('days') or [])} at {', '.join(cad.get('times') or [])}, at most "
                    f"{cad.get('max_per_day', 1)} a day, {c.get('timezone') or 'no time zone'}"),
        ("Approval", rule + "; approvers: " + (", ".join(a.get("name", "?") for a in c.get("approvers") or []
                                                        if isinstance(a, dict)) or "none")),
        ("Names dictionary", f"{len(c.get('names') or {})} name(s)"),
        ("No-go topics", ", ".join(c.get("no_go") or []) or "none"),
        ("Guest releases", "covered by the contract" if c.get("guest_release") == "covered_by_contract" else
         "stated per episode"),
        ("Sources", f"{len(c.get('sources') or [])} source(s)"),
        ("WoopSocial project", project_of(c) or "not created yet"),
    ]
    for p in plats:
        a = accs.get(p) or {}
        sid = connected_id(a)
        items.append((PLATFORM_NAMES.get(p, p), f"connected {a.get('handle') or ''} ({sid})".replace("  ", " ") if sid
                      else "not connected: run client.py connect"))
    for i, (k, v) in enumerate(items, 1):
        lines.append(f"{i}. **{k}:** {v}")
    errs = [i for i in issues if i[0] == "error"]
    rest = [i for i in issues if i[0] != "error"]
    if errs:
        lines += ["", "## To fix", ""] + [f"- `{f}`: {m}" for _, f, m in errs]
    if rest:
        lines += ["", "## Notes", ""] + [f"- {lv}: `{f}`: {m}" for lv, f, m in rest]
    return "\n".join(lines) + "\n"


def load(ws, cid):
    path = os.path.join(client_dir(ws, cid), "client.json")
    if not os.path.isfile(path):
        known = ", ".join(client_ids(ws)) or "none yet"
        die(f"no client \"{cid}\" (clients/{cid}/client.json). Clients here: {known}. Start one with client.py new")
    c = read_json(path, "the client file")
    if not isinstance(c, dict):
        die(f"clients/{cid}/client.json must hold one JSON object")
    return c, path


def cmd_new(ws, cid, name):
    if not valid_id(cid):
        die(f"\"{cid}\" can't be a client id: use lowercase letters, digits and single dashes, like orbit-podcast")
    path = os.path.join(client_dir(ws, cid), "client.json")
    if os.path.exists(path):
        die(f"clients/{cid}/client.json already exists; edit it, or run client.py check {cid}")
    write_json(path, template(cid, name or cid))
    print(f"wrote {rel(path)}. Fill it in with the client (references/client-file.md has every field), then run "
          f"client.py check {cid}")


def cmd_check(ws, cid, lpath):
    c, path = load(ws, cid)
    issues = validate(c, ws, cid, load_ledger(lpath))
    text = checklist(c, issues, cid)
    write_text(os.path.join(client_dir(ws, cid), "checklist.md"), text)
    print(text)
    errs = sum(1 for i in issues if i[0] == "error")
    print(f"{errs} error(s), {sum(1 for i in issues if i[0] == 'warning')} warning(s) -> {rel(os.path.join(client_dir(ws, cid), 'checklist.md'))}")
    sys.exit(1 if errs else 0)


def cmd_list(ws, lpath):
    ids = client_ids(ws)
    if not ids:
        print("No clients yet. Start one with: client.py new <client-id> --name \"Show Name\"")
        return
    ledger = load_ledger(lpath)
    for cid in ids:
        c, _ = load(ws, cid)
        plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str)]
        conn = sum(1 for p in plats if connected_id(accounts_of(c).get(p)))
        errs = sum(1 for i in validate(c, ws, cid, ledger) if i[0] == "error")
        print(f"{cid:28} {str(c.get('name'))[:30]:30} {c.get('status', 'active'):12} {conn}/{len(plats)} accounts connected"
              + (f", {errs} error(s) in client.json" if errs else "") + (" (EXAMPLE)" if c.get("example") is True else ""))


def cmd_connect(ws, cid):
    c, _ = load(ws, cid)
    plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str)]
    accs = accounts_of(c)
    missing = [p for p in plats if not connected_id(accs.get(p))]
    pid = project_of(c)
    name = c.get("name") or cid
    poss = name + ("'" if name.endswith("s") else "'s")
    print(f"Connect {poss} own accounts. The client signs in on each platform in their own browser; you never "
          "see or keep a password or a code.\n")
    step = 1
    if not pid:
        print(f"{step}. projects_create with name \"{name}\" (one project per client). Then:\n"
              f"   client.py project {cid} <the project id>\n")
        step += 1
    if not missing:
        print(f"{step}. Every platform is connected: {', '.join(plats)}. Run client.py check {cid}.")
        return
    print(f"{step}. oauth_create_authorization with projectId {pid or '<the new project id>'} for each of: "
          + ", ".join(missing) + " (omit redirectUrl).")
    step += 1
    print(f"{step}. Send the links to the client in one message, for example:\n")
    print(f"   \"Hi, to let us post the approved clips on your accounts, please open each link below on a device "
          f"where you're signed in to that account and allow access. The screen will ask you to allow WoopSocial, "
          f"the posting service we use to post the clips you approve and read their numbers. You stay in control: "
          f"you can remove the access any time in each app's settings, and we never need your password.\n"
          + "".join(f"   {PLATFORM_NAMES[p]}: <link>\n" for p in missing) + "   Thanks!\"\n")
    step += 1
    print(f"{step}. When the client says it's done: social_accounts_list with projectId {pid or '<the project id>'}, save "
          f"the reply as accounts.json, and for TikTok social_accounts_get_platform_inputs (save as tiktok-inputs.json). "
          f"Then:\n   client.py accounts {cid} accounts.json tiktok-inputs.json")
    print("\nInstagram needs a Business or Creator account (free to switch in the app). WoopSocial's free plan covers "
          "2 social accounts; one client on TikTok, Reels and Shorts is already 3, so agency use is a paid plan.")


def cmd_project(ws, cid, pid, lpath):
    c, path = load(ws, cid)
    if not isinstance(pid, str) or placeholder_id(pid):
        die("give the id projects_create returned")
    for o, oc in other_clients(ws, cid).items():
        if project_of(oc) == pid:
            die(f"project {pid} is client {o}'s. Each client gets its own project (projects_create)")
    old = project_of(c)
    if old and old != pid and any(connected_id(a) for a in accounts_of(c).values()):
        die(f"client {cid} already has project {old} with connected accounts. Offboard those accounts first, or fix "
            "client.json by hand if the id there is wrong")
    c.setdefault("woopsocial", {})
    if not isinstance(c["woopsocial"], dict):
        c["woopsocial"] = {}
    c["woopsocial"]["projectId"] = pid
    c["woopsocial"].setdefault("accounts", {})
    write_json(path, c)
    print(f"client {cid}: project {pid}. Next: client.py connect {cid}")


def reply_accounts(data):
    """Account entries in a saved social_accounts_list reply: dicts with a platform and an id."""
    found = []

    def walk(x, depth=0):
        if depth > 6:
            return
        if isinstance(x, list):
            for y in x:
                walk(y, depth + 1)
        elif isinstance(x, dict):
            if isinstance(x.get("platform"), str) and isinstance(x.get("id") or x.get("socialAccountId"), str):
                found.append(x)
            else:
                for v in x.values():
                    if isinstance(v, (list, dict)):
                        walk(v, depth + 1)
    walk(unwrap_reply(data))
    return found


def tiktok_inputs(data):
    """(privacy options, max video seconds) from a saved social_accounts_get_platform_inputs reply."""
    opts, secs = None, None

    def walk(x, depth=0):
        nonlocal opts, secs
        if depth > 6:
            return
        if isinstance(x, dict):
            for k, v in x.items():
                kl = k.lower()
                if kl in ("privacyleveloptions", "privacyoptions") and isinstance(v, list):
                    opts = [str(o) for o in v if isinstance(o, str)]
                elif "duration" in kl and is_num(v, 1):
                    secs = int(v)
                elif isinstance(v, (dict, list)):
                    walk(v, depth + 1)
        elif isinstance(x, list):
            for y in x:
                walk(y, depth + 1)
    walk(unwrap_reply(data))
    return opts, secs


def cmd_accounts(ws, cid, files, lpath):
    c, path = load(ws, cid)
    pid = project_of(c)
    if not pid:
        die(f"client {cid} has no WoopSocial project yet: client.py connect {cid}")
    plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str)]
    reply = read_json(files[0], "the saved social_accounts_list reply")
    items = reply_accounts(reply)
    if not items:
        die(f"{files[0]} holds no accounts. Save the whole social_accounts_list reply for project {pid}")
    ledger = load_ledger(lpath)
    others = other_clients(ws, cid)
    accs = c.setdefault("woopsocial", {}).setdefault("accounts", {})
    by_plat = {}
    for it in items:
        if it.get("projectId") not in (None, pid):
            continue   # another project's account: never this client's
        by_plat.setdefault(it["platform"].upper(), []).append(it)
    changed = []
    for p in plats:
        cands = by_plat.get(p, [])
        if not cands:
            print(f"{PLATFORM_NAMES[p]}: not in project {pid} yet (the client hasn't finished that link)")
            continue
        if len(cands) > 1:
            die(f"project {pid} has {len(cands)} {PLATFORM_NAMES[p]} accounts. A client project should hold one per "
                "platform; remove the extra one (social_accounts_delete) after asking the client")
        it = cands[0]
        sid = it.get("id") or it.get("socialAccountId")
        for o, oc in others.items():
            if any(connected_id(x) == sid for x in accounts_of(oc).values()):
                die(f"{sid} is already client {o}'s account. An account belongs to one client")
        if ledger["accounts"].get(sid) not in (None, cid):
            die(f"the ledger records {sid} as client {ledger['accounts'][sid]}'s account. An account belongs to one client")
        status = str(it.get("status") or "").upper()
        handle = next((it.get(k) for k in ("username", "handle", "displayName", "name") if isinstance(it.get(k), str)), "")
        entry = accs.get(p) if isinstance(accs.get(p), dict) else {}
        entry.update({"socialAccountId": sid, "handle": handle})
        if status and status != "CONNECTED":
            print(f"{PLATFORM_NAMES[p]}: {handle} is {status}; send the client a new link (client.py connect)")
            entry["status"] = status
        else:
            entry.pop("status", None)
        accs[p] = entry
        ledger["accounts"][sid] = cid
        changed.append(f"{PLATFORM_NAMES[p]} {handle} ({sid})")
    for f in files[1:]:
        opts, secs = tiktok_inputs(read_json(f, "a saved social_accounts_get_platform_inputs reply"))
        if "TIKTOK" in accs and (opts or secs):
            if opts:
                accs["TIKTOK"]["privacyOptions"] = [o for o in opts if o in TIKTOK_PRIVACY]
            if secs:
                accs["TIKTOK"]["max_video_s"] = secs
            changed.append("TikTok audiences and length limit")
    write_json(path, c)
    save_ledger(lpath, ledger)
    print("saved: " + ("; ".join(changed) if changed else "nothing new") + f". Run client.py check {cid}")


def scheduled_posts(ledger, cid):
    return [(k, e) for k, e in ledger["posts"].items() if e.get("client") == cid
            and e.get("status") in ("scheduled", "processing", "cancel_requested")]


def cmd_release(ws, sid, lpath):
    ledger = load_ledger(lpath)
    owner = ledger["accounts"].get(sid)
    if not owner:
        die(f"the ledger doesn't give {sid} to any client")
    c, _ = load(ws, owner)
    if c.get("status") != "offboarded":
        die(f"{sid} is client {owner}'s account and {owner} is {c.get('status', 'active')}. Only an offboarded client's "
            "account can be released")
    if any(connected_id(a) == sid for a in accounts_of(c).values()):
        die(f"{sid} is still connected in {owner}'s client file")
    del ledger["accounts"][sid]
    save_ledger(lpath, ledger)
    print(f"released {sid} (was {owner}'s, offboarded). It can now be connected for another client; its old posts stay "
          f"in {owner}'s history")


def cmd_offboard(ws, cid, lpath, cancelled=None, revoked=None, done=False, nothing_waiting=False):
    c, path = load(ws, cid)
    ledger = load_ledger(lpath)
    from agencylib import clear_requests
    edir = os.path.join(client_dir(ws, cid), "episodes")
    gone = []
    for ep in sorted(os.listdir(edir)) if os.path.isdir(edir) else []:
        gone += clear_requests(os.path.join(edir, ep), ledger, cid, ep)
    if gone:
        save_ledger(lpath, ledger)
        print(f"removed {len(gone)} unsent request(s): nothing new is sent for this client")
    if cancelled:
        for post_id in cancelled:
            keys = [k for k, e in ledger["posts"].items() if k.split("|")[0] == post_id]
            if not keys:
                die(f"post {post_id} isn't in the ledger")
            if any(ledger["posts"][k].get("client") != cid for k in keys):
                die(f"post {post_id} belongs to another client, not {cid}")
            for k in keys:
                if ledger["posts"][k].get("status") in ("published",):
                    die(f"post {post_id} is already live on {ledger['posts'][k].get('platform')}; only the client can "
                        "delete a live post, in the app")
                ledger["posts"][k]["status"] = "cancelled"
                ledger["posts"][k]["cancelled_at"] = iso(now_utc())
        save_ledger(lpath, ledger)
        print(f"recorded as cancelled: {', '.join(cancelled)}")
    if revoked:
        accs = accounts_of(c)
        raw = c["woopsocial"]["accounts"]
        for p in revoked:
            p = p.upper()
            key = next((k for k in raw if k.upper() == p), None)
            if key is None or not connected_id(accs.get(p)):
                die(f"{p} isn't a connected account of {cid}")
            c.setdefault("revoked", []).append({"platform": p, "socialAccountId": raw[key].get("socialAccountId"),
                                                "handle": raw[key].get("handle"), "at": iso(now_utc())})
            raw[key] = {"socialAccountId": None, "handle": raw[key].get("handle"), "revoked": True}
        write_json(path, c)
        print(f"recorded as removed from WoopSocial: {', '.join(p.upper() for p in revoked)}")
    left = scheduled_posts(ledger, cid)
    still = [p for p, a in accounts_of(c).items() if connected_id(a)]
    if done:
        if left or still:
            die(f"not done yet: {len(left)} scheduled post(s) to cancel and {len(still)} account(s) still connected. "
                f"Run client.py offboard {cid} for the list")
        if not nothing_waiting:
            die("one more check first: social_account_posts_list with the client's projectId and deliveryStatus "
                "NOT_STARTED must show nothing (posts made on another computer or outside this skill aren't in this "
                f"ledger). Then: client.py offboard {cid} --done --nothing-waiting")
        c["status"] = "offboarded"
        c["offboarded_at"] = iso(now_utc())
        write_json(path, c)
        print(f"client {cid} is offboarded: no scheduled posts left, every account removed from WoopSocial.")
        return
    if c.get("status") not in ("offboarding", "offboarded"):
        c["status"] = "offboarding"
        write_json(path, c)
    pid = project_of(c)
    zone = c.get("timezone")
    lines = [f"# Offboarding {c.get('name') or cid}", "",
             f"Status: {c['status']}. No new clips, pages or schedules for this client from now on.", "",
             "## 1. Cancel scheduled posts", ""]
    if left:
        lines.append("These were scheduled and haven't gone out. For each, `posts_delete` with the post id (it works while "
                     "every account of the post is still NOT_STARTED), then `client.py offboard "
                     f"{cid} --cancelled <postId>`:")
        lines.append("")
        seen = set()
        now = now_utc()
        for k, e in sorted(left, key=lambda x: x[1].get("scheduledFor") or ""):
            pid_ = k.split("|")[0]
            when = parse_time(e.get("scheduledFor"))
            past = when and when < now
            lines.append(f"- `{pid_}`: {e.get('platform')} clip {e.get('episode')}/{e.get('clip')}, "
                         f"{clock(when, zone) if when else 'time unknown'}" + (" (same post as above)" if pid_ in seen else "")
                         + (": its time has passed, so it may be live. `posts_get` first, then `schedule.py --status`"
                            if past else ""))
            seen.add(pid_)
    else:
        lines.append("The ledger has no scheduled posts left for this client.")
    lines += ["", f"Then check nothing else waits: `social_account_posts_list` with projectId {pid or '<project>'} and "
              "deliveryStatus NOT_STARTED. Anything there that this ledger doesn't know (made outside this skill) is "
              "listed by that call; ask before deleting it.", "", "## 2. Remove access", ""]
    accs = accounts_of(c)
    if still:
        lines.append("On the agency's side, for each account: `social_accounts_delete` with its id (this removes "
                     "WoopSocial's access token), then `client.py offboard "
                     f"{cid} --revoked <PLATFORM>`:")
        lines.append("")
        for p in still:
            lines.append(f"- {PLATFORM_NAMES.get(p, p)} {accs[p].get('handle') or ''}: `{connected_id(accs[p])}`")
    else:
        lines.append("Every account has been removed from WoopSocial.")
    where = {"TIKTOK": "TikTok", "INSTAGRAM": "Instagram (through Meta's settings)", "YOUTUBE": "your Google account for YouTube"}
    had = [p for p in PLATFORMS if p in still or any(isinstance(r, dict) and r.get("platform") == p for r in c.get("revoked") or [])]
    if had:
        lines += ["", "On the client's side (send them this): \"Your clips stay on your accounts. If you want to be sure no "
                  "app of ours can post, open each app's settings for connected or third-party apps and remove WoopSocial: "
                  + ", ".join(where[p] for p in had) + ".\""]
    lines += ["", "## 3. Hand over and clean up", "",
              "- Send the client their clip files and brand assets if the contract says so.",
              "- Send a last monthly report (report.py) for the posts that went out.",
              "- Delete the client's uploaded media in WoopSocial (`media_list` with the projectId, then `media_delete`) and "
              "their source files on the agency's side, unless the contract says to keep them.", "",
              "## 4. Close", "", f"Once the lists above are empty and `social_account_posts_list` with projectId {pid or '<project>'} "
              f"and deliveryStatus NOT_STARTED shows nothing: `client.py offboard {cid} --done --nothing-waiting`. Live posts "
              "stay on the client's accounts; only the client deletes those.", ""]
    out = os.path.join(client_dir(ws, cid), "offboard.md")
    write_text(out, "\n".join(lines))
    print("\n".join(lines))
    print(f"-> {rel(out)}")


def main():
    ap = argparse.ArgumentParser(description="Create, check, connect, list and offboard clients.")
    ap.add_argument("command", choices=["new", "check", "list", "connect", "project", "accounts", "offboard", "release"])
    ap.add_argument("client", nargs="?")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--name")
    ap.add_argument("--workspace", help="the agency's folder (holds clients/); default: this folder or a parent")
    ap.add_argument("--ledger")
    ap.add_argument("--cancelled", nargs="+")
    ap.add_argument("--revoked", nargs="+")
    ap.add_argument("--done", action="store_true")
    ap.add_argument("--nothing-waiting", action="store_true")
    a = ap.parse_args()
    ws = os.path.abspath(a.workspace) if a.workspace else (workspace_of(os.getcwd()) or os.getcwd())
    lpath = ledger_path(a.ledger)
    if a.command == "list":
        return cmd_list(ws, lpath)
    if not a.client:
        die(f"client.py {a.command} needs the " + ("account id" if a.command == "release" else "client id"))
    if a.command == "release":
        return cmd_release(ws, a.client, lpath)
    if a.command == "new":
        return cmd_new(ws, a.client, a.name)
    if a.command == "check":
        return cmd_check(ws, a.client, lpath)
    if a.command == "connect":
        return cmd_connect(ws, a.client)
    if a.command == "project":
        if len(a.rest) != 1:
            die("usage: client.py project <client-id> <projectId>")
        return cmd_project(ws, a.client, a.rest[0], lpath)
    if a.command == "accounts":
        if not a.rest:
            die("usage: client.py accounts <client-id> accounts.json [tiktok-inputs.json]")
        return cmd_accounts(ws, a.client, a.rest, lpath)
    if a.command == "offboard":
        return cmd_offboard(ws, a.client, lpath, a.cancelled, a.revoked, a.done, a.nothing_waiting)


if __name__ == "__main__":
    guard(main)
