#!/usr/bin/env python3
"""crew: spawn agent CLIs in iTerm2 split panes (one tmux session each),
let them message each other, and save / restore the whole group.

State lives in <project>/.crew.json. Standard library only.
"""
import argparse
import glob
import json
import os
import random
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid

import advise

HERE = os.path.dirname(os.path.abspath(__file__))
PANE = os.path.join(HERE, "pane.zsh")
STATE = ".crew.json"
ITERM = "/Applications/iTerm.app"
EFFORT_SUFFIX = re.compile(r"-(low|medium|high|xhigh|max)$")
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
CLAUDE_MODELS = [("fable", "Claude Fable（最新）"), ("opus", "Claude Opus（最新）")]
CLAUDE_EFFORTS = ["low", "medium", "high", "xhigh", "max"]
AGENTS = ("claude", "codex", "agy")


def die(msg):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False, indent=2))
    sys.exit(1)


def done(**kw):
    print(json.dumps({"ok": True, **kw}, ensure_ascii=False, indent=2))


def run(*argv, stdin=None):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, input=stdin)
    except PermissionError:
        die("系统不允许运行 %s：当前会话多半在沙箱里。crew 需要调用 ps、tmux 和 iTerm2，"
            "Codex 要以 full access 运行（codex -s danger-full-access）才能使用。" % argv[0])
    except FileNotFoundError:
        return 127, ""
    return r.returncode, r.stdout.strip()


def tmux(*argv, stdin=None):
    return run("tmux", *argv, stdin=stdin)


# ---------- state ----------

def find_dir(start):
    """Nearest ancestor holding .crew.json, else `start` itself."""
    d = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(d, STATE)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(start)
        d = parent


