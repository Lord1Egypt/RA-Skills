#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memory-orchestrator 会话状态：按对话框隔离的轮次计数、提前提醒、最近 checkpoint。

只记录：项目名/对话框标识/轮数/token 用量/提醒标记/时间戳/agent 归属。绝不记录对话正文。

token 触发（可选）：bump 时传 token_count=；轮数与 token 两个阈值互补，哪个先到先触发。
TURN_THRESHOLD/TURN_WARN_AT（默认 8/7）；TOKEN_THRESHOLD/TOKEN_WARN_AT（默认 150000/130000）。
本文件不发起任何网络调用。

不可写降级：主路径 $CODEX_HOME/memory/state.json 不可写时自动落到
$TMPDIR/memory-orchestrator/state.json（可用 CODEX_MEMORY_STATE_FALLBACK 覆盖），
并在输出 JSON 的 storage 字段标明 primary/fallback。
"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import i18n

try:
    import fcntl  # POSIX
except ImportError:
    fcntl = None
try:
    import msvcrt  # Windows
except ImportError:
    msvcrt = None

STATE = Path(os.environ.get("CODEX_MEMORY_STATE", Path.home() / ".codex" / "memory" / "state.json"))
DEFAULTS = {"active_project": "", "turn_count": 0, "last_checkpoint": "", "last_action": "", "updated_at": ""}
THRESHOLD = int(os.environ.get("TURN_THRESHOLD", "8"))
WARN_AT = int(os.environ.get("TURN_WARN_AT", "7"))
TOKEN_THRESHOLD = int(os.environ.get("TOKEN_THRESHOLD", "150000"))
TOKEN_WARN_AT = int(os.environ.get("TOKEN_WARN_AT", "130000"))
REQUEST_PEAK_THRESHOLD = int(os.environ.get("REQUEST_PEAK_THRESHOLD", "100000"))
REQUEST_COUNT_THRESHOLD = int(os.environ.get("REQUEST_COUNT_THRESHOLD", "120"))
INPUT_TOTAL_THRESHOLD = int(os.environ.get("INPUT_TOTAL_THRESHOLD", "8000000"))
AGENT_DEFAULT = os.environ.get("MEMORY_AGENT") or "codex"

STORAGE = {"path": str(STATE), "mode": "primary"}


def _state_fallback():
    p = os.environ.get("CODEX_MEMORY_STATE_FALLBACK")
    if p:
        return Path(p)
    return Path(tempfile.gettempdir()) / "memory-orchestrator" / "state.json"


def storage_path():
    """优先可用路径：已存在的主路径，或父目录可写的主路径；否则回退临时路径。"""
    candidates = [STATE, _state_fallback()]
    for p in candidates:
        try:
            if p.exists() or os.access(str(p.parent), os.W_OK):
                return p
        except OSError:
            continue
    return _state_fallback()


def _write_json(path, d):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    fd, tmp = tempfile.mkstemp(prefix=".state-", suffix=".json", dir=str(os.path.dirname(path)))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


def _dialog_key(active_project, thread_id, agent=None):
    """对话框唯一键：agent==codex 保持历史格式；其他 agent 加 @ 命名空间防碰撞。"""
    proj = active_project or "default"
    tid = thread_id or proj
    if agent and agent != "codex":
        return f"{proj}||{tid}||@{agent}"
    return f"{proj}||{tid}"


def _resolve_agent(kv, args=None):
    if isinstance(kv, dict) and kv.get("agent"):
        return kv["agent"]
    if getattr(args, "agent", None):
        return args.agent
    return os.environ.get("MEMORY_AGENT") or AGENT_DEFAULT


