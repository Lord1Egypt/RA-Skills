"""Quota, rankings and model advice for crew.

Everything here is read-only and local:
  - quota comes from files the CLIs already keep (Codex session logs, Claude Code's
    /usage cache) or from the CLI's own status line (agy), launched in a hidden
    terminal without sending any prompt;
  - rankings come from a file the user (or their main agent) writes, so this module
    never makes a network request.
Any source that cannot be read or has an unrecognised format is reported as unknown;
callers must never block on it. Set CREW_NO_QUOTA=1 to switch all quota reads off.
"""
import datetime as dt
import fcntl
import glob
import json
import os
import pty
import re
import select
import shlex
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time

HOME = os.path.expanduser("~")
CONFIG = os.path.join(os.environ.get("XDG_CONFIG_HOME") or os.path.join(HOME, ".config"), "crew")
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.join(HOME, ".cache"), "crew")
RANKINGS = os.path.join(CONFIG, "rankings.json")
ROLES = os.path.join(CONFIG, "roles.json")
QUOTA_CACHE = os.path.join(CACHE, "quota.json")
DEFAULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "defaults.json")
QUOTA_TTL = 600          # seconds a quota reading is reused
PROBE_TIMEOUT = 20       # seconds to wait for a CLI to render its usage
RANKINGS_MAX_AGE = 30    # days before rankings.json is reported as stale


# ---------- small helpers ----------

def now():
    return time.time()


def iso(epoch):
    return dt.datetime.fromtimestamp(epoch, dt.timezone.utc).isoformat(timespec="seconds")


def parse_time(v):
    """ISO string or epoch seconds -> epoch seconds; None when absent or nonsensical."""
    if v is None or v == "":
        return None
    try:
        if isinstance(v, (int, float)):
            t = float(v)
        else:
            t = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError, OverflowError):
        return None
    return t if t > 946684800 else None   # 1970 placeholders etc. mean "unknown"


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def write_json(path, data):
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def pool(pid, label, remaining, resets, at, source, scope=None):
    """remaining: percent left (0-100). A window that has already reset counts as full."""
    r = parse_time(resets)
    if r and r < now():
        remaining = 100.0
    return {"pool": pid, "label": label, "remaining": round(max(0.0, min(100.0, remaining)), 1),
            "resets": iso(r) if r else None, "at": iso(at) if at else None,
            "source": source, "scope": scope}


ANSI = re.compile(r"\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(\x07|\x1b\\\\)|\x1b[()][0-9A-Za-z]")
TRUST = re.compile(r"trust\s+(this\s+folder|the\s+contents|this\s+directory|the\s+files)", re.I)


def run_in_terminal(argv, check, timeout=PROBE_TIMEOUT, cwd=None, idle=None):
    """Start an interactive CLI on a hidden pseudo-terminal and read its result with
    check(). No prompt is typed. check() is polled while it runs; with `idle`, the CLI
    is stopped once its screen has been quiet that many seconds (some CLIs only save
    on exit), and check() runs once more after it has stopped."""
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
    try:
        proc = subprocess.Popen(argv, stdin=slave, stdout=slave, stderr=slave, cwd=cwd,
                                start_new_session=True,
                                preexec_fn=lambda: fcntl.ioctl(0, termios.TIOCSCTTY, 0),
                                env=dict(os.environ, TERM="xterm-256color"))
    except OSError:
        os.close(master)
        os.close(slave)
        return None
    os.close(slave)
    screen, presses, last = "", 0, None
    try:
        end, nxt = time.monotonic() + timeout, 0
        while time.monotonic() < end and proc.poll() is None:
            if time.monotonic() >= nxt:
                got = check()
                if got:
                    return got
                nxt = time.monotonic() + 0.5
            if idle and last and time.monotonic() - last > idle:
                break
            if select.select([master], [], [], 0.25)[0]:
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    break
                last = time.monotonic()
                screen = (screen + ANSI.sub(" ", chunk.decode("utf-8", "replace")))[-8000:]
                # The probe runs in crew's own empty cache folder; the first time a CLI
                # sees it, it asks whether to trust it. Move to "Yes" and confirm.
                if presses < 4 and TRUST.search(screen):
                    time.sleep(0.8)            # let the menu take keyboard input
                    while select.select([master], [], [], 0.1)[0]:
                        try:
                            screen += ANSI.sub(" ", os.read(master, 65536).decode("utf-8", "replace"))
                        except OSError:
                            break
                    sel = re.findall(r"[❯>›]\s*(Yes|No)\b", screen)
                    yes = bool(sel) and sel[-1] == "Yes"
                    os.write(master, b"\r" if yes else b"\x1b[B")
                    presses += 1
                    if yes:
                        screen = ""
                    last = None
    finally:
        os.close(master)
        stop(proc)
    return check()