def load(d):
    p = os.path.join(d, STATE)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def store(d, state):
    p = os.path.join(d, STATE)
    with open(p + ".tmp", "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(p + ".tmp", p)


def group_name(d):
    g = re.sub(r"[^a-z0-9]+", "-", os.path.basename(d).lower()).strip("-")
    return g or "crew"


def member(state, name):
    for m in state["members"]:
        if m["name"] == name:
            return m
    return None


# ---------- tmux ----------

def alive(session):
    return tmux("has-session", "-t", "=" + session)[0] == 0


def client_tty(session):
    rc, out = tmux("list-clients", "-t", "=" + session, "-F", "#{client_tty}")
    return out.splitlines()[0] if rc == 0 and out else None


def capture(session, lines=0):
    argv = ["capture-pane", "-p", "-t", "=" + session + ":"]
    if lines:
        argv += ["-S", str(-lines)]
    return tmux(*argv)


def keys(session, *k):
    tmux("send-keys", "-t", "=" + session + ":", *k)


def send_text(session, text):
    """Type text into the agent's prompt, then submit. The pause lets the TUI
    finish taking the text in before Enter arrives."""
    target = "=" + session + ":"
    if "\n" in text:
        tmux("load-buffer", "-b", "crew-msg", "-", stdin=text)
        tmux("paste-buffer", "-p", "-d", "-b", "crew-msg", "-t", target)
    else:
        tmux("send-keys", "-t", target, "-l", text)
    time.sleep(0.6)
    tmux("send-keys", "-t", target, "Enter")


def wait_ready(session, timeout=60):
    """Wait until the agent's screen settles; accept a trust-folder dialog."""
    t0, prev, stable, presses = time.time(), None, 0, 0
    while time.time() - t0 < timeout:
        time.sleep(1)
        rc, cur = capture(session)
        if rc != 0:
            return "exited"
        if re.search(r"trust (this folder|the contents|this directory|the files)", cur, re.I):
            chosen = [l for l in cur.splitlines()
                      if re.match(r"\s*[❯>›]\s*\S", l) and re.search(r"\b(Yes|No)\b", l)]
            if presses >= 4:
                return "trust_prompt"
            keys(session, "Enter" if chosen and "Yes" in chosen[-1] else "Down")
            presses += 1
            prev, stable = None, 0
            continue
        if cur.strip() and cur == prev:
            stable += 1
            if stable >= 2:
                return "ready"
        else:
            stable = 0
        prev = cur
    return "timeout"


# ---------- delivery: never type over what the user is typing ----------
# Order of preference for getting a message to a member:
#   codex  `codex queue --thread <live thread>`: the CLI's own queue, no keystrokes
#   agy    `agy agentapi send-message`: needs the member's language-server address and
#          token, which only its own shell commands inherit, so crew.py records them
#          whenever an agy member runs it (register_agy)
#   claude and anything the routes above cannot reach is typed, guarded:
#   typed  only when the input box is empty and nobody has pressed a key in the pane
#          for IDLE_SECS; otherwise the message waits in <project>/.crew/outbox/ and a
#          detached `crew.py flush` delivers it once the box is clear.

IDLE_SECS = 8
WAIT_MAX = 1800
POLL = 2
OUTBOX = os.path.join(".crew", "outbox")
AGY_CREDS = os.path.expanduser("~/.cache/crew/agy")
SGR = re.compile(r"\x1b\[([0-9;]*)m")
ESC = re.compile(r"\x1b(\[[0-9;?]*[A-Za-z]|\][^\x07]*\x07|[()][A-Z0-9])")
RULE = re.compile(r"^\s*─{10,}\s*$")
PROMPT_MARK = {"claude": "❯", "codex": "›", "agy": ">"}


def screen(session):
    """Raw pane lines (with SGR codes) and the cursor row; None if the pane is gone."""
    t = "=" + session + ":"
    try:
        raw = subprocess.run(["tmux", "capture-pane", "-p", "-e", "-t", t],
                             capture_output=True, text=True).stdout
    except OSError:
        return None, None
    rc, cur = tmux("display-message", "-p", "-t", t, "#{cursor_y}")
    if rc != 0 or not cur.isdigit():
        return None, None
    return raw.split("\n"), int(cur)


def bright(line):
    """The text of a line minus what is drawn dim or grey: input-box placeholders
    ("Try …", "Ask Codex to do anything", agy's mode hint) are drawn that way."""
    out, dim, pos = [], False, 0
    for m in SGR.finditer(line):
        if not dim:
            out.append(line[pos:m.start()])
        codes = [c for c in m.group(1).split(";") if c] or ["0"]
        i = 0
        while i < len(codes):
            c = codes[i]
            if c in ("0", "22"):
                dim = False
            elif c in ("2", "90"):
                dim = True
            elif c == "39" and "2" not in codes:
                dim = False
            if c in ("38", "48") and i + 1 < len(codes):
                i += 2 if codes[i + 1] == "5" else 4
            i += 1
        pos = m.end()
    if not dim:
        out.append(line[pos:])
    return ESC.sub("", "".join(out))


def input_state(m):
    """'empty', 'text' or 'unknown' (a dialog, a menu, a layout crew does not know):
    what is in the member's input box right now."""
    raw, cy = screen(m["session"])
    if raw is None:
        return "unknown"
    plain = [ESC.sub("", SGR.sub("", l)) for l in raw]
    mark = PROMPT_MARK.get(m["agent"])
    if m["agent"] in ("claude", "agy"):
        # the box is the space between the two lowest horizontal rules
        rules = [i for i, l in enumerate(plain) if RULE.match(l)]
        if len(rules) < 2:
            return "unknown"
        a, b = rules[-2], rules[-1]
        if b - a < 2 or not plain[a + 1].lstrip().startswith(mark):
            return "unknown"
        box = range(a + 1, b)
    elif m["agent"] == "codex":
        # no rule below the composer: it is the last `›` line plus its continuation
        # lines down to the cursor
        idx = [i for i, l in enumerate(plain) if l == mark or l.startswith(mark + " ")]
        if not idx:
            return "unknown"
        p, end = idx[-1], idx[-1] + 1
        while end < len(plain) and end <= cy and plain[end].startswith("  ") and plain[end].strip():
            end += 1
        box = range(p, end)
    else:
        return "unknown"
    text = []
    for j, i in enumerate(box):
        v = bright(raw[i])
        text.append((v.lstrip()[len(mark):] if j == 0 else v).strip())
    return "text" if any(text) else "empty"


def last_key(session):
    """When a person last pressed a key in this pane (tmux client_activity; crew's own
    send-keys do not count), or 0 when no terminal is attached."""
    rc, out = tmux("list-clients", "-t", "=" + session, "-F", "#{client_activity}")
    return max([int(x) for x in out.split() if x.isdigit()] or [0]) if rc == 0 else 0


def notify(session, text):
    """One line in the pane's tmux status bar, outside the agent's input box."""
    tty = client_tty(session)
    if tty:
        tmux("display-message", "-c", tty, "-d", "6000", text[:200])


def typed(m, text):
    """Type text in only when the box is empty and the keyboard has been idle.
    'typed', 'left_in_box' (the user started typing mid-paste, so Enter is withheld),
    or None (not now)."""
    k0 = last_key(m["session"])
    if time.time() - k0 < IDLE_SECS or input_state(m) != "empty":
        return None
    target = "=" + m["session"] + ":"
    if "\n" in text:
        tmux("load-buffer", "-b", "crew-msg", "-", stdin=text)
        tmux("paste-buffer", "-p", "-d", "-b", "crew-msg", "-t", target)
    else:
        tmux("send-keys", "-t", target, "-l", text)
    time.sleep(0.6)
    if last_key(m["session"]) != k0:
        notify(m["session"], "crew：一条消息已放进输入框但没有发送（检测到你在打字），确认后按回车")
        return "left_in_box"
    tmux("send-keys", "-t", target, "Enter")
    return "typed"


def type_when_clear(m, text, timeout=40):
    """typed(), retried until the box is clear: for crew's own setup messages to a
    pane that has just opened. Types anyway at the end so setup never stalls."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        via = typed(m, text)
        if via:
            return via
        time.sleep(1)
    send_text(m["session"], text)
    return "typed"


def agy_creds_path(m):
    return os.path.join(AGY_CREDS, m["session"] + ".json")


def register_agy(args):
    """Called on every crew.py run: when the caller is an agy member, record the
    address and token of its language server so others can reach it silently."""
    addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS")
    tok = os.environ.get("ANTIGRAVITY_CSRF_TOKEN")
    conv = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
    if not (addr and tok and conv):
        return
    try:
        d = find_dir(getattr(args, "dir", None) or os.getcwd())
        state = load(d)
        if not state:
            return
        m = member(state, caller(state, state["group"])[0])
        agent, pid = calling_agent()
        if not m or m["agent"] != "agy" or agent != "agy":
            return
        os.makedirs(AGY_CREDS, mode=0o700, exist_ok=True)
        p = agy_creds_path(m)
        fd = os.open(p + ".tmp", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump({"address": addr, "token": tok, "conversation": conv, "pid": pid,
                       "at": int(time.time())}, f)
        os.replace(p + ".tmp", p)
        if m.get("session_id") != conv:
            m["session_id"] = conv
            store(d, state)
    except Exception:
        pass  # registering is best effort; delivery falls back to typing


def agy_creds(m):
    """Recorded language-server credentials of an agy member, if its process still runs."""
    try:
        with open(agy_creds_path(m)) as f:
            c = json.load(f)
        os.kill(int(c["pid"]), 0)
        return c
    except (OSError, ValueError, KeyError, TypeError):
        return None


def agy_bin():
    return shutil.which("agy") or os.path.expanduser("~/.local/bin/agy")


def silent(d, state, m, text):
    """Deliver without touching the input box; the route used, or None."""
    if m["agent"] == "codex":
        sid = live_session_id(m)
        if not sid:  # without the thread the pane shows, a queued message could go astray
            return None
        if sid != m.get("session_id"):
            m["session_id"] = sid
            store(d, state)
        rc, out = run("codex", "queue", "--thread", sid, "--message", text)
        return "codex-queue" if rc == 0 and out.startswith("Queued message") else None
    if m["agent"] == "agy":
        c = agy_creds(m)
        if not c:
            return None
        env = dict(os.environ, ANTIGRAVITY_LS_ADDRESS=c["address"],
                   ANTIGRAVITY_CSRF_TOKEN=c["token"])
        try:
            r = subprocess.run([agy_bin(), "agentapi", "send-message", "--title", "crew",
                                c["conversation"], text],
                               capture_output=True, text=True, env=env, timeout=20)
            ok = r.returncode == 0 and '"sendMessage"' in r.stdout and '"error"' not in r.stdout
        except (OSError, subprocess.TimeoutExpired):
            ok = False
        if not ok:  # agy restarted: stale address or token
            try:
                os.unlink(agy_creds_path(m))
            except OSError:
                pass
            return None
        # agy does not echo the incoming message in its pane; show it in the status bar
        notify(m["session"], "crew → %s：%s" % (m["name"], text.replace("\n", " ")))
        return "agentapi"
    return None


def outbox_dir(d, m):
    return os.path.join(d, OUTBOX, m["name"])


def pending(d, m):
    return sorted(glob.glob(os.path.join(outbox_dir(d, m), "*.json")))


def enqueue(d, m, text):
    q = outbox_dir(d, m)
    os.makedirs(q, exist_ok=True)
    p = os.path.join(q, "%d-%04d.json" % (time.time() * 1000, random.randint(0, 9999)))
    with open(p + ".tmp", "w") as f:
        json.dump({"text": text, "created": time.time()}, f, ensure_ascii=False)
    os.replace(p + ".tmp", p)
    subprocess.Popen([sys.executable, os.path.abspath(__file__), "flush", "--to", m["name"],
                      "--dir", d], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True, cwd=d)
    return p


def deliver(d, state, m, text):
    """Get text to member m now if that is safe, else queue it. Returns the route:
    codex-queue / agentapi / typed / left_in_box / queued."""
    if not pending(d, m):  # never overtake messages already waiting for this member
        via = silent(d, state, m, text) or typed(m, text)
        if via:
            return via
    enqueue(d, m, text)
    notify(m["session"], "crew：有消息等你输完再发给 %s（输入框里有内容）" % m["name"])
    return "queued"


def cmd_flush(args):
    """Detached helper: deliver queued messages for one member, oldest first."""
    import fcntl
    d = os.path.abspath(args.dir)
    state = load(d)
    m = member(state, args.to) if state else None
    if not m:
        return
    q = outbox_dir(d, m)
    os.makedirs(q, exist_ok=True)
    with open(os.path.join(q, ".lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)  # one deliverer per member at a time; order kept
        while True:
            files = pending(d, m)
            if not files or not alive(m["session"]):
                return
            p = files[0]
            try:
                with open(p) as f:
                    item = json.load(f)
            except (OSError, ValueError):
                os.replace(p, p + ".bad")
                continue
            if time.time() - item.get("created", 0) > WAIT_MAX:
                os.makedirs(os.path.join(q, "expired"), exist_ok=True)
                os.replace(p, os.path.join(q, "expired", os.path.basename(p)))
                notify(m["session"], "crew：有一条消息等了 %d 分钟仍没发出，已移到 %s"
                       % (WAIT_MAX // 60, os.path.join(OUTBOX, m["name"], "expired")))
                continue
            state = load(d) or state
            m = member(state, args.to) or m
            if silent(d, state, m, item["text"]) or typed(m, item["text"]):
                os.unlink(p)
                continue
            time.sleep(POLL)


# ---------- who is calling ----------

def caller(state, group):
    """(member name, tmux session or None, tty or None) of the calling agent."""
    agent, apid = calling_agent()
    if agent == "codex":
        # codex >= 0.171 runs tool calls from a shared daemon: no tty, and TMUX / ITERM
        # variables are the daemon's, not this session's. Members carry a CREW_MEMBER
        # marker (see agent_argv); a session without it is main.
        m = member(state or {"members": []}, os.environ.get("CREW_MEMBER", ""))
        if m:
            return m["name"], m["session"], client_tty(m["session"])
        if not proc_tty(apid):
            tty, sess = codex_window(os.environ.get("CODEX_THREAD_ID"), state)
            return main_or_guest(state, agent, sess), sess, tty
    pane = os.environ.get("TMUX_PANE")
    if os.environ.get("TMUX") and pane:
        rc, sess = tmux("display-message", "-p", "-t", pane, "#{session_name}")
        if rc == 0 and sess:
            for m in (state or {}).get("members", []):
                if m["session"] == sess:
                    return m["name"], sess, client_tty(sess)
            return main_or_guest(state, agent, sess), sess, client_tty(sess)
    pid = os.getpid()
    while pid > 1:
        rc, out = run("ps", "-o", "ppid=,tty=", "-p", str(pid))
        if rc != 0 or not out:
            break
        ppid, tty = out.split()[:2]
        if tty not in ("??", "-"):
            return main_or_guest(state, agent), None, "/dev/" + tty
        pid = int(ppid)
    return main_or_guest(state, agent), None, None


def main_or_guest(state, agent, sess=None):
    """A caller that is not a member is main, unless the group's main is evidently
    someone else: a different kind of agent, a live tmux session the caller is not
    in, or a conversation still running in another process. Then the caller is just
    another session that happens to sit in (or under) the project directory."""
    main = member(state, "main") if state else None
    if not main:
        return "main"
    if agent and main["agent"] != agent:
        return "guest"
    if alive(main["session"]) and sess != main["session"]:
        return "guest"
    mine = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if agent == "claude" and mine and main.get("session_id") not in (None, mine) \
            and session_running("claude", main["session_id"]):
        return "guest"
    return "main"


def calling_agent():
    """(agent, pid) of the nearest claude / codex / agy process above this script."""
    pid = os.getpid()
    while pid > 1:
        rc, out = run("ps", "-o", "ppid=,comm=", "-p", str(pid))
        if rc != 0 or not out:
            break
        ppid, comm = out.split(None, 1)
        base = os.path.basename(comm.strip())
        if base in AGENTS:
            return base, pid
        pid = int(ppid)
    if os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return "claude", None
    return None, None


def proc_tty(pid):
    out = run("ps", "-o", "tty=", "-p", str(pid))[1].strip()
    return None if out in ("", "??", "-") else "/dev/" + out


def codex_db(sql, *params):
    """Read-only query against codex's thread index; [] when it is unavailable."""
    path = os.path.join(os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex"),
                        "state_5.sqlite")
    try:
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=2)
        try:
            return con.execute(sql, params).fetchall()
        finally:
            con.close()
    except sqlite3.Error:
        return []