def load():
    d = dict(DEFAULTS)
    for p in [storage_path(), STATE, _state_fallback()]:
        if p.exists():
            try:
                with open(p, encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    for k, v in loaded.items():
                        d[k] = v
                break
            except Exception:
                continue
    d.setdefault("dialogs", {})
    d.setdefault("agents", {})
    if not isinstance(d["dialogs"], dict):
        d["dialogs"] = {}
    if not isinstance(d["agents"], dict):
        d["agents"] = {}
    return d


def save(d):
    global STORAGE
    target = storage_path()
    fallback = _state_fallback()
    try:
        _write_json(target, d)
        STORAGE = {"path": str(target), "mode": ("primary" if str(target) == str(STATE) else "fallback")}
    except (PermissionError, OSError):
        if str(target) == str(fallback):
            raise
        try:
            _write_json(fallback, d)
            STORAGE = {"path": str(fallback), "mode": "fallback"}
        except Exception as exc:
            raise OSError(f"状态文件不可写且降级路径写入失败: {exc}") from exc


class _StateLock:
    def __enter__(self):
        self.f = None
        lock_base = storage_path()
        lock_path = str(lock_base) + ".lock"
        if fcntl:
            os.makedirs(os.path.dirname(lock_path), exist_ok=True)
            self.f = open(lock_path, "a+")
            fcntl.flock(self.f.fileno(), fcntl.LOCK_EX)
        elif msvcrt:
            os.makedirs(os.path.dirname(lock_path), exist_ok=True)
            self.f = open(lock_path, "a+b")
            self.f.seek(0)
            msvcrt.locking(self.f.fileno(), msvcrt.LK_LOCK, 1)
        return self

    def __exit__(self, *exc):
        if self.f:
            try:
                if fcntl:
                    fcntl.flock(self.f.fileno(), fcntl.LOCK_UN)
                elif msvcrt:
                    self.f.seek(0)
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
            except Exception:
                pass
            try:
                self.f.close()
            except Exception:
                pass
        return False


def mark_alive(d, agent):
    agents = d.setdefault("agents", {})
    agents[agent] = {
        "agent_alive": True,
        "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return d


def cross_check(d, current_agent=None, threshold=THRESHOLD, warn_at=WARN_AT,
                token_threshold=TOKEN_THRESHOLD, token_warn_at=TOKEN_WARN_AT):
    """读共享注册表，列出其他 Agent 的超阈值/接近阈值对话框，以及未见存活标记的 Agent。

    只读他人的行；绝不改写 owner != 当前 agent 的记录。
    """
    current_agent = current_agent or AGENT_DEFAULT
    dialogs = d.get("dialogs") or {}
    others = []
    for key, s in dialogs.items():
        if not isinstance(s, dict):
            continue
        owner = s.get("owner") or s.get("agent") or "codex"
        if owner == current_agent:
            continue
        count = int(s.get("turn_count") or 0)
        toks = int(s.get("token_count") or s.get("tokens") or 0)
        if count < warn_at and toks < token_warn_at:
            continue
        parts = key.split("||", 2)
        metric = []
        if count >= threshold:
            metric.append("over_turns")
        elif count >= warn_at:
            metric.append("warn_turns")
        if toks >= token_warn_at:
            metric.append("over_tokens" if toks >= token_threshold else "warn_tokens")
        others.append({
            "agent": owner,
            "active_project": s.get("active_project") or parts[0],
            "thread_id": s.get("thread_id") or (parts[1] if len(parts) > 1 else key),
            "turn_count": count,
            "token_count": toks,
            "metric": "+".join(metric) or ("over" if count >= threshold else "warn"),
            "status": "over" if (count >= threshold or toks >= token_threshold) else "warn",
        })
    others.sort(key=lambda r: (r["agent"], r["status"] != "over", r["metric"]))

    known = d.get("agents") or {}
    suggest = [
        {"agent": name, "suggest_install": not bool(m.get("agent_alive"))}
        for name, m in known.items()
        if name != current_agent and isinstance(m, dict)
    ]
    suggest.sort(key=lambda s: s["agent"])
    return others, suggest


def _fmt_ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _attach_storage(out):
    out["storage"] = STORAGE.copy()
    return out


def main():
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    desc = ("memory-orchestrator state: get/set/bump/touch/cross-check (turn count only, no content)."
            if lang == "en" else "memory-orchestrator 状态：get/set/bump/touch/cross-check（只记轮数，不记内容）")
    ap = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("action", choices=["get", "set", "bump", "touch", "cross-check"])
    ap.add_argument("kv", nargs="*", help="key=value pairs, e.g. active_project=hotel agent=codex; bump accepts thread_id=xxx" if lang == "en" else "键值对，如 active_project=酒店 agent=codex。bump 支持 thread_id=xxx 标识对话框")
    ap.add_argument("--threshold", type=int, default=THRESHOLD, help="hard threshold (turns)" if lang == "en" else "硬阈值（轮）")
    ap.add_argument("--warn-at", type=int, default=None, help="advance warn line (turns), default threshold-1" if lang == "en" else "提前提醒线（轮），默认 threshold-1")
    ap.add_argument("--token-threshold", type=int, default=TOKEN_THRESHOLD, help="hard threshold (tokens)" if lang == "en" else "硬阈值（token）")
    ap.add_argument("--token-warn-at", type=int, default=None, help="advance warn line (tokens)" if lang == "en" else "提前提醒线（token），默认 token_threshold-20000")
    ap.add_argument("--thread-id", default=None, help="dialog identity" if lang == "en" else "对话框标识（同一活跃项目下隔离不同对话框）")
    ap.add_argument("--agent", default=None, help="agent name (default $MEMORY_AGENT or codex)" if lang == "en" else "Agent 名（默认 $MEMORY_AGENT 或 codex）")
    ap.add_argument("--json", action="store_true", help="also output JSON for cross-check" if lang == "en" else "cross-check 也输出 JSON（其他动作始终输出 JSON）")
    args = ap.parse_args(raw)
    warn_at = args.warn_at if args.warn_at is not None else max(1, args.threshold - 1)
    tok_warn_at = args.token_warn_at if args.token_warn_at is not None else max(1, args.token_threshold - 20000)

    kv = {}
    for s in args.kv:
        if "=" in s:
            k, v = s.split("=", 1)
            kv[k] = v

    project = kv.get("active_project", "")
    thread_id = kv.get("thread_id", args.thread_id or "")
    agent = _resolve_agent(kv, args)

    with _StateLock():
        d = load()
        if args.action == "get":
            print(json.dumps(d, ensure_ascii=False))
            return
        if args.action == "touch":
            d = mark_alive(d, agent)
            save(d)
            out = _attach_storage({"agent": agent, "agent_alive": True, "status": "ok",
                                   "message": (f"{agent} registered a local liveness marker for this skill" if lang == "en" else f"{agent} 已在本机登记本 Skill 存活标记")})
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return
        if args.action == "cross-check":
            others, suggest = cross_check(d, current_agent=agent, threshold=args.threshold, warn_at=warn_at,
                                          token_threshold=args.token_threshold, token_warn_at=tok_warn_at)
            out = _attach_storage({"agent": agent, "others": others, "suggest_install": suggest})
            # v1.9.2：原为 `if args.json or True` 恒真分支（else 不可达），已按实际行为简化为 JSON 输出
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return

        if args.action == "set":
            for k, v in kv.items():
                if k in ("active_project", "last_checkpoint", "last_action"):
                    d[k] = v
                elif k == "turn_count":
                    d["turn_count"] = int(v or 0)
                elif k == "token_count":
                    d["token_count"] = int(v or 0)
            if "turn_count" in kv or "token_count" in kv:
                skey = _dialog_key(d.get("active_project", project), thread_id, agent)
                dialogs = d.setdefault("dialogs", {})
                sc = dialogs.get(skey, {})
                sc.update({
                    "thread_id": thread_id or d.get("active_project") or project,
                    "active_project": d.get("active_project", project),
                    "agent": agent,
                    "owner": agent,
                    "turn_count": int(kv.get("turn_count") or sc.get("turn_count") or 0),
                    "token_count": int(kv.get("token_count") or sc.get("token_count") or 0),
                    "warned": bool(sc.get("warned")),
                    "forced": bool(sc.get("forced")),
                    "checked_at": _fmt_ts(),
                })
                dialogs[skey] = sc
            d = mark_alive(d, agent)
            save(d)
            out = _attach_storage({"agent": agent, "active_project": d.get("active_project", project), "ok": True,
                                   "status": "ok", "message": ("state recorded" if lang == "en" else "状态已记录")})
            print(json.dumps(out, ensure_ascii=False))
            return

        # bump：可传精确 turn_count；否则兼容旧行为 +1。token/请求/input 指标均来自本机实测。
        for k, v in kv.items():
            if k == "active_project":
                d["active_project"] = v
            elif k == "last_checkpoint":
                d["last_checkpoint"] = v
            elif k == "last_action":
                d["last_action"] = v
        project = d.get("active_project", "") or project
        key = _dialog_key(project, thread_id, agent)
        dialogs = d.setdefault("dialogs", {})
        cur = dialogs.get(key, {})
        exact_turn = "turn_count" in kv
        count = int(kv.get("turn_count") or 0) if exact_turn else int(cur.get("turn_count") or 0) + 1
        token_count = int(kv.get("token_count") or cur.get("token_count") or 0)
        request_peak = int(kv.get("request_peak") or cur.get("request_peak") or 0)
        request_count = int(kv.get("request_count") or cur.get("request_count") or 0)
        input_total = int(kv.get("input_total") or cur.get("input_total") or 0)
        tok_warn = tok_warn_at
        already_forced = bool(cur.get("forced"))
        reasons = []
        if count >= args.threshold:
            reasons.append("over_turns")
        if token_count >= args.token_threshold:
            reasons.append("over_tokens")
        if request_peak >= REQUEST_PEAK_THRESHOLD:
            reasons.append("over_request_peak")
        if request_count >= REQUEST_COUNT_THRESHOLD:
            reasons.append("over_requests")
        if input_total >= INPUT_TOTAL_THRESHOLD:
            reasons.append("over_input_total")
        cur = {
            "thread_id": thread_id or project,
            "active_project": project,
            "agent": agent,
            "owner": agent,
            "turn_count": count,
            "turn_count_source": "exact" if exact_turn else "increment",
            "token_count": token_count,
            "request_peak": request_peak,
            "request_count": request_count,
            "input_total": input_total,
            "gate_reasons": reasons,
            "forced_reasons": sorted(set(cur.get("forced_reasons") or []) | (set(reasons) if reasons else set())),
            "warned": bool(cur.get("warned")),
            "forced": already_forced or bool(reasons),
            "checked_at": _fmt_ts(),
        }
        dialogs[key] = cur
        d["active_project"] = project
        d["turn_count"] = count  # 兼容旧单对话字段
        d = mark_alive(d, agent)
        out = {
            "agent": agent, "thread_id": cur["thread_id"], "active_project": project,
            "turn_count": count, "token_count": token_count,
            "request_peak": request_peak, "request_count": request_count, "input_total": input_total,
            "gate_reasons": reasons, "forced_reasons": cur["forced_reasons"],
            "warned": False, "forced": False, "already_forced": False,
            "status": "ok", "message": "", "cross_check": {"others": [], "suggest_install": []},
        }
        metric = ("over" if count >= args.threshold else "warn_turns") if count >= warn_at else ""
        if token_count:
            metric = ("over_tokens" if token_count >= args.token_threshold else "warn_tokens") if token_count >= tok_warn else metric
        over_now = bool(reasons)
        warn_now = (not over_now) and (count >= warn_at or (token_count and token_count >= tok_warn))
        if over_now and not already_forced:
            cur["forced"] = True
            cur["warned"] = True
            out["warned"] = True
            out["forced"] = True
            labels = {
                "over_turns": f"{args.threshold} 轮",
                "over_tokens": f"{args.token_threshold} token",
                "over_request_peak": f"单请求 input 峰值 {REQUEST_PEAK_THRESHOLD}",
                "over_requests": f"请求数 {REQUEST_COUNT_THRESHOLD}",
                "over_input_total": f"累计 input {INPUT_TOTAL_THRESHOLD}",
            }
            detail = " / ".join(labels[r] for r in reasons)
            out["message"] = f"⚠️ 统一闸门触发（{detail}），请先生成恢复包，再开新对话。"
        elif over_now and already_forced:
            out["already_forced"] = True
        elif (not cur["forced"]) and (not cur["warned"]) and warn_now:
            cur["warned"] = True
            out["warned"] = True
            if count >= warn_at and token_count and token_count >= tok_warn:
                out["message"] = f"⚠️ 接近阈值：{args.threshold - count} 轮 或 {max(0, args.token_threshold - token_count)} token，请准备开新对话（只提醒一次）。"
            elif token_count and token_count >= tok_warn:
                out["message"] = f"⚠️ 接近 token 阈值：再用约 {max(0, args.token_threshold - token_count)} token 达 {args.token_threshold}，请准备开新对话（只提醒一次）。"
            else:
                rem = max(1, args.threshold - count)
                out["message"] = f"⚠️ 再 {rem} 轮将达到阈值 {args.threshold} 轮，请准备开新对话（本提醒只出一次）。"
        dialogs[key] = cur
        save(d)
        if out["warned"] or out["forced"]:
            others, suggest = cross_check(d, current_agent=agent, threshold=args.threshold, warn_at=warn_at,
                                          token_threshold=args.token_threshold, token_warn_at=tok_warn_at)
            out["cross_check"] = {"others": others, "suggest_install": suggest}
        out["metric"] = metric or None
        if lang == "en" and out.get("message"):
            _en = out["message"]
            _en = _en.replace("⚠️ 统一闸门触发（", "⚠️ unified gate triggered (")
            _en = _en.replace("），请先生成恢复包，再开新对话。", "); generate a recovery pack first, then open a new dialog.")
            _en = _en.replace("单请求 input 峰值 ", "single-request input peak ")
            _en = _en.replace("请求数 ", "requests ")
            _en = _en.replace("累计 input ", "cumulative input ")
            _en = _en.replace(" 轮", " turns")
            _en = _en.replace(" 轮 / ", " turns / ")
            _en = _en.replace("⚠️ 对话同时达到阈值：", "⚠️ conversation crossed both thresholds: ")
            _en = _en.replace(" 轮 / ", " turns / ")
            _en = _en.replace(" token，请生成恢复包后开新对话。", " tokens; generate a recovery pack and open a new dialog.")
            _en = _en.replace("⚠️ 对话已达 token 阈值 ", "⚠️ conversation reached token threshold ")
            _en = _en.replace("，请先生成恢复包，再开新对话。（轮数 ", "; generate a recovery pack first, then open a new dialog. (turns ")
            _en = _en.replace(" < ", " < ")
            _en = _en.replace("）", ")")
            _en = _en.replace("⚠️ 对话已达阈值 ", "⚠️ conversation reached threshold ")
            _en = _en.replace(" 轮，请先生成恢复包，再开新对话。", " turns; generate a recovery pack first, then open a new dialog.")
            _en = _en.replace("⚠️ 接近阈值：", "⚠️ approaching thresholds: ")
            _en = _en.replace(" 轮 或 ", " turns or ")
            _en = _en.replace(" token，请准备开新对话（只提醒一次）。", " token(s); prepare a new dialog (one-time notice).")
            _en = _en.replace("⚠️ 接近 token 阈值：再用约 ", "⚠️ approaching token threshold: about ")
            _en = _en.replace(" token 达 ", " tokens to reach ")
            _en = _en.replace("，请准备开新对话（只提醒一次）。", "; prepare a new dialog (one-time notice).")
            _en = _en.replace("⚠️ 再 ", "⚠️ only ")
            _en = _en.replace(" 轮将达到阈值 ", " turns to threshold ")
            _en = _en.replace(" 轮，请准备开新对话（本提醒只出一次）。", " turns; prepare a new dialog (one-time notice).")
            out["message"] = _en
        out = _attach_storage(out)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