def stop(proc):
    for sig, wait in ((signal.SIGTERM, 3), (signal.SIGKILL, 2)):
        try:
            os.killpg(proc.pid, sig)
            proc.wait(timeout=wait)
            return
        except (ProcessLookupError, PermissionError):
            return
        except subprocess.TimeoutExpired:
            continue


def probe_dir():
    d = os.path.join(CACHE, "probe")
    os.makedirs(d, mode=0o700, exist_ok=True)
    return d


# ---------- Codex: rate_limits events in the local session logs ----------

def codex_window(minutes):
    if not num(minutes):
        return "窗口"
    if minutes % 10080 == 0:
        return "周" if minutes == 10080 else "%d 周" % (minutes // 10080)
    if minutes % 1440 == 0:
        return "%d 天" % (minutes // 1440)
    return "%g 小时" % (minutes / 60.0)


def codex_quota():
    base = os.path.join(os.environ.get("CODEX_HOME") or os.path.join(HOME, ".codex"), "sessions")
    files = sorted(glob.glob(os.path.join(base, "*", "*", "*", "rollout-*.jsonl")),
                   key=lambda p: os.path.getmtime(p), reverse=True)[:8]
    if not files:
        return [], "没有找到 Codex 会话记录（%s）。用 Codex 说一句话后再试。" % base
    best, best_at = None, 0
    for path in files:
        try:
            with open(path, "rb") as f:
                f.seek(0, 2)
                f.seek(max(0, f.tell() - 4 * 1024 * 1024))
                lines = f.read().splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            if b'"rate_limits"' not in line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            p = ev.get("payload") or {}
            rl = p.get("rate_limits") or {}
            if p.get("type") != "token_count" or rl.get("limit_id") not in ("codex", None):
                continue
            at = parse_time(ev.get("timestamp")) or os.path.getmtime(path)
            if at > best_at:
                best, best_at = rl, at
            break
        if best:
            break   # files are newest first
    if not best:
        return [], "Codex 会话记录里没有可识别的额度事件（CLI 格式可能已变）。"
    rows = []
    for key in ("primary", "secondary"):
        w = best.get(key)
        if isinstance(w, dict) and num(w.get("used_percent")):
            rows.append(pool("codex-" + key, "Codex %s额度" % codex_window(w.get("window_minutes")),
                             100 - w["used_percent"], w.get("resets_at"), best_at,
                             "Codex 会话记录"))
    note = "读取最近一次 Codex 会话里的额度事件。"
    if best.get("plan_type"):
        note += "套餐：%s。" % best["plan_type"]
    return rows, note


# ---------- Claude Code: the /usage cache in ~/.claude.json ----------

CLAUDE_KIND = {"session": ("claude-5h", "Claude 5 小时额度"),
               "weekly_all": ("claude-weekly", "Claude 全模型周额度")}


def claude_cache():
    cfg_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    conf = read_json(os.path.join(cfg_dir, ".claude.json")) if cfg_dir else None
    conf = conf or read_json(os.path.join(HOME, ".claude.json"), {})
    cache = conf.get("cachedUsageUtilization") or {}
    owner = (conf.get("oauthAccount") or {}).get("accountUuid")
    if not cache or (owner and cache.get("accountUuid") not in (None, owner)):
        return [], None
    at = (cache.get("fetchedAtMs") or 0) / 1000.0 or None
    usage = cache.get("utilization") or {}
    rows = {}
    for item in usage.get("limits") or []:
        if not isinstance(item, dict) or not num(item.get("percent")):
            continue
        kind = item.get("kind")
        if kind in CLAUDE_KIND:
            pid, label = CLAUDE_KIND[kind]
            scope = None
        elif kind == "weekly_scoped":
            m = ((item.get("scope") or {}).get("model") or {})
            name = m.get("display_name") or m.get("id") or ""
            if not name:
                continue
            scope = name.lower()
            pid, label = "claude-weekly-" + re.sub(r"[^a-z0-9]+", "-", scope), "Claude %s 周额度" % name
        else:
            continue
        rows[pid] = pool(pid, label, 100 - item["percent"], item.get("resets_at"), at,
                         "Claude Code /usage", scope)
    if not rows:   # older layout: five_hour / seven_day / seven_day_<model>
        for key, item in usage.items():
            if not isinstance(item, dict) or not num(item.get("utilization")):
                continue
            if key == "five_hour":
                pid, label, scope = "claude-5h", "Claude 5 小时额度", None
            elif key == "seven_day":
                pid, label, scope = "claude-weekly", "Claude 全模型周额度", None
            elif key.startswith("seven_day_"):
                scope = key[len("seven_day_"):]
                pid, label = "claude-weekly-" + scope, "Claude %s 周额度" % scope
            else:
                continue
            rows[pid] = pool(pid, label, 100 - item["utilization"], item.get("resets_at"), at,
                             "Claude Code /usage", scope)
    return list(rows.values()), at


def claude_quota(refresh):
    rows, at = claude_cache()
    if rows and at and now() - at < QUOTA_TTL and not refresh:
        return rows, "读取 Claude Code 的 /usage 缓存。"
    before = at or 0
    argv = ["claude", "--settings", '{"disableAllHooks":true}', "--strict-mcp-config",
            "--mcp-config", '{"mcpServers":{}}', "--tools", "", "--", "/usage"]

    def fresh():
        r, t = claude_cache()
        return r if r and t and t > before else None
    got = run_in_terminal(argv, fresh, cwd=probe_dir(), idle=4)
    if got:
        return got, "通过 Claude Code 的 /usage 刷新（不发送对话）。"
    if rows and at and now() - at < 180:
        return rows, "Claude Code 刚刷新过 /usage（3 分钟内不会重复拉取），使用该读数。"
    if rows:
        return rows, "刷新失败，显示上次 /usage 的缓存。"
    return [], ("读不到 Claude 额度。订阅账户在 Claude Code 里运行一次 /usage 后再试；"
                "API key 账户没有订阅额度。")


# ---------- agy: quota from its own status-line payload ----------

def agy_rows(payload, at):
    rows = []
    for key, e in (payload.get("quota") or {}).items():
        if not isinstance(e, dict) or e.get("disabled"):
            continue
        frac = e.get("remaining_fraction")
        if not (num(frac) and 0 <= frac <= 1):
            continue
        resets = e.get("reset_time")
        if not parse_time(resets) and num(e.get("reset_in_seconds")) and e["reset_in_seconds"] > 0:
            resets = at + e["reset_in_seconds"]
        if (parse_time(resets) or 0) <= at + 1:
            resets = None      # an untouched pool reports "resets now"
        group = key.rsplit("-", 1)[0]          # gemini-5h -> gemini, 3p-weekly -> 3p
        win = key.rsplit("-", 1)[-1]
        label = "agy %s %s额度" % ("Gemini" if group == "gemini" else "第三方模型" if group == "3p"
                                  else group, {"5h": "5 小时", "weekly": "周"}.get(win, win + " "))
        rows.append(pool("agy-" + key, label, frac * 100, resets, at, "agy 状态栏", group))
    return rows


def agy_quota(refresh):
    with tempfile.TemporaryDirectory(dir=probe_dir()) as tmp:
        dest = os.path.join(tmp, "quota.json")
        hook = shlex.join([sys.executable, os.path.abspath(__file__), "--agy-hook", dest])
        settings = {"statusLine": {"type": "command", "command": hook, "enabled": True}}
        got = run_in_terminal(["agy", "--settings", json.dumps(settings)],
                              lambda: read_json(dest), cwd=probe_dir())
    if got:
        return got, "读取 agy 状态栏返回的额度（不发送对话）。"
    return [], "agy 没有返回额度（未登录、版本不同或启动超时）。可在 agy 里用 /usage 核对。"


# ---------- all agents, cached ----------

SOURCES = {"codex": lambda refresh: codex_quota(),
           "claude": claude_quota,
           "agy": agy_quota}


def quota(agents=("codex", "claude", "agy"), refresh=False, installed=None):
    """{agent: {"pools": [...], "note": str, "checked": iso}}; never raises."""
    if os.environ.get("CREW_NO_QUOTA") == "1":
        return {a: {"pools": [], "note": "CREW_NO_QUOTA=1，已关闭额度读取。", "checked": None}
                for a in agents}
    cache = read_json(QUOTA_CACHE, {}) or {}
    out, dirty = {}, False
    for a in agents:
        c = cache.get(a)
        if c and not refresh and now() - c.get("_t", 0) < QUOTA_TTL:
            out[a] = c
            continue
        if installed is not None and not installed(a):
            out[a] = {"pools": [], "note": "未安装 %s。" % a, "checked": iso(now())}
            continue
        try:
            rows, note = SOURCES[a](refresh)
        except Exception as e:   # a CLI changed under us: report, don't break spawn
            rows, note = [], "读取 %s 额度出错：%s" % (a, e)
        out[a] = cache[a] = {"pools": rows, "note": note, "checked": iso(now()), "_t": now()}
        dirty = True
    if dirty:
        try:
            write_json(QUOTA_CACHE, cache)
        except OSError:
            pass
    return {a: {k: v for k, v in r.items() if k != "_t"} for a, r in out.items()}


def pools_for(agent, model, q):
    """The quota pools a member running `model` on `agent` draws from."""
    rows = (q.get(agent) or {}).get("pools") or []
    m = (model or "").lower()
    if agent == "agy":
        group = "gemini" if m.startswith("gemini") else "3p"
        return [r for r in rows if r.get("scope") == group]
    if agent == "claude":
        return [r for r in rows if not r.get("scope") or r["scope"] in m]
    return rows


def bottleneck(agent, model, q):
    ps = pools_for(agent, model, q)
    return min(ps, key=lambda r: r["remaining"]) if ps else None


# ---------- rankings and roles ----------

def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def split_variant(name):
    """'Gemini 4 Neon (xHigh)' -> ('gemini4neon', 'xhigh')"""
    m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", name or "")
    return (norm(m.group(1)), norm(m.group(2))) if m else (norm(name), None)


def version_key(name):
    """'Claude Opus 4.6 (High)' -> [4, 6]; 'GPT-6.2 Astra' -> [6, 2]"""
    head = re.sub(r"\(.*?\)", "", name or "")
    m = re.findall(r"\d+(?:\.\d+)*", head)
    return [int(x) for x in m[-1].split(".")] if m else []


def load_rankings():
    data = read_json(RANKINGS)
    if not isinstance(data, dict) or not isinstance(data.get("categories"), dict):
        return None
    return data


def rankings_status():
    data = load_rankings()
    if not data:
        return {"present": False, "path": RANKINGS, "stale": True}
    age = None
    t = parse_time(data.get("fetched"))
    if t:
        age = int((now() - t) // 86400)
    return {"present": True, "path": RANKINGS, "source": data.get("source"),
            "fetched": data.get("fetched"), "age_days": age,
            "stale": age is None or age > RANKINGS_MAX_AGE,
            "categories": {k: len(v) for k, v in data["categories"].items()
                           if isinstance(v, list)}}


def validate_rankings(data):
    errs = []
    if not isinstance(data, dict):
        return ["顶层必须是对象"]
    if not parse_time(data.get("fetched")):
        errs.append("缺少 fetched（ISO 日期，如 2026-11-24）")
    cats = data.get("categories")
    if not isinstance(cats, dict) or not cats:
        errs.append("categories 必须是非空对象")
        return errs
    for c, rows in cats.items():
        if not isinstance(rows, list):
            errs.append("%s 必须是数组" % c)
            continue
        for i, r in enumerate(rows):
            if not isinstance(r, dict) or not r.get("name") or not num(r.get("score")):
                errs.append("%s[%d] 需要 name 和数字 score" % (c, i))
            elif r.get("cost") is not None and not num(r.get("cost")):
                errs.append("%s[%d] 的 cost 必须是数字或省略" % (c, i))
    return errs


def _candidates(rows, agent, model):
    want = norm(model)
    if agent == "agy":
        want = norm(re.sub(r"-(low|medium|high|xhigh|max)$", "", model or ""))
    out = []
    for r in rows:
        base, var = split_variant(r.get("name"))
        if agent == "claude" and not re.search(r"\d", want):
            # an alias such as "fable" means the newest Claude model of that family
            ok = base.startswith("claude" + want) or base.startswith(want)
        else:
            ok = base == want or base == "claude" + want
        if ok:
            out.append((r, base, var))
    return out


def match_entry(rows, agent, model, effort, everywhere=None):
    """Best leaderboard row for this crew option, or None. For an alias (Claude's
    "fable"), only the newest version seen in `everywhere` (all categories) counts,
    so an older model never stands in for the one the alias actually starts."""
    hits = _candidates(rows, agent, model)
    if not hits:
        return None
    pool = _candidates(everywhere, agent, model) if everywhere else hits
    newest = max(version_key(h[0]["name"]) for h in pool)
    hits = [h for h in hits if version_key(h[0]["name"]) == newest]
    if not hits:
        return None
    same = [h for h in hits if h[2] == norm(effort)]
    return max(same or hits, key=lambda h: h[0]["score"])[0]


def all_rows(ranks):
    return [r for rows in (ranks.get("categories") or {}).values() if isinstance(rows, list)
            for r in rows]


def load_roles():
    base = read_json(DEFAULTS, {}) or {}
    user = read_json(ROLES, {}) or {}
    tasks = dict(base.get("tasks") or {})
    for k, v in (user.get("tasks") or {}).items():
        merged = dict(tasks.get(k) or {})
        merged.update(v or {})
        tasks[k] = merged
    policy = dict(base.get("policy") or {})
    policy.update(user.get("policy") or {})
    return {"tasks": tasks, "policy": policy, "user_file": ROLES,
            "user_present": os.path.exists(ROLES)}


def advise(task, options, q, roles=None):
    """Rank crew options for a task.

    Rule (Elo-based, explainable): among options with enough quota, every one whose
    leaderboard score is within `elo_margin` of the best is "good enough"; the cheapest
    of those is recommended. The user's `prefer` list for the task goes first, `avoid`
    is dropped. Unknown quota or rank never removes an option, it only ranks it lower.
    """
    roles = roles or load_roles()
    pol = roles["policy"]
    margin = pol.get("elo_margin", 50)
    min_quota = pol.get("min_quota", 20)
    t = roles["tasks"].get(task)
    if t is None:
        return {"error": "未知任务类型 %s。可选：%s" % (task, "、".join(sorted(roles["tasks"])))}
    cats = t.get("arena") or []
    prefer = [norm(x) for x in t.get("prefer") or []]
    avoid = [norm(x) for x in (t.get("avoid") or []) + (pol.get("avoid_for_members") or [])]
    ranks = load_rankings() or {"categories": {}}
    everything = all_rows(ranks)

    rows = []
    for o in options:
        key = norm(o["model"])
        if any(a and a in key for a in avoid):
            continue
        effort = o.get("effort") or "high"
        hits, costs = {}, []
        for c in cats:
            e = match_entry(ranks["categories"].get(c) or [], o["agent"], o["model"], effort,
                            everything)
            if e:
                hits[c] = e
                if num(e.get("cost")):
                    costs.append(e["cost"])
        b = bottleneck(o["agent"], o["model"], q)
        rows.append({
            "agent": o["agent"], "model": o["model"], "label": o.get("label"), "effort": effort,
            "score": next((hits[c]["score"] for c in cats if c in hits), None),
            "cost": round(sum(costs) / len(costs), 2) if costs else None,
            "quota": b["remaining"] if b else None,
            "quota_pool": b["label"] if b else None,
            "preferred": any(p and p in key for p in prefer),
            "matched": ["%s:%s" % (c, e["name"]) for c, e in hits.items()], "_hits": hits})

    # gap = how far below the best usable candidate, per category, averaged over the
    # categories this candidate appears in (Elo scales differ between categories)
    usable = [r for r in rows if r["quota"] is None or r["quota"] >= min_quota]
    best = {c: max((r["_hits"][c]["score"] for r in usable if c in r["_hits"]), default=None)
            for c in cats}
    for r in rows:
        gaps = [best[c] - e["score"] for c, e in r.pop("_hits").items() if best.get(c) is not None]
        r["gap"] = round(sum(gaps) / len(gaps)) if gaps else None
        why = []
        if r["preferred"]:
            why.append("你为此任务指定的偏好")
        if r["quota"] is not None and r["quota"] < min_quota:
            r["tier"] = "额度不足"
            why.append("%s 只剩 %.0f%%" % (r["quota_pool"], r["quota"]))
        elif r["gap"] is None:
            r["tier"] = "无排名"
            why.append("未进入已记录的排名（多半在前列之外）" if cats else "此任务没有对应的排行分类，按你的偏好或自行判断")
        elif r["gap"] <= margin:
            r["tier"] = "够用"
            why.append("与最高分差 %d（≤ %d）" % (r["gap"], margin))
        else:
            r["tier"] = "较弱"
            why.append("与最高分差 %d" % r["gap"])
        r["why"] = "；".join(why)

    order = {"够用": 0, "较弱": 1, "无排名": 2, "额度不足": 3}

    def key(r):
        cost = r["cost"] if r["cost"] is not None else float("inf")
        return (0 if r["preferred"] and r["tier"] != "额度不足" else 1, order[r["tier"]],
                cost, r["gap"] if r["gap"] is not None else 0)
    rows.sort(key=key)
    rs = rankings_status()
    return {"task": task, "label": t.get("label"), "arena_categories": cats,
            "rule": "额度 ≥ %d%% 且与最高分相差 ≤ %d 的选项里选成本最低的；你的偏好优先；额度不足的排最后但仍列出" % (min_quota, margin),
            "pick": rows[0] if rows else None, "candidates": rows,
            "rankings": {"fetched": rs.get("fetched"), "stale": rs["stale"]}}


if __name__ == "__main__" and sys.argv[1:2] == ["--agy-hook"]:
    # agy calls this as its status-line command; the payload arrives on stdin
    os.umask(0o077)
    try:
        rows = agy_rows(json.load(sys.stdin), now())
        if rows:
            write_json(sys.argv[2], rows)
    except Exception:
        pass
    print("crew")