def etime_seconds(t):
    """ps etime ([[dd-]hh:]mm:ss) -> seconds."""
    days, _, rest = t.rpartition("-")
    n = 0
    for part in rest.split(":"):
        n = n * 60 + int(part)
    return n + 86400 * int(days or 0)


def codex_window(thread, state=None):
    """(iTerm tty, tmux session or None) of the codex window showing `thread`.
    The daemon does not expose which window owns a thread, so match on the resume
    argument, then on working directory, then on start time. Windows of the group's
    other members are never candidates."""
    if not thread:
        return None, None
    panes = dict(l.split(None, 1) for l in
                 tmux("list-panes", "-a", "-F", "#{pane_tty} #{session_name}")[1].splitlines()
                 if " " in l)
    members = {m["session"] for m in (state or {}).get("members", []) if m["name"] != "main"}

    def where(pr):
        return (client_tty(pr["sess"]) if pr["sess"] else pr["tty"]), pr["sess"]

    procs = []
    for line in run("ps", "-axo", "pid=,tty=,etime=,command=")[1].splitlines():
        f = line.split(None, 3)
        if len(f) < 4 or f[1] in ("??", "-"):
            continue
        argv = f[3].split()
        if os.path.basename(argv[0]) != "codex" or "app-server" in argv or "exec" in argv[1:2]:
            continue
        pr = {"pid": f[0], "tty": "/dev/" + f[1], "sess": panes.get("/dev/" + f[1]),
              "start": time.time() - etime_seconds(f[2])}
        if pr["sess"] in members:
            continue
        if thread in argv:
            return where(pr)
        procs.append(pr)
    row = codex_db("select cwd, created_at_ms from threads where id = ?", thread)
    cwd, created = (row[0][0], row[0][1] / 1000.0) if row else (os.getcwd(), time.time())
    here = []
    for pr in procs:
        out = run("lsof", "-a", "-d", "cwd", "-p", pr["pid"], "-Fn")[1]
        dirs = [l[1:] for l in out.splitlines() if l.startswith("n")]
        if dirs and os.path.realpath(dirs[0]) == os.path.realpath(cwd):
            here.append(pr)
    if len(here) > 1:  # the thread is created a few seconds after its window starts
        here = sorted((pr for pr in here if pr["start"] <= created + 5),
                      key=lambda pr: pr["start"])[-1:]
    return where(here[0]) if here else (None, None)


def codex_intro_thread(d, state, m):
    """Thread a freshly spawned codex member is on, found by the intro we sent it."""
    head = "[crew] 你是协作组「%s」的 agent，名称 %s。" % (state["group"], m["name"])
    for tid, cwd in codex_db("select id, cwd from threads where first_user_message like ? "
                             "order by created_at_ms desc limit 5", head + "%"):
        if os.path.realpath(cwd) == os.path.realpath(d):
            return tid
    return None


def calling_session_id(agent, pid):
    if agent == "claude" and os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return os.environ["CLAUDE_CODE_SESSION_ID"]
    if agent == "codex" and os.environ.get("CODEX_THREAD_ID"):
        return os.environ["CODEX_THREAD_ID"]
    if not agent or not pid:
        return None
    return agent_session_id(agent, [str(pid)] + run("pgrep", "-P", str(pid))[1].split())


GUEST = ("当前会话不属于「%s」组（该组的 main 是 %s 会话，组文件在 %s）。"
         "要在当前目录另建一个组，用 spawn --here。")


def sync_main(state, who, args, d):
    """Refresh main's record when main itself is calling; refuse a non-member."""
    main = member(state, "main")
    if who == "guest":
        die(GUEST % (state["group"], main["agent"], os.path.join(d, STATE)))
    if who != "main":
        return
    agent, pid = calling_agent()
    if not agent:
        return
    sid = calling_session_id(agent, pid)
    if sid:
        main["session_id"] = sid
    if getattr(args, "main_model", None):
        main["model"] = split_agy(args.main_model)[0] if agent == "agy" else args.main_model
    if getattr(args, "main_effort", None):
        main["effort"] = args.main_effort


def split_agy(model):
    """agy ids may carry the effort as a suffix: gemini-4-neon-high -> (family, effort)."""
    hit = EFFORT_SUFFIX.search(model or "")
    return (model[:hit.start()], hit.group(1)) if hit else (model, None)


# ---------- iTerm2 ----------

SPLIT = '''
on run argv
  set {fromTTY, dirn, cmd} to argv
  tell application "%s"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if (tty of s) is fromTTY then
            if dirn is "v" then
              tell s to set n to (split vertically with default profile command cmd)
            else
              tell s to set n to (split horizontally with default profile command cmd)
            end if
            set newTTY to tty of n
            tell s to select
            return newTTY
          end if
        end repeat
      end repeat
    end repeat
  end tell
  return "NOTFOUND"
end run
''' % ITERM

WINDOW = '''
on run argv
  tell application "%s"
    activate
    set w to (create window with default profile command (item 1 of argv))
    set zoomed of w to true
    return tty of current session of w
  end tell
end run
''' % ITERM

FOCUS = '''
on run argv
  tell application "%s"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if (tty of s) is (item 1 of argv) then
            activate
            select w
            select t
            tell s to select
            return "OK"
          end if
        end repeat
      end repeat
    end repeat
  end tell
  return "NOTFOUND"
end run
''' % ITERM


