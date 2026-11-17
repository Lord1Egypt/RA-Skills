#!/usr/bin/env python3
"""会话钩子（Session Hook）——把「Agent 没打收尾标签」这件事变成可见信号（G4 · no_signoff）。

设计背景（为何需要）：
  收尾信号块依赖 Agent 在会话结束时输出并记录。若 Agent 没执行，数据上就像会话没
  发生过——「没记」本身是不可见的。no_signoff 缺失检测把沉默变成信号：会话开始钩子
  检查上一次会话是否留了收尾标记，没留则追加一行 L0·no_signoff 信号，让监控端能
  客观量化「Agent 执行率」，从而判断是 SKILL.md 措辞失效还是用户关了采集。

用法（SKILL.md A.2 会话钩子，均为静默执行、失败不阻塞、不打扰用户）：
  python scripts/session_hook.py begin [--dir <技能目录>]   # 会话开始：检测 + 更新状态
  python scripts/session_hook.py end   [--dir <技能目录>]   # 会话结束：标记已收尾（收尾块之后调用）
  python scripts/session_hook.py action <name> <outcome> [--dir <技能目录>]   # P1-4 动作链遥测（白名单动作名 + success/fail/partial/skip）

状态文件：<技能目录>/.session_state.json（运行时产物，发布时排除）：
  {"last_start_ts": "...", "last_signoff": false}

边界（防误报）：
  - 首次运行（无状态文件）：只建状态，不记 no_signoff（没有历史可判）。
  - `.optin=off`：本地记录关闭，跳过检测与记录。
  - 非信号技能（无 references/signals.md）：跳过。
  - begin 未结束又 begin（上次未收尾）：记一条 no_signoff。

零 PII：只写方法层标签 + 事件名；不读对话内容、不读用户文件。
"""
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone

STATE_NAME = ".session_state.json"
LOCK_NAME = ".session_hook.lock"
SIGNALS_MD = os.path.join("references", "signals.md")
EVENTS_ALLOWED = {"helpful", "unhelpful", "confusion", "suggestion", "abandoned", "misdiagnosis",
                  "accept", "reject", "iteration", "edit_capture"}
LAYERS_ALLOWED = {f"L{i}" for i in range(1, 8)}
# ---- P1-4 动作链遥测白名单（方法层标签，零 PII；详情见 signals.md §八）----
ACTION_NAMES_ALLOWED = {
    # 锻造炉自身动作（产出技能由 forge-signal-kit 注入各自白名单；此处为兜底默认集）
    "forge_new", "upgrade", "review", "recast", "clarify",
    "register_skill", "open_cloud_sync", "close_cloud_sync", "turn_off_log",
    "publish", "joint_test", "self_check", "inject_signal_kit",
    "run_pipeline", "view_signals", "view_growth", "delete_signals",
    "download_proposals", "apply_proposal",
}
ACTION_OUTCOMES_ALLOWED = {"success", "fail", "partial", "skip"}


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _optin_on(skill_dir):
    """本地记录开关：.optin 不存在 = 默认 on（安装即开）；存在则以内容为准。"""
    p = os.path.join(skill_dir, ".optin")
    try:
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip().lower() in ("1", "on", "true", "yes")
        return True
    except Exception:
        return True


def _read_anon_id(skill_dir):
    try:
        p = os.path.join(skill_dir, ".anon_id")
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    except Exception:
        pass
    return None


def _read_skill_version(skill_dir):
    try:
        md = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
        import re
        m = re.search(r"^version:\s*([\d.]+)", md, re.M)
        return m.group(1) if m else None
    except Exception:
        return None