def osa(script, *argv):
    agent, pid = calling_agent()
    if agent == "codex" and not proc_tty(pid):
        return osa_via_tmux(script, *argv)
    try:
        r = subprocess.run(["/usr/bin/osascript", "-", *argv], input=script,
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        die("iTerm2 没有响应 AppleScript。检查 系统设置 > 隐私与安全性 > 自动化 里"
            "当前终端或 agent 是否被允许控制 iTerm。")
    if r.returncode != 0:
        die("iTerm2 AppleScript 失败：" + r.stderr.strip())
    return r.stdout.strip()


def osa_via_tmux(script, *argv):
    """codex runs tool calls from a background daemon that macOS will not let drive
    iTerm2 (the consent prompt never appears and the AppleEvent times out). The tmux
    server was started from an iTerm2 pane and is allowed to, so let it run osascript."""
    if tmux("list-sessions")[0] != 0:
        die("Codex 的后台进程不能直接控制 iTerm2，需要借助一个已经在 iTerm2 里运行的 tmux。"
            "先在 iTerm2 里运行 tmux（在 tmux 里启动 codex 最简单），再重试。")
    base = os.path.join(tempfile.gettempdir(), "crew-osa-%d" % os.getpid())
    with open(base + ".scpt", "w") as f:
        f.write(script)
    with open(base + ".sh", "w") as f:  # a file, so tmux does not expand # in the arguments
        f.write("/usr/bin/osascript %s > %s 2> %s\necho $? > %s\n" % (
            " ".join(shlex.quote(a) for a in (base + ".scpt",) + argv),
            shlex.quote(base + ".out"), shlex.quote(base + ".err"), shlex.quote(base + ".rc")))
    tmux("run-shell", "/bin/sh " + shlex.quote(base + ".sh"))

    def slurp(ext):
        try:
            with open(base + ext) as f:
                return f.read().strip()
        except OSError:
            return ""
    rc, out, err = slurp(".rc"), slurp(".out"), slurp(".err")
    for ext in (".scpt", ".sh", ".out", ".err", ".rc"):
        try:
            os.remove(base + ext)
        except OSError:
            pass
    if rc != "0":
        die("iTerm2 AppleScript 失败（经 tmux 执行）：" + (err or "没有返回结果"))
    return out


def dq(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def pane_command(session, d, argv):
    return " ".join(["/bin/zsh", dq(PANE), dq(session), dq(d)] + [dq(a) for a in argv])


# ---------- agents ----------

def agent_argv(m, resume):
    sid, model, effort = m.get("session_id"), m.get("model"), m.get("effort")
    a = m["agent"]
    if a == "claude":
        argv = ["claude"]
        if resume and sid:
            argv += ["--resume", sid]
        elif sid:
            argv += ["--session-id", sid]
        if model:
            argv += ["--model", model]
        if effort:
            argv += ["--effort", effort]
        return argv
    if a == "codex":
        argv = ["codex"] + (["resume", sid] if resume and sid else [])
        if model:
            argv += ["-m", model]
        if effort:
            argv += ["-c", "model_reasoning_effort=" + effort]
        if not m.get("sandbox"):
            argv += ["-s", "danger-full-access", "-a", "never"]
        # tool calls run in a shared daemon; this is how crew.py learns who is calling
        argv += ["-c", 'shell_environment_policy.set.CREW_MEMBER="%s"' % m["name"]]
        return argv
    if a == "agy":
        argv = ["agy"] + (["--conversation", sid] if resume and sid else [])
        if model:
            # agy model ids carry the effort as a suffix: gemini-4-neon-high
            argv += ["--model", model + "-" + effort if effort else model]
        if effort:
            argv += ["--effort", effort]
        return argv
    die("未知 agent：" + a)


def agy_catalog():
    """{family: {"label":..., "efforts":[...]}} in the CLI's own order."""
    rc, out = run("agy", "models")
    fams = {}
    for line in out.splitlines():
        if "\t" not in line:
            continue
        mid, label = line.split("\t", 1)
        hit = EFFORT_SUFFIX.search(mid)
        if not hit:
            continue
        fam = fams.setdefault(mid[:hit.start()],
                              {"label": re.sub(r"\s*\(.*\)$", "", label), "efforts": []})
        fam["efforts"].append(hit.group(1))
    return fams


def codex_catalog():
    rc, out = run("codex", "debug", "models")
    try:
        models = json.loads(out)["models"]
    except Exception:
        try:
            with open(os.path.expanduser("~/.codex/models_cache.json")) as f:
                models = json.load(f)["models"]
        except Exception:
            return []
    models = [x for x in models if x.get("visibility") == "list"]
    return sorted(models, key=lambda x: x.get("priority", 999))


def live_session_id(m):
    """Session id the agent in this pane is using right now (None if unknown)."""
    rc, out = tmux("list-panes", "-t", "=" + m["session"], "-F", "#{pane_pid}")
    if rc != 0 or not out:
        return None
    pid = out.splitlines()[0]
    return agent_session_id(m["agent"], [pid] + run("pgrep", "-P", pid)[1].split())


def agent_session_id(agent, pids):
    if agent == "claude":
        for p in pids:
            try:
                with open(os.path.expanduser("~/.claude/sessions/%s.json" % p)) as f:
                    return json.load(f)["sessionId"]
            except Exception:
                continue
        return None
    pat = {"codex": r"/rollout-[^/]*-(%s)\.jsonl$" % UUID,
           "agy": r"/conversations/(%s)\.db$" % UUID}[agent]
    for p in pids:
        rc, out = run("lsof", "-p", p, "-Fn")
        for line in out.splitlines():
            hit = re.search(pat, line)
            if hit:
                return hit.group(1)
    return None


def session_running(agent, sid):
    """pid of a live agent process on this session id, else None."""
    if agent != "claude":
        if agent == "codex" and any(codex_window(sid)):
            return int(run("pgrep", "-x", "codex")[1].split()[0])
        for p in run("pgrep", "-x", agent)[1].split():
            if agent_session_id(agent, [p] + run("pgrep", "-P", p)[1].split()) == sid:
                return int(p)
        return None
    for p in glob.glob(os.path.expanduser("~/.claude/sessions/*.json")):
        try:
            with open(p) as f:
                d = json.load(f)
            if d.get("sessionId") == sid:
                os.kill(int(d["pid"]), 0)
                return int(d["pid"])
        except Exception:
            continue
    return None


# ---------- commands ----------

def claude_models():
    """Claude Code model aliases always resolve to the newest model of a family, so the
    menu stays current across releases. Users can replace it in roles.json."""
    user = advise.read_json(advise.ROLES, {}) or {}
    rows = user.get("claude_models")
    if isinstance(rows, list) and rows:
        return [(r[0], r[1] if len(r) > 1 else r[0]) for r in rows if r]
    return CLAUDE_MODELS


def installed(agent):
    return shutil.which(agent) is not None


def all_options():
    """Every model crew can start, in each CLI's own order."""
    rows = []
    if installed("codex"):
        for x in codex_catalog():
            rows.append({"agent": "codex", "model": x["slug"], "label": x["display_name"],
                         "efforts": [e["effort"] for e in x.get("supported_reasoning_levels", [])]})
    if installed("agy"):
        for fam, info in agy_catalog().items():
            rows.append({"agent": "agy", "model": fam, "label": info["label"],
                         "efforts": info["efforts"]})
    if installed("claude"):
        for mid, label in claude_models():
            rows.append({"agent": "claude", "model": mid, "label": label,
                         "efforts": CLAUDE_EFFORTS})
    return rows


def menu_options():
    """The spawn menu: the first two models of each installed CLI."""
    rows, count = [], {}
    for o in all_options():
        count[o["agent"]] = count.get(o["agent"], 0) + 1
        if count[o["agent"]] <= 2:
            rows.append(o)
    return rows


def cmd_models(args):
    rows = all_options() if args.all else menu_options()
    q = {} if args.no_quota else advise.quota(sorted({r["agent"] for r in rows}),
                                               installed=installed)
    for i, r in enumerate(rows, 1):
        r["n"] = i
        b = advise.bottleneck(r["agent"], r["model"], q) if q else None
        r["quota"] = ("%.0f%%（%s）" % (b["remaining"], b["label"])) if b else None
    done(options=rows, quota_notes={a: v["note"] for a, v in q.items()} or None)


def cmd_quota(args):
    agents = [args.agent] if args.agent else list(AGENTS)
    done(quota=advise.quota(agents, refresh=args.refresh, installed=installed),
         cache=advise.QUOTA_CACHE, ttl_seconds=advise.QUOTA_TTL)


def cmd_advise(args):
    opts = [dict(o, effort=args.effort) for o in (all_options() if args.all else menu_options())]
    agents = sorted({o["agent"] for o in opts})
    q = advise.quota(agents, installed=installed)
    res = advise.advise(args.task, opts, q)
    if "error" in res:
        die(res["error"])
    if not args.verbose:
        res["candidates"] = res["candidates"][:args.top]
    done(**res)


RANKINGS_SCHEMA = {
    "source": "https://arena.ai/leaderboard",
    "fetched": "YYYY-MM-DD",
    "categories": {"webdev": [{"name": "Model Name (Effort)", "rank": 1, "score": 1800,
                               "cost": 2.5}]}}


def cmd_rankings(args):
    if args.action == "import":
        try:
            with open(args.file) as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            die("读不了 %s：%s" % (args.file, e))
        errs = advise.validate_rankings(data)
        if errs:
            die("格式不对：" + "；".join(errs[:8]))
        advise.write_json(advise.RANKINGS, data)
    if args.action == "show":
        data = advise.load_rankings()
        if not data:
            die("还没有排行数据（%s）。先按 SKILL.md 的步骤从 arena.ai 读取并 rankings import。"
                % advise.RANKINGS)
        menu = menu_options()
        cats = [args.file] if args.file else list(data["categories"])
        out = {}
        for c in cats:
            rows = sorted(data["categories"].get(c) or [], key=lambda r: r.get("rank") or 999)
            for r in rows:
                r["in_menu"] = None
            for o in menu:
                e = advise.match_entry(rows, o["agent"], o["model"], None, advise.all_rows(data))
                if e:   # every effort variant of the newest matching version
                    base = advise.split_variant(e["name"])[0]
                    for r in rows:
                        if advise.split_variant(r["name"])[0] == base:
                            r["in_menu"] = "%s/%s" % (o["agent"], o["model"])
            out[c] = rows
        st = advise.rankings_status()
        done(fetched=st.get("fetched"), age_days=st.get("age_days"), stale=st["stale"],
             source=data.get("source"), note=data.get("note"), categories=out)
        return
    st = advise.rankings_status()
    roles = advise.load_roles()
    wanted = sorted({c for t in roles["tasks"].values() for c in t.get("arena") or []})
    done(rankings=st, categories_used_by_tasks=wanted,
         missing=[c for c in wanted if c not in (st.get("categories") or {})],
         schema=RANKINGS_SCHEMA if (args.action == "schema" or st["stale"]) else None)


def cmd_doctor(args):
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "ok": ok, "detail": detail})
    add("macOS", sys.platform == "darwin", sys.platform)
    add("python3 >= 3.8", sys.version_info >= (3, 8), sys.version.split()[0])
    add("tmux", installed("tmux"), run("tmux", "-V")[1] or "未安装")
    add("iTerm2", os.path.isdir(ITERM), ITERM)
    for a in AGENTS:
        if installed(a):
            add(a, True, (run(a, "--version")[1].splitlines() or ["?"])[0])
        else:
            add(a, None, "未安装（可选）")
    if installed("codex"):
        ok = run("codex", "queue", "--help")[0] == 0
        add("codex queue（静默投递）", ok or None,
            "可用" if ok else "这个版本没有 codex queue，给 Codex 发消息会改用输入框（升级 codex 可解决）")
    if installed("agy"):
        ok = run(agy_bin(), "agentapi", "--help")[0] == 0
        add("agy agentapi（静默投递）", ok or None,
            "可用" if ok else "这个版本没有 agentapi，给 agy 发消息会改用输入框")
    opts = all_options()
    for a in AGENTS:
        if installed(a):
            n = sum(1 for o in opts if o["agent"] == a)
            add("%s 模型列表" % a, n > 0, "%d 个模型" % n if n else "读不到模型列表，CLI 输出格式可能已变")
    q = advise.quota([a for a in AGENTS if installed(a)], refresh=args.refresh, installed=installed)
    for a, v in q.items():
        add("%s 额度" % a, bool(v["pools"]) or None,
            "%s %s" % (v["note"], "；".join("%s %.0f%%" % (p["label"], p["remaining"])
                                            for p in v["pools"])))
    st = advise.rankings_status()
    add("排行榜", st["present"] and not st["stale"],
        "未导入（%s）" % st["path"] if not st["present"]
        else "抓取于 %s，%s 天前%s" % (st["fetched"], st["age_days"], "，已过期" if st["stale"] else ""))
    roles = advise.load_roles()
    add("个人分工配置", True, roles["user_file"] + ("" if roles["user_present"] else "（未创建，使用默认）"))
    done(checks=checks, failed=[c["check"] for c in checks if c["ok"] is False])


def intro_text(state, m, main_reachable):
    others = "、".join("%s(%s)" % (x["name"], x["agent"])
                       for x in state["members"] if x["name"] != m["name"])
    t = ("[crew] 你是协作组「%s」的 agent，名称 %s。组员：%s。"
         % (state["group"], m["name"], others))
    if m["agent"] == "codex" and m.get("sandbox"):
        t += "你运行在沙箱内，无法主动给组员发消息；直接在本窗格回答，组员会来读取。"
    else:
        t += ("给组员发消息请运行：python3 %s send --to <名称> \"内容\"（自动署名）。"
              % dq(os.path.abspath(__file__)))
        if not main_reachable:
            t += "main 目前不在 tmux 中，收不到消息，它会主动读取你的窗格。"
    t += "以 [from 名称] 开头的输入来自组员。"
    if m["agent"] == "agy":
        # registers this agy's language server so messages can skip the input box
        t += ("现在先运行一次：python3 %s whoami，再只回复：%s 就绪。"
              % (dq(os.path.abspath(__file__)), m["name"]))
    else:
        t += "现在只需回复：%s 就绪。" % m["name"]
    return t


REREGISTER = ("[crew] 窗口已恢复。请运行一次 python3 %s whoami 重新登记消息通道，"
              "然后只回复：已登记，不要做别的。")


def cmd_spawn(args):
    d = os.path.abspath(args.dir) if args.here else find_dir(args.dir)
    state = load(d)
    group = state["group"] if state else group_name(d)
    who, who_sess, who_tty = caller(state, group)

    if not state:
        agent, pid = calling_agent()
        if not agent:
            die("建组要由 claude / codex / agy 会话来执行（在调用链上没有找到这些进程）。")
        model, effort = args.main_model, args.main_effort
        if agent == "agy":
            model, suffix = split_agy(model)
            effort = effort or suffix
        elif agent == "claude":
            effort = effort or os.environ.get("CLAUDE_EFFORT")
        state = {"group": group, "members": [{
            "name": "main", "agent": agent, "model": model, "effort": effort,
            "session_id": calling_session_id(agent, pid),
            "session": who_sess or group + "-main", "split": None}]}
    else:
        sync_main(state, who, args, d)

    name = args.name
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        die("名称只能用小写字母、数字和连字符：" + name)
    if member(state, name):
        die("组里已有名为 %s 的 agent。" % name)
    session = group + "-" + name
    if alive(session):
        die("tmux 会话 %s 已存在（不在本组记录里）。先确认它是什么，再 tmux kill-session -t %s。"
            % (session, session))

    model, effort = args.model, args.effort
    if args.agent == "agy":
        model = split_agy(model)[0]
        fams = agy_catalog()
        if model not in fams:
            die("agy 没有模型 %s。可选：%s" % (model, "、".join(fams)))
        if effort not in fams[model]["efforts"]:
            die("%s 不支持 effort %s。可选：%s" % (model, effort, "、".join(fams[model]["efforts"])))

    # default layout: 1st agent right of main, 2nd under the 1st, 3rd under main,
    # later ones to the right of earlier agents
    agents = [x for x in state["members"] if x["name"] != "main"]
    k = len(agents) + 1
    if args.split_from:
        src, direction = args.split_from, args.split or "v"
    elif k == 1:
        src, direction = "main", "v"
    elif k == 2:
        src, direction = agents[0]["name"], "h"
    elif k == 3:
        src, direction = "main", "h"
    else:
        src, direction = agents[k - 4]["name"], "v"
    src_m = member(state, src)
    if not src_m:
        die("找不到用来分屏的成员：" + src)
    src_tty = client_tty(src_m["session"]) or (who_tty if src == who else None)
    if not src_tty:
        die("成员 %s 的窗格当前不可见，无法从它分屏。可用 --from 指定其他成员。" % src)

    m = {"name": name, "agent": args.agent, "model": model, "effort": effort,
         "session_id": str(uuid.uuid4()) if args.agent == "claude" else None,
         "session": session, "split": {"from": src, "dir": direction}}
    if args.agent == "codex":
        m["sandbox"] = args.sandbox
    argv = agent_argv(m, resume=False)
    tty = osa(SPLIT, src_tty, direction, pane_command(session, d, argv))
    if tty == "NOTFOUND":
        die("在 iTerm2 里找不到 tty 为 %s 的窗格。" % src_tty)

    for _ in range(20):
        if alive(session):
            break
        time.sleep(0.5)
    else:
        die("窗格已打开但 tmux 会话没有起来（命令可能立即退出）。手动运行查看报错：%s"
            % " ".join(argv))

    state["members"].append(m)
    store(d, state)
    status = wait_ready(session)
    if status == "ready":
        main_sess = member(state, "main")["session"]
        type_when_clear(m, intro_text(state, m, alive(main_sess)))
        for _ in range(30):
            time.sleep(1)
            sid = live_session_id(m) or (
                codex_intro_thread(d, state, m) if m["agent"] == "codex" else None)
            if sid:
                m["session_id"] = sid
                break
        store(d, state)
    warn = None
    b = advise.bottleneck(args.agent, model, advise.quota([args.agent], installed=installed))
    if b and b["remaining"] < advise.load_roles()["policy"].get("min_quota", 20):
        warn = "%s 只剩 %.0f%%%s。可用 advise 看替代模型。" % (
            b["label"], b["remaining"], "，%s 重置" % b["resets"] if b["resets"] else "")
    done(name=name, session=session, tty=tty, status=status, command=" ".join(argv),
         session_id=m["session_id"], state_file=os.path.join(d, STATE), quota_warning=warn,
         note=None if status == "ready" else "agent 未就绪：用 read 查看窗格内容并处理。")


def need_state(args):
    d = find_dir(args.dir)
    state = load(d)
    if not state:
        die("%s 及其上级目录里没有 %s。先 spawn 一个 agent。" % (os.path.abspath(args.dir), STATE))
    return d, state


def cmd_send(args):
    d, state = need_state(args)
    who, sess = caller(state, state["group"])[:2]
    reply = ""
    sessions = {x["session"] for x in state["members"]}
    if who == "guest" or (sess and sess not in sessions):
        # A member of another group writing across (send --dir <other project>): name it by
        # its own group so the receiver knows who it is and how to answer.
        home = find_dir(os.getcwd())
        hs = load(home) if home != d else None
        hwho = caller(hs, hs["group"])[0] if hs else "guest"
        if hs and hwho != "guest":
            who = "%s/%s" % (hs["group"], hwho)
            reply = "（回复：crew send --dir %s --to %s）" % (home, hwho)
        elif sess:
            who = sess
    m = member(state, args.to)
    if not m:
        die("没有成员 %s。现有：%s" % (args.to, "、".join(x["name"] for x in state["members"])))
    if m["name"] == who:
        die("不能给自己发消息。")
    if not alive(m["session"]):
        die("%s 不在 tmux 中（会话 %s 不存在），收不到消息。" % (m["name"], m["session"])
            + ("main 要在恢复（restore）之后才进 tmux。" if m["name"] == "main" else ""))
    me, tid = member(state, who), os.environ.get("CODEX_THREAD_ID")
    agent = calling_agent()[0]
    if me and me["agent"] == "codex" and agent == "codex" and tid \
            and tid != me.get("session_id"):
        me["session_id"] = tid
        store(d, state)
    text = "[from %s]%s %s" % (who, reply, args.message)
    via = deliver(d, state, m, text)
    done(sent_to=m["name"], sender=who, via=via,
         note={"queued": "%s 的输入框里有内容或正在打字，消息已排队，空出来后自动发送"
                         "（最多等 %d 分钟）。" % (m["name"], WAIT_MAX // 60),
               "left_in_box": "对方正好在打字：消息已放进输入框但没按回车，由对方确认发送。"}.get(via))


TASKS = os.path.join(".crew", "tasks.json")
BUSY_MARKS = ("esc to interrupt", "esc to cancel", "Working (", "Thinking", "Running…")


def load_tasks(d):
    p = os.path.join(d, TASKS)
    try:
        with open(p) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def store_tasks(d, tasks):
    p = os.path.join(d, TASKS)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + ".tmp", "w") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(p + ".tmp", p)