def _append_signal(skill_dir, sig):
    path = os.path.join(skill_dir, "signals-log.jsonl")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(sig, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


def _read_state(skill_dir):
    p = os.path.join(skill_dir, STATE_NAME)
    try:
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    except Exception:
        pass
    return None


def _write_state(skill_dir, state):
    p = os.path.join(skill_dir, STATE_NAME)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.flush()
    except Exception:
        pass


def cmd_begin(skill_dir):
    """会话开始钩子：检测上次未收尾 → 记 no_signoff；更新状态（本次开始=未收尾）。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭（.optin=off），跳过")
        return 0

    prev = _read_state(skill_dir)
    if prev is None:
        # 首次：只建状态，不记（防误报——没有历史可判）
        _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": False})
        print(f"[session] [{name}] 首跑：仅建会话状态，不检测")
        return 0

    if prev.get("last_signoff") is False:
        # 上次会话开始了但未留收尾标记 → 把「没记」变成可见信号
        sig = {
            "ts": _utcnow_iso(),
            "signal_id": str(uuid.uuid4()),
            "client_signal_id": str(uuid.uuid4()),
            "skill_slug": name,
            "skill_version": _read_skill_version(skill_dir),
            "method_layer": "L0",
            "event": "no_signoff",
            "weight": 1,
            "note": "",
            "anon_id": _read_anon_id(skill_dir) or "",
        }
        ok = _append_signal(skill_dir, sig)
        print(f"[session] [{name}] 检测到上次会话未收尾 → 记录 L0·no_signoff（{'✓' if ok else '✗ 写入失败'}）")
    else:
        print(f"[session] [{name}] 上次会话已收尾，无需检测")

    _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": False})
    return 0


def cmd_start(skill_dir):
    """会话开始钩子（一条命令完成三件事）：补传 + 拉回 + 缺失检测。
    ——把 A.2 的 3 条命令收敛为 1 条，Agent 只需执行一次，确定性更高。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    # 1) 补传上次积累（upload_signals 默认扫描 ~/.workbuddy/skills，未开云同步内部跳过）
    try:
        subprocess.run([sys.executable, os.path.join(HERE, "upload_signals.py")],
                       capture_output=True, timeout=120)
    except Exception:
        pass
    # 2) 拉回云端历史（只对本技能；无配置/无 anon 内部跳过）
    try:
        subprocess.run([sys.executable, os.path.join(HERE, "download_signals.py"),
                        "pull", "--dir", skill_dir], capture_output=True, timeout=120)
    except Exception:
        pass
    # 3) begin 缺失检测（防误报：首跑仅建状态）
    cmd_begin(skill_dir)
    return 0


def _split_event(event):
    """拆分 `L<层>:<事件>` 或 `L<层>·<事件>`（Agent 可能照 SKILL.md 展示块 `[信号] L3·helpful`
    传中圆点 `·`——只认 `:` 会 TypeError 崩溃，P1-2 修复）。
    返回 (layer, event)；无分隔符时 event 为空串，由 _append_method_signal 报"未知事件"而非崩溃。"""
    for sep in (":", "·"):
        if sep in event:
            layer, ev = event.split(sep, 1)
            return layer.strip(), ev.strip()
    return event.strip(), ""


def _append_method_signal(skill_dir, layer, event, note=""):
    """写一条语义信号（标准 JSON，供 Agent 收尾/交互时调用，避免手写格式错误）。"""
    if event not in EVENTS_ALLOWED:
        print(f"[session] 未知事件: {event}（允许: {sorted(EVENTS_ALLOWED)}）")
        return 1
    if layer not in LAYERS_ALLOWED:
        print(f"[session] 未知层: {layer}（允许: {sorted(LAYERS_ALLOWED)}）")
        return 1
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭，跳过")
        return 0
    sig = {
        "ts": _utcnow_iso(),
        "signal_id": str(uuid.uuid4()),
        "client_signal_id": str(uuid.uuid4()),
        "skill_slug": name,
        "skill_version": _read_skill_version(skill_dir),
        "method_layer": layer,
        "event": event,
        "weight": 1,
        "note": note,
        "anon_id": _read_anon_id(skill_dir) or "",
    }
    ok = _append_signal(skill_dir, sig)
    print(f"[session] [{name}] 已记录信号 {layer}·{event}{('（'+note[:40]+'）') if note else ''}（{'✓' if ok else '✗ 写入失败'}）")
    return 0 if ok else 1


def cmd_signal(skill_dir, layer, event, note=""):
    return _append_method_signal(skill_dir, layer, event, note)


def cmd_usage(skill_dir, calls, success, errors="", duration=0, note=""):
    """写一条客观使用信号（usage_call，L0 + metric）——Agent 陈述客观事实，脚本生成标准 JSON。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭，跳过")
        return 0
    errors_map = {}
    if errors:
        for kv in errors.split(","):
            if "=" in kv:
                k, v = kv.split("=", 1)
                errors_map[k.strip()] = int(v)
    metric = {"calls": int(calls), "success": int(success), "period": "session", "source": "agent"}
    if errors_map:
        metric["errors"] = errors_map
    if duration:
        metric["duration_avg_ms"] = int(duration)
    sig = {
        "ts": _utcnow_iso(),
        "signal_id": str(uuid.uuid4()),
        "client_signal_id": str(uuid.uuid4()),
        "skill_slug": name,
        "skill_version": _read_skill_version(skill_dir),
        "method_layer": "L0",
        "event": "usage_call",
        "weight": 1,
        "note": note,
        "anon_id": _read_anon_id(skill_dir) or "",
        "metric": metric,
    }
    ok = _append_signal(skill_dir, sig)
    print(f"[session] [{name}] 已记录客观使用 usage_call（calls={calls} success={success}）（{'✓' if ok else '✗ 写入失败'}）")
    return 0 if ok else 1


def cmd_action(skill_dir, name, outcome):
    """写一条动作链遥测信号（action_trace，L0 + action_name/action_outcome）——匿名/方法层/opt-in。

    动作名必须在白名单（防止任意用户文本泄漏 PII）；结果固定枚举。守体验铁律。
    """
    author = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{author}] 非信号技能，跳过")
        return 0
    if not _optin_on(skill_dir):
        print(f"[session] [{author}] 本地记录关闭，跳过")
        return 0
    if name not in ACTION_NAMES_ALLOWED:
        print(f"[session] 未知动作名: {name}（允许: {sorted(ACTION_NAMES_ALLOWED)}）")
        return 1
    if outcome not in ACTION_OUTCOMES_ALLOWED:
        print(f"[session] 未知结果: {outcome}（允许: {sorted(ACTION_OUTCOMES_ALLOWED)}）")
        return 1
    sig = {
        "ts": _utcnow_iso(),
        "signal_id": str(uuid.uuid4()),
        "client_signal_id": str(uuid.uuid4()),
        "skill_slug": author,
        "skill_version": _read_skill_version(skill_dir),
        "method_layer": "L0",
        "event": "action_trace",
        "weight": 1,
        "note": "",
        "anon_id": _read_anon_id(skill_dir) or "",
        "action_name": name,
        "action_outcome": outcome,
    }
    ok = _append_signal(skill_dir, sig)
    print(f"[session] [{author}] 已记录动作链遥测 L0·action_trace({name}={outcome})（{'✓' if ok else '✗ 写入失败'}）")
    return 0 if ok else 1


def cmd_end(skill_dir, event=None):
    """会话结束钩子：写收尾信号（可选 --event）+ 标记已收尾。
    ——Agent 只需一条命令：先写信号（脚本生成标准 JSON），再标记收尾。"""
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, SIGNALS_MD)):
        print(f"[session] [{name}] 非信号技能，跳过")
        return 0
    if event:
        rc = _append_method_signal(skill_dir, *_split_event(event))
        if rc:
            return rc
    if not _optin_on(skill_dir):
        print(f"[session] [{name}] 本地记录关闭，跳过")
        return 0
    _write_state(skill_dir, {"last_start_ts": _utcnow_iso(), "last_signoff": True})
    print(f"[session] [{name}] 会话已标记收尾")
    return 0


def main():
    import argparse
    p = argparse.ArgumentParser(prog="session_hook.py", description=__doc__.splitlines()[0])
    p.add_argument("--dir", default=None, help="技能目录（默认=脚本所在目录的上一级）")
    sub = p.add_subparsers(dest="cmd")
    ps = sub.add_parser("start", help="会话开始：补传+拉回+缺失检测（一条命令）")
    ps.add_argument("--dir", default=None)
    sp = sub.add_parser("signal", help="写一条语义信号")
    sp.add_argument("--dir", default=None)
    sp.add_argument("event", help="格式 L<层>:<事件> 或 L<层>·<事件>，如 L3:helpful / L3·helpful")
    sp.add_argument("--note", default="", help="仅相对路径/标签等零 PII 备注")
    su = sub.add_parser("usage", help="写一条客观使用信号（usage_call）")
    su.add_argument("--dir", default=None)
    su.add_argument("--calls", required=True, type=int, help="调用次数")
    su.add_argument("--success", required=True, type=int, help="成功次数")
    su.add_argument("--errors", default="", help="错误分布 k=v,k=v（如 timeout=1,auth=2）")
    su.add_argument("--duration", default=0, type=int, help="平均耗时 ms")
    su.add_argument("--note", default="", help="行业细节（如 endpoint=search(v1)）")
    se = sub.add_parser("end", help="会话结束：写收尾信号+标记收尾")
    se.add_argument("--dir", default=None)
    se.add_argument("--event", default=None, help="格式 L<层>:<事件> 或 L<层>·<事件>，如 L3:helpful / L3·helpful")
    sa = sub.add_parser("action", help="写一条动作链遥测(action_trace)")
    sa.add_argument("--dir", default=None)
    sa.add_argument("name", help="动作名（白名单方法层标签，见 signals.md §八）")
    sa.add_argument("outcome", help="结果 success/fail/partial/skip")
    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 2
    # 技能目录：--dir（主或子命令）优先，否则用脚本位置推导（scripts/ 的父目录）
    sub_args = getattr(args, args.cmd, None)
    skill_dir = args.dir or (sub_args.dir if sub_args else None) \
        or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.cmd == "start":
        return cmd_start(skill_dir)
    if args.cmd == "signal":
        layer, ev = _split_event(args.event)
        return cmd_signal(skill_dir, layer, ev, note=args.note)
    if args.cmd == "usage":
        return cmd_usage(skill_dir, args.calls, args.success, errors=args.errors,
                         duration=args.duration, note=args.note)
    if args.cmd == "end":
        return cmd_end(skill_dir, event=args.event)
    if args.cmd == "action":
        return cmd_action(skill_dir, args.name, args.outcome)
    return 2


if __name__ == "__main__":
    sys.exit(main())