def cmd_task(args):
    d, state = need_state(args)
    who = caller(state, state["group"])[0]
    name = args.for_ or who
    if args.for_ and who != "main":
        die("只有 main 能替别人记任务；记自己的不要加 --for。")
    if not member(state, name):
        die("没有成员 %s。现有：%s" % (name, "、".join(x["name"] for x in state["members"])))
    tasks = load_tasks(d)
    t = tasks.get(name, {"now": "", "next": []})
    if args.done:
        t["now"] = ""
    if args.now is not None:
        t["now"] = args.now.strip()
    if args.clear_next:
        t["next"] = []
    t["next"] = t.get("next", []) + [x.strip() for x in args.next if x.strip()]
    t["updated"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    t["by"] = who
    tasks[name] = t
    store_tasks(d, tasks)
    done(member=name, **{k: t[k] for k in ("now", "next", "updated")})


FLOW = os.path.join(".crew", "flow.json")
FLOW_MARK = {"todo": "·", "doing": "▶", "done": "✓", "blocked": "⏸"}


def load_flow(d):
    try:
        with open(os.path.join(d, FLOW)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"steps": []}


def cmd_flow(args):
    d, state = need_state(args)
    who = caller(state, state["group"])[0]
    fl = load_flow(d)
    steps = fl.setdefault("steps", [])
    edit = args.clear or args.add or args.status or args.remove
    if edit and who != "main":
        die("只有 main 能改工作流程；组员用 task 登记自己的任务。")

    def idx(n):
        if not 1 <= n <= len(steps):
            die("没有第 %d 步（共 %d 步）" % (n, len(steps)))
        return n - 1
    if args.clear:
        steps.clear()
    for a in args.add:
        text, _, owner = a.partition("@")
        steps.append({"step": text.strip(), "owner": owner.strip(), "status": "todo"})
    if args.status:
        n, st = args.status
        if st not in FLOW_MARK:
            die("状态只能是 todo / doing / done / blocked")
        steps[idx(int(n))]["status"] = st
    if args.remove:
        steps.pop(idx(args.remove))
    if edit:
        fl["updated"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        p = os.path.join(d, FLOW)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p + ".tmp", "w") as f:
            json.dump(fl, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(p + ".tmp", p)
    done(**fl)


def print_flow(fl):
    steps = fl.get("steps") or []
    if not steps:
        return

    def name(x):
        return x["step"] + (("（%s）" % x["owner"]) if x.get("owner") else "")
    done_ = [x for x in steps if x.get("status") == "done"]
    rest = [x for x in steps if x.get("status") != "done"]
    print("\n关键路径%s" % (("（更新于 %s）" % fl["updated"]) if fl.get("updated") else ""))
    if rest:
        chain, k = [], 0
        while k < len(rest):
            # consecutive steps already under way run in parallel: join them with 、
            if rest[k].get("status") in ("doing", "blocked"):
                grp = []
                while k < len(rest) and rest[k].get("status") in ("doing", "blocked"):
                    grp.append(("⏸" if rest[k]["status"] == "blocked" else "▶") + name(rest[k]))
                    k += 1
                chain.append("、".join(grp))
            else:
                chain.append(name(rest[k]))
                k += 1
        print("  " + " → ".join(chain))
    else:
        print("  全部完成")
    if done_:
        print("  已完成：" + "；".join(x["step"] for x in done_))


def busy_state(m):
    if not alive(m["session"]):
        return "离线"
    rc, out = capture(m["session"], 40)
    if rc != 0:
        return "未知"
    tail = "\n".join(out.splitlines()[-25:])
    return "忙" if any(k in tail for k in BUSY_MARKS) else "空闲"


STALL_MARKS = ("API Error", "Connection dropped", "ECONNRESET", "Resend your message",
               "Error running remote compact", "No response from API", "stream disconnected",
               "Connection failed")
NUDGE = ("刚才连接中断，你停在了提示符上。请从断点继续你登记的任务：%s。已完成的部分保留，"
         "做完照常更新 crew task 并报告。")


def stalled(m):
    """A member idle at its prompt right after a connection error (not finished, just stopped)."""
    if not alive(m["session"]):
        return None
    rc, out = capture(m["session"], 40)
    if rc != 0:
        return None
    tail = "\n".join(out.splitlines()[-25:])
    if any(k in tail for k in BUSY_MARKS):
        return None
    hit = [k for k in STALL_MARKS if k in tail]
    return hit[0] if hit else None


def cmd_watch(args):
    d, state = need_state(args)
    tasks = load_tasks(d)
    found = []
    for m in state["members"]:
        if m["name"] == "main":
            continue
        why = stalled(m)
        if not why:
            continue
        now = tasks.get(m["name"], {}).get("now", "")
        item = {"name": m["name"], "error": why, "task": now, "nudged": False}
        if args.nudge and now:
            item["via"] = deliver(d, state, m, "[from crew-watch] " + NUDGE % now)
            item["nudged"] = True
        found.append(item)
    done(group=state["group"], stalled=found)


def live_model(m):
    """Model shown in a Codex pane's footer (e.g. 'GPT-6.2-Astra xhigh'), or None."""
    if m["agent"] != "codex" or not alive(m["session"]):
        return None
    rc, out = capture(m["session"], 8)
    hits = re.findall(r"(GPT-[\w.\-]+)\s+(low|medium|high|xhigh|max)", out or "")
    return ("%s %s" % hits[-1]) if hits else None


def cmd_board(args):
    d, state = need_state(args)
    tasks = load_tasks(d)
    rows = []
    for m in state["members"]:
        t = tasks.get(m["name"], {})
        live = live_model(m)
        drift = bool(live and m.get("model") and m["model"].replace("gpt-", "").lower()
                     not in live.lower().replace("gpt-", ""))
        rows.append({"name": m["name"], "agent": m["agent"], "model": m.get("model"),
                     "live_model": live, "model_changed": drift,
                     "state": busy_state(m), "now": t.get("now", ""), "next": t.get("next", []),
                     "updated": t.get("updated", "")})
    q = {}
    if not args.no_quota:
        try:
            q = advise.quota(sorted({r["agent"] for r in rows if installed(r["agent"])}),
                             installed=installed)
        except Exception:
            q = {}
    for r in rows:
        b = advise.bottleneck(r["agent"], r["model"], q) if q else None
        r["quota"] = {"remaining": b["remaining"], "label": b["label"],
                      "resets": b.get("resets")} if b else None
    if not args.text:
        done(group=state["group"], dir=d, members=rows, flow=load_flow(d).get("steps"),
             quota=q or None)
        return
    print("%s（%s）" % (state["group"], d))
    for r in rows:
        qs = ""
        if r["quota"]:
            qs = " · 额度 %.0f%%%s" % (r["quota"]["remaining"],
                                       " ⚠" if r["quota"]["remaining"] < 20 else "")
        print("\n● %s  [%s · %s %s%s]  %s" % (r["name"], r["state"], r["agent"], r["model"] or "",
                                              qs, ("更新于 " + r["updated"]) if r["updated"] else "未登记任务"))
        if r["model_changed"]:
            print("  ⚠ 模型被换了：配置 %s，窗格里是 %s" % (r["model"], r["live_model"]))
        print("  现在：%s" % (r["now"] or "—"))
        for i, n in enumerate(r["next"], 1):
            print("  排期 %d：%s" % (i, n))
    print_flow(load_flow(d))
    if q:
        print("\n剩余额度（本机读取）")
        for a in sorted(q):
            for p in q[a].get("pools", []):
                print("  %3.0f%%  %s%s" % (p["remaining"], p["label"],
                                          ("（%s 重置）" % local_time(p["resets"])) if p.get("resets") else ""))


def local_time(iso):
    try:
        import datetime
        t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
        return t.strftime("%m-%d %H:%M")
    except Exception:
        return iso


def cmd_read(args):
    d, state = need_state(args)
    m = member(state, args.name)
    if not m:
        die("没有成员 " + args.name)
    rc, out = capture(m["session"], args.lines)
    if rc != 0:
        die("%s 不在 tmux 中，无法读取。" % m["name"])
    print("\n".join(l for l in out.splitlines() if l.strip()))


def refresh_ids(state, who):
    changes = []
    for m in state["members"]:
        new = None
        if alive(m["session"]):
            new = live_session_id(m)
        elif m["name"] == "main" and who == "main":
            new = calling_session_id(*calling_agent())
        if new and new != m.get("session_id"):
            changes.append({"name": m["name"], "old": m.get("session_id"), "new": new})
            m["session_id"] = new
    return changes


def cmd_status(args):
    d, state = need_state(args)
    rows = []
    for m in state["members"]:
        up = alive(m["session"])
        rows.append({"name": m["name"], "agent": m["agent"], "model": m.get("model"),
                     "effort": m.get("effort"), "session": m["session"], "in_tmux": up,
                     "tty": client_tty(m["session"]) if up else None,
                     "saved_session_id": m.get("session_id"),
                     "live_session_id": live_session_id(m) if up else None})
    done(group=state["group"], dir=d, members=rows)


def cmd_whoami(args):
    d = find_dir(args.dir)
    state = load(d)
    who, sess, tty = caller(state, state["group"] if state else group_name(d))
    agent, pid = calling_agent()
    done(name=who, agent=agent, pid=pid, session_id=calling_session_id(agent, pid),
         tmux_session=sess, tty=tty, group=state["group"] if state else None,
         group_file=os.path.join(d, STATE) if state else None,
         note=("这个目录还没有建组，建组后调用方会成为 main。" if not state else
               GUEST % (state["group"], member(state, "main")["agent"], os.path.join(d, STATE))
               if who == "guest" else None))


def cmd_save(args):
    d, state = need_state(args)
    who = caller(state, state["group"])[0]
    sync_main(state, who, args, d)
    changes = refresh_ids(state, who)
    store(d, state)
    launcher = os.path.join(d, state["group"] + "-crew.command")
    with open(launcher, "w") as f:
        f.write('''#!/bin/zsh
# 双击恢复「%s」agent 组的 iTerm2 窗口。成员、模型、effort、会话 ID 记在同目录的 %s。
emulate -LR zsh
path+=("$HOME/.local/bin" /opt/homebrew/bin /usr/local/bin /Library/Frameworks/Python.framework/Versions/Current/bin)
exec python3 %s restore --dir "${0:A:h}"
''' % (state["group"], STATE, dq(os.path.abspath(__file__))))
    os.chmod(launcher, 0o755)
    missing = [m["name"] for m in state["members"] if not m.get("session_id")]
    done(state_file=os.path.join(d, STATE), launcher=launcher, updated=changes,
         members=[{k: m.get(k) for k in ("name", "agent", "model", "effort", "session_id")}
                  for m in state["members"]],
         missing_session_id=missing,
         note="没有会话 ID 的成员恢复时会开新对话。" if missing else None)


def cmd_restore(args):
    d = os.path.abspath(args.dir)
    state = load(d)
    if not state:
        die("%s 里没有 %s。" % (d, STATE))
    main = member(state, "main")

    tty = client_tty(main["session"])
    if tty and osa(FOCUS, tty) == "OK":
        done(action="focused", note="该组的窗口已打开，已切换过去。")
        return
    if main.get("session_id") and not alive(main["session"]):
        pid = session_running(main["agent"], main["session_id"])
        if pid and not args.force:
            die("main 的对话仍在另一个不在 tmux 里的 %s 进程中运行（pid %d）。"
                "先退出那个窗口，再恢复；否则同一对话会被两个进程同时写入。" % (main["agent"], pid))

    opened = []
    for m in state["members"]:
        cmd = pane_command(m["session"], d, agent_argv(m, resume=True))
        if m["name"] == "main":
            osa(WINDOW, cmd)
        else:
            src = member(state, (m.get("split") or {}).get("from", "main")) or main
            src_tty = client_tty(src["session"]) or client_tty(main["session"])
            if not src_tty or osa(SPLIT, src_tty, (m.get("split") or {}).get("dir", "v"), cmd) == "NOTFOUND":
                opened.append({"name": m["name"], "ok": False})
                continue
        for _ in range(30):
            if client_tty(m["session"]):
                break
            time.sleep(0.5)
        opened.append({"name": m["name"], "ok": bool(client_tty(m["session"])),
                       "resumed": bool(m.get("session_id"))})
    for m in state["members"]:
        # a restarted agy has a new language server: the recorded address is stale
        if m["agent"] == "agy" and m["name"] != "main" and alive(m["session"]) \
                and not agy_creds(m):
            if wait_ready(m["session"]) == "ready":
                type_when_clear(m, REREGISTER % dq(os.path.abspath(__file__)))
    tty = client_tty(main["session"])
    if tty:
        osa(FOCUS, tty)
    done(action="restored", members=opened)


# ---------- panel: anonymous multi-round review ----------
# <project>/.crew/panel/<id>/
#   panel.json            round counter + member -> letter map (main must not read it early)
#   topic.md
#   drafts/<member>/      what each member writes (1-position.md, 2-review.md, 3-final.md)
#   board/<round>/<X>.md  the same files, published under the member's letter
#   map.md                main's synthesis: consensus, live disagreements, minority positions

PANEL_DIR = os.path.join(".crew", "panel")
ROUNDS = [("positions", "1-position.md", "独立立场"),
          ("reviews", "2-review.md", "互评"),
          ("final", "3-final.md", "修正")]


def panel_load(d, pid):
    base = os.path.join(d, PANEL_DIR)
    if pid:
        roots = [os.path.join(base, pid)]
    else:
        roots = sorted(glob.glob(os.path.join(base, "*")),
                       key=lambda r: os.path.getmtime(r) if os.path.isdir(r) else 0)[-1:]
    for root in roots:
        try:
            with open(os.path.join(root, "panel.json")) as f:
                return root, json.load(f)
        except Exception:
            pass
    die("没有找到评议（%s）。先运行 panel start。" % (pid or "尚未开始过"))


def panel_store(root, p):
    path = os.path.join(root, "panel.json")
    with open(path + ".tmp", "w") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(path + ".tmp", path)


def draft_path(root, name, rnd):
    return os.path.join(root, "drafts", name, ROUNDS[rnd][1])


def board_dir(root, rnd):
    return os.path.join(root, "board", ROUNDS[rnd][0])


def submitted(path):
    """Non-empty and untouched for a few seconds, so a file mid-write does not count."""
    try:
        st = os.stat(path)
    except OSError:
        return False
    return st.st_size > 0 and time.time() - st.st_mtime > 3


def panel_prompt(root, p, pm, rnd):
    head = "[crew panel %s] 第 %d 轮 · %s。" % (p["id"], rnd + 1, ROUNDS[rnd][2])
    out = draft_path(root, pm["name"], rnd)
    tail = "写完后在本窗格回复“已提交”，不要给组员发消息。"
    if rnd == 0:
        return (head + "议题见 %s 。请独立思考，把你自己的立场写成 Markdown 保存到 %s 。"
                "这一轮不要读取其他组员的窗格或文件，也不要和组员讨论。"
                "之后会匿名公开，文中不要透露你是哪个模型、叫什么名字。"
                "建议包含：核心判断、理由和证据、你最不确定的地方、什么证据会让你改主意。"
                % (os.path.join(root, "topic.md"), out) + tail)
    if rnd == 1:
        return (head + "所有立场已匿名公开在 %s ，你的是 %s.md。读完其他每一份，把评议保存到 %s 。"
                "对每一份分别写：最强的反对意见、值得借鉴的点；最后写你仍然不同意的地方。"
                "只按论据评判，不要统计有多少份持同一观点，不要猜测或提及作者身份，也不要透露自己的身份。"
                % (board_dir(root, 0), pm["alias"], out) + tail)
    return (head + "所有评议已匿名公开在 %s （文件名是评议者的代号，你的立场代号是 %s）。"
            "读完后把最终立场保存到 %s 。开头写“变更说明”：逐条列出改了什么、是哪条论据让你改的；"
            "以及哪些反对意见你听了仍然坚持、理由是什么。完全不改也可以，但要写明理由。"
            "只因论据改变立场，不因持某观点的人多。变更说明之后写完整的最终立场。"
            % (board_dir(root, 1), pm["alias"], out) + tail)


def panel_send(state, root, p, rnd):
    failed = []
    d = os.path.dirname(os.path.dirname(os.path.dirname(root)))  # <d>/.crew/panel/<id>
    for pm in p["members"]:
        if pm["name"] == "main":
            continue  # main takes part via --with-main; its task is returned in the report
        m = member(state, pm["name"])
        if m and alive(m["session"]):
            deliver(d, state, m, panel_prompt(root, p, pm, rnd))
        else:
            failed.append(pm["name"])
    return failed


def panel_progress(root, p):
    rnd = p["round"]
    if rnd >= len(ROUNDS):
        return []
    return [{"name": pm["name"], "submitted": submitted(draft_path(root, pm["name"], rnd))}
            for pm in p["members"]]


def panel_report(root, p, **kw):
    rnd = p["round"]
    rows = panel_progress(root, p)
    mine = [pm for pm in p["members"] if pm["name"] == "main"]
    if mine and rnd < len(ROUNDS):
        kw["main_task"] = panel_prompt(root, p, mine[0], rnd)
    done(id=p["id"], dir=root,
         round=rnd + 1 if rnd < len(ROUNDS) else None,
         phase=ROUNDS[rnd][2] if rnd < len(ROUNDS) else "汇总",
         members=rows, all_submitted=all(r["submitted"] for r in rows), **kw)


def need_main(state):
    who = caller(state, state["group"])[0]
    if who != "main":
        die("评议由 main 主持，%s 是参评成员，不能执行这个命令。" % who)


def cmd_panel_start(args):
    d, state = need_state(args)
    need_main(state)
    if args.topic_file:
        with open(args.topic_file) as f:
            topic = f.read()
    else:
        topic = args.topic
    if not topic or not topic.strip():
        die("需要 --topic 或 --topic-file。")
    names = ([n.strip() for n in args.members.split(",") if n.strip()] if args.members
             else [m["name"] for m in state["members"] if m["name"] != "main"])
    if args.with_main and "main" not in names:
        names.append("main")
    for n in names:
        m = member(state, n)
        if not m:
            die("没有成员 " + n)
        if n != "main" and not alive(m["session"]):
            die("%s 不在 tmux 中，无法参加评议。" % n)
    if len(set(names)) != len(names) or len(names) < 2:
        die("评议至少需要 2 个不重复的成员（建议 3 个以上）。当前：%s" % ("、".join(names) or "无"))
    if len(names) > 26:
        die("最多 26 个成员。")
    pid = args.id or time.strftime("%Y%m%d-%H%M%S")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", pid):
        die("评议 ID 只能用字母、数字、点、下划线、连字符：" + pid)
    root = os.path.join(d, PANEL_DIR, pid)
    if os.path.exists(root):
        die("评议 %s 已存在。" % pid)
    letters = [chr(ord("A") + i) for i in range(len(names))]
    random.SystemRandom().shuffle(letters)
    p = {"id": pid, "created": time.strftime("%Y-%m-%d %H:%M:%S"), "round": 0, "dropped": [],
         "members": [{"name": n, "alias": a} for n, a in zip(names, letters)]}
    for n in names:
        os.makedirs(os.path.join(root, "drafts", n))
    with open(os.path.join(root, "topic.md"), "w") as f:
        f.write(topic.rstrip() + "\n")
    panel_store(root, p)
    failed = panel_send(state, root, p, 0)
    panel_report(root, p, not_delivered=failed,
                 next="panel wait 等全部提交，然后 panel next 公开并进入互评。")


def cmd_panel_status(args):
    d, state = need_state(args)
    root, p = panel_load(d, args.id)
    panel_report(root, p)


def cmd_panel_wait(args):
    d, state = need_state(args)
    root, p = panel_load(d, args.id)
    t0 = time.time()
    while time.time() - t0 < args.timeout:
        if all(r["submitted"] for r in panel_progress(root, p)):
            break
        time.sleep(5)
    panel_report(root, p)


def cmd_panel_next(args):
    d, state = need_state(args)
    need_main(state)
    root, p = panel_load(d, args.id)
    rnd = p["round"]
    if rnd >= len(ROUNDS):
        die("三轮已结束。读 %s 写 map.md，然后 panel reveal。" % board_dir(root, 2))
    pending = [r["name"] for r in panel_progress(root, p) if not r["submitted"]]
    if pending:
        if not args.force:
            die("还没提交：%s。等它们写完；确定要放弃这些成员就加 --force。" % "、".join(pending))
        if len(p["members"]) - len(pending) < 2:
            die("加 --force 后剩余成员不足 2 个，无法继续。")
        p["dropped"] += [{"name": n, "round": rnd + 1} for n in pending]
        p["members"] = [pm for pm in p["members"] if pm["name"] not in pending]
    out = board_dir(root, rnd)
    os.makedirs(out, exist_ok=True)
    for pm in p["members"]:
        shutil.copyfile(draft_path(root, pm["name"], rnd), os.path.join(out, pm["alias"] + ".md"))
    p["round"] = rnd + 1
    panel_store(root, p)
    if p["round"] < len(ROUNDS):
        failed = panel_send(state, root, p, p["round"])
        panel_report(root, p, published=out, dropped=pending, not_delivered=failed)
        return
    done(id=p["id"], dir=root, phase="汇总", published=out, dropped=pending,
         read=[board_dir(root, 0), board_dir(root, 1), out],
         write=os.path.join(root, "map.md"),
         next="只读 board/ 下的匿名文件，写出 map.md，然后 panel reveal 揭晓代号。")


def cmd_panel_reveal(args):
    d, state = need_state(args)
    need_main(state)
    root, p = panel_load(d, args.id)
    if not args.force and not submitted(os.path.join(root, "map.md")):
        die("还没有 %s。先完成汇总再揭晓，避免身份影响判断。" % os.path.join(root, "map.md"))
    rows = []
    for pm in sorted(p["members"], key=lambda x: x["alias"]):
        m = member(state, pm["name"]) or {}
        rows.append({"alias": pm["alias"], "name": pm["name"], "agent": m.get("agent"),
                     "model": m.get("model"), "effort": m.get("effort")})
    done(id=p["id"], dir=root, authors=rows, dropped=p.get("dropped", []))


def main():
    p = argparse.ArgumentParser(prog="crew")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("models", help="top 2 models of each installed CLI, with remaining quota")
    s.add_argument("--all", action="store_true", help="every model, not just the first two per CLI")
    s.add_argument("--no-quota", action="store_true")
    s.set_defaults(fn=cmd_models)

    s = sub.add_parser("quota", help="remaining quota per CLI (local reads only)")
    s.add_argument("--agent", choices=AGENTS)
    s.add_argument("--refresh", action="store_true", help="ignore the 10-minute cache")
    s.set_defaults(fn=cmd_quota)

    s = sub.add_parser("advise", help="recommend a model for a task type")
    s.add_argument("--task", required=True)
    s.add_argument("--effort", default="high")
    s.add_argument("--top", type=int, default=6)
    s.add_argument("--all", action="store_true", help="consider every model, not only the menu")
    s.add_argument("--verbose", action="store_true", help="list every candidate")
    s.set_defaults(fn=cmd_advise)

    s = sub.add_parser("rankings", help="show, or import, the leaderboard snapshot used by advise")
    s.add_argument("action", nargs="?", choices=["status", "show", "import", "schema"], default="status")
    s.add_argument("file", nargs="?", help="import: the JSON file; show: one category key")
    s.set_defaults(fn=cmd_rankings)

    s = sub.add_parser("doctor", help="check dependencies, model lists, quota sources, config")
    s.add_argument("--refresh", action="store_true")
    s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("spawn", help="open a new agent in a split pane")
    s.add_argument("--name", required=True)
    s.add_argument("--agent", required=True, choices=["claude", "codex", "agy"])
    s.add_argument("--model", required=True)
    s.add_argument("--effort", default="high")
    s.add_argument("--sandbox", action="store_true",
                   help="codex only: keep the default sandbox (then it cannot reach tmux)")
    s.add_argument("--from", dest="split_from", help="member whose pane to split")
    s.add_argument("--split", choices=["v", "h"])
    s.add_argument("--main-model", help="model id of the calling main agent")
    s.add_argument("--main-effort", help="effort of the calling main agent")
    s.add_argument("--here", action="store_true",
                   help="use this directory's group even if a parent directory has one")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_spawn)

    s = sub.add_parser("send", help="message another member")
    s.add_argument("--to", required=True)
    s.add_argument("message")
    s.add_argument("--typed", action="store_true", help=argparse.SUPPRESS)  # 1.4.0, now a no-op
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_send)

    s = sub.add_parser("flush", help=argparse.SUPPRESS)  # detached deliverer of queued messages
    s.add_argument("--to", required=True)
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_flush)

    s = sub.add_parser("read", help="print a member's pane")
    s.add_argument("--name", required=True)
    s.add_argument("--lines", type=int, default=80)
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_read)

    s = sub.add_parser("status")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("task", help="record what you (or, for main, another member) are doing now and next")
    s.add_argument("--for", dest="for_", metavar="NAME", help="main only: set another member's tasks")
    s.add_argument("--now", help="current task, one line")
    s.add_argument("--next", action="append", default=[], help="a scheduled task; repeat for several")
    s.add_argument("--done", action="store_true", help="current task finished: clear 'now'")
    s.add_argument("--clear-next", action="store_true", help="drop the scheduled list before adding --next")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_task)

    s = sub.add_parser("flow", help="the group's workflow chain shown on board (main edits)")
    s.add_argument("--add", action="append", default=[], metavar="STEP[@MEMBER]",
                   help="append a step, optionally with its owner; repeat for several")
    s.add_argument("--status", nargs=2, metavar=("N", "STATUS"), help="todo / doing / done / blocked")
    s.add_argument("--remove", type=int, metavar="N")
    s.add_argument("--clear", action="store_true", help="drop all steps before --add")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_flow)

    s = sub.add_parser("watch", help="find members stopped at their prompt after a connection error")
    s.add_argument("--nudge", action="store_true", help="send each stalled member a 'continue' message")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_watch)

    s = sub.add_parser("board", help="every member: busy or idle, current and scheduled tasks")
    s.add_argument("--text", action="store_true", help="a readable table instead of JSON")
    s.add_argument("--no-quota", action="store_true", help="skip the remaining-quota column")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_board)

    s = sub.add_parser("save", help="refresh session ids, write the .command launcher")
    s.add_argument("--main-model")
    s.add_argument("--main-effort")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_save)

    s = sub.add_parser("whoami", help="which agent is calling, and its session id")
    s.add_argument("--dir", default=os.getcwd())
    s.set_defaults(fn=cmd_whoami)

    s = sub.add_parser("restore", help="reopen the group's iTerm2 window")
    s.add_argument("--dir", default=os.getcwd())
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_restore)

    s = sub.add_parser("panel", help="anonymous multi-round review among members")
    ps = s.add_subparsers(dest="panel_cmd", required=True)
    q = ps.add_parser("start", help="open a panel and ask for independent positions")
    q.add_argument("--topic")
    q.add_argument("--topic-file")
    q.add_argument("--members", help="comma-separated; default: every member except main")
    q.add_argument("--with-main", action="store_true",
                   help="main also takes part under a random letter, writing drafts/main/")
    q.add_argument("--id", help="default: timestamp")
    q.set_defaults(fn=cmd_panel_start)
    q = ps.add_parser("status")
    q.set_defaults(fn=cmd_panel_status)
    q = ps.add_parser("wait", help="block until everyone submitted this round, or timeout")
    q.add_argument("--timeout", type=int, default=540)
    q.set_defaults(fn=cmd_panel_wait)
    q = ps.add_parser("next", help="publish this round anonymously and start the next")
    q.add_argument("--force", action="store_true", help="drop members who have not submitted")
    q.set_defaults(fn=cmd_panel_next)
    q = ps.add_parser("reveal", help="letter -> member map, once map.md is written")
    q.add_argument("--force", action="store_true")
    q.set_defaults(fn=cmd_panel_reveal)
    for q in ps.choices.values():
        if q.get_default("fn") is not cmd_panel_start:
            q.add_argument("--id", help="default: the most recent panel")
        q.add_argument("--dir", default=os.getcwd())

    args = p.parse_args()
    if args.fn is not cmd_flush:
        register_agy(args)
    args.fn(args)


if __name__ == "__main__":
    main()
