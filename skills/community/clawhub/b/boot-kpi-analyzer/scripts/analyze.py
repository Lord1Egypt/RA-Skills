#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Boot KPI Analyzer - SS4 车机开机/关机 KPI 分析工具

用法:
  analyze.py list                        # 列出所有可用数据
  analyze.py boot --latest               # 分析最新开机 KPI
  analyze.py boot --dir <YYYYMMDD_HHMMSS>
  analyze.py shutdown --latest           # 分析最新关机 KPI
  analyze.py shutdown --dir <YYYYMMDD_HHMMSS>
  analyze.py both --latest               # 同时分析开机+关机
"""

import os, re, sys, json, argparse
from datetime import datetime

BOOT_BASE     = "/home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/uploads"
SHUTDOWN_BASE = "/home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/reboot_tests"

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def sorted_sessions(base_dir):
    if not os.path.isdir(base_dir):
        return []
    entries = [e for e in os.scandir(base_dir) if e.is_dir()]
    entries.sort(key=lambda e: e.name)
    return entries

def latest_session(base_dir):
    s = sorted_sessions(base_dir)
    return s[-1] if s else None

def find_session(base_dir, name):
    path = os.path.join(base_dir, name)
    if os.path.isdir(path):
        return path
    for s in reversed(sorted_sessions(base_dir)):
        if s.name.startswith(name):
            return s.path
    return None

def sep(title="", w=70):
    if title:
        pad = max(2, (w - len(title) - 2) // 2)
        print("─" * pad + f" {title} " + "─" * (w - pad - len(title) - 2))
    else:
        print("─" * w)

# ── list 命令 ────────────────────────────────────────────────────────────────

def cmd_list(args):
    sep("开机 KPI 数据 (uploads)")
    for s in sorted_sessions(BOOT_BASE)[-20:]:
        has = "✓" if os.path.exists(os.path.join(s.path, "boot_kpi_summary.txt")) else " "
        print(f"  [{has}] {s.name}")
    if not sorted_sessions(BOOT_BASE):
        print(f"  (空: {BOOT_BASE})")

    print()
    sep("关机 KPI 数据 (reboot_tests)")
    for s in sorted_sessions(SHUTDOWN_BASE)[-20:]:
        rp = os.path.join(s.path, "report.json")
        tag, dur = " ", ""
        if os.path.exists(rp):
            try:
                r = json.load(open(rp))
                tag = "✓" if r.get("test_result") == "success" else "✗"
                d = r.get("reboot_duration")
                dur = f"  {d:.1f}s" if d else ""
            except Exception:
                pass
        print(f"  [{tag}] {s.name}{dur}")
    if not sorted_sessions(SHUTDOWN_BASE):
        print(f"  (空: {SHUTDOWN_BASE})")

# ── Boot KPI 解析 ────────────────────────────────────────────────────────────

# boot_kpi.log 格式: <service> -> <state> at <ms>ms from system boot
_BOOT_RE = re.compile(r'^(.+?)\s+->\s+(\S+)\s+at\s+(\d+)ms')

# unit_kpi.log: [UnitKPI] Dependency of qcrosvm.service (type=xxx): <svc> -> <state> at <ms>ms
_UNIT_DEP_RE = re.compile(
    r'\[UnitKPI\]\s+Dependency of qcrosvm\.service\s+\(type=([^)]+)\):\s+(.+?)\s+->\s+(\S+)\s+at\s+(\d+)ms'
)
_QCROSVM_ACTIVE_RE = re.compile(r'qcrosvm\.service became active at\s+(\d+)ms', re.IGNORECASE)


def parse_boot_kpi_log(log_path):
    events = []
    if not os.path.exists(log_path):
        return events
    with open(log_path, errors='replace') as f:
        for line in f:
            m = _BOOT_RE.match(line.strip())
            if m:
                events.append({"unit": m.group(1).strip(), "state": m.group(2), "ms": int(m.group(3))})
    return events


def parse_unit_kpi_log(log_path):
    deps, qcrosvm_times = [], []
    if not os.path.exists(log_path):
        return deps, qcrosvm_times
    with open(log_path, errors='replace') as f:
        for line in f:
            m = _UNIT_DEP_RE.search(line)
            if m:
                deps.append({"type": m.group(1).strip(), "unit": m.group(2).strip(),
                             "state": m.group(3), "ms": int(m.group(4))})
            m2 = _QCROSVM_ACTIVE_RE.search(line)
            if m2:
                qcrosvm_times.append(int(m2.group(1)))
    return deps, qcrosvm_times


def build_service_stats(events):
    """从 boot_kpi 事件计算各服务激活耗时"""
    unit_map = {}
    for ev in events:
        unit_map.setdefault(ev["unit"], []).append(ev)
    results = []
    for unit, evs in unit_map.items():
        by_state = {e["state"]: e["ms"] for e in evs}
        t_start = by_state.get("activating")
        t_end   = by_state.get("active")
        t_fail  = by_state.get("failed")
        dur = (t_end - t_start) if (t_end is not None and t_start is not None) else None
        results.append({
            "unit": unit,
            "activating_ms": t_start,
            "active_ms": t_end,
            "failed_ms": t_fail,
            "duration_ms": dur,
        })
    return results


# ── cmd_boot ─────────────────────────────────────────────────────────────────

def cmd_boot(args):
    if args.latest:
        s = latest_session(BOOT_BASE)
        if not s:
            print(f"[ERROR] 无开机 KPI 数据: {BOOT_BASE}"); return
        session_dir, session_name = s.path, s.name
    elif args.dir:
        session_dir = find_session(BOOT_BASE, args.dir)
        session_name = args.dir
        if not session_dir:
            print(f"[ERROR] 找不到目录: {args.dir}"); return
    else:
        print("[ERROR] 请指定 --latest 或 --dir <name>"); return

    sep(f"开机 KPI 分析: {session_name}")
    print(f"路径: {session_dir}\n")

    # 1. 先输出 summary
    summary_path = os.path.join(session_dir, "boot_kpi_summary.txt")
    if os.path.exists(summary_path):
        sep("boot_kpi_summary.txt")
        with open(summary_path, errors='replace') as f:
            print(f.read())
    else:
        print("[INFO] 无 boot_kpi_summary.txt，使用原始日志分析\n")

    # 2. 解析 boot_kpi.log
    events = parse_boot_kpi_log(os.path.join(session_dir, "boot_kpi.log"))
    if events:
        stats = build_service_stats(events)

        # qcrosvm 摘要
        sep("qcrosvm.service 时序")
        qcrosvm_events = [e for e in events if "qcrosvm" in e["unit"]]
        for ev in qcrosvm_events:
            print(f"  {ev['unit']:<45} -> {ev['state']:<12} at {ev['ms']}ms")
        qcrosvm_stats = [s for s in stats if "qcrosvm" in s["unit"]]
        for s in qcrosvm_stats:
            if s["duration_ms"] is not None:
                print(f"\n  ★ qcrosvm 激活耗时: {s['duration_ms']}ms  ({s['duration_ms']/1000:.2f}s)")

        # 慢服务 Top 20
        print()
        sep("慢服务 Top 20（激活耗时 > 100ms）")
        slow = sorted([s for s in stats if s["duration_ms"] is not None and s["duration_ms"] > 100],
                      key=lambda x: -x["duration_ms"])
        if slow:
            for i, s in enumerate(slow[:20], 1):
                print(f"  {i:>2}. {s['duration_ms']:>6}ms  {s['unit']}")
        else:
            print("  (无慢服务)")

        # 失败服务
        print()
        sep("失败的服务")
        failed = sorted(set(e["unit"] for e in events if e["state"] == "failed"))
        if failed:
            for u in failed:
                print(f"  ✗ {u}")
        else:
            print("  (无失败服务)")
    else:
        print("[WARN] boot_kpi.log 为空或不存在")

    # 3. unit_kpi.log
    unit_kpi_path = os.path.join(session_dir, "unit_kpi.log")
    deps, qcrosvm_times = parse_unit_kpi_log(unit_kpi_path)
    if deps or qcrosvm_times:
        print()
        sep("qcrosvm 依赖分析 (unit_kpi.log)")
        if qcrosvm_times:
            print(f"  qcrosvm 激活次数: {len(qcrosvm_times)}")
            for i, t in enumerate(qcrosvm_times, 1):
                print(f"    第{i}次激活: {t}ms ({t/1000:.2f}s)")
        if deps:
            print(f"\n  依赖服务总数: {len(deps)}")
            slow_deps = sorted([d for d in deps if d["ms"] > 5000], key=lambda x: -x["ms"])
            if slow_deps:
                print(f"  慢依赖 (>5s) Top 20:")
                for d in slow_deps[:20]:
                    print(f"    {d['ms']:>7}ms  [{d['type']}]  {d['unit']} -> {d['state']}")
            failed_deps = [d for d in deps if d["state"] in ("failed", "inactive")]
            if failed_deps:
                print(f"\n  失败/inactive 依赖:")
                for d in failed_deps:
                    print(f"    ✗ [{d['type']}] {d['unit']} -> {d['state']} at {d['ms']}ms")


# ── Shutdown 解析 ─────────────────────────────────────────────────────────────

# shutdown-monitor-units.log 格式:
# [2026-03-05 11:19:39.132] Unit: foo.service | State: ACTIVE -> INACTIVE | BPF_timestamp: 1319282669115
_SHUTDOWN_RE = re.compile(
    r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\]\s+'
    r'Unit:\s+(.+?)\s+\|\s+State:\s+(\S+)\s+->\s+(\S+)\s+\|\s+BPF_timestamp:\s+(\d+)'
)


def parse_shutdown_log(log_path):
    events = []
    if not os.path.exists(log_path):
        return events
    with open(log_path, errors='replace') as f:
        for line in f:
            m = _SHUTDOWN_RE.search(line)
            if m:
                events.append({
                    "wall": m.group(1),
                    "unit": m.group(2).strip(),
                    "from": m.group(3),
                    "to":   m.group(4),
                    "ns":   int(m.group(5)),
                })
    return events


def analyze_shutdown_events(events):
    """
    计算关机时序：
    - shutdown_target_ns: shutdown.target INACTIVE->ACTIVE 的 BPF 时间戳（关机开始基准）
    - umount_target_ns: umount.target INACTIVE->ACTIVE（关机晚期）
    - 每个服务从 ACTIVE/ACTIVATING -> DEACTIVATING 到 INACTIVE/FAILED 的耗时
    """
    # 找基准时间戳
    shutdown_start_ns = None
    umount_start_ns   = None
    for ev in events:
        if ev["unit"] == "shutdown.target" and ev["from"] == "INACTIVE" and ev["to"] == "ACTIVE":
            shutdown_start_ns = ev["ns"]
        if ev["unit"] == "umount.target" and ev["from"] == "INACTIVE" and ev["to"] == "ACTIVE":
            umount_start_ns = ev["ns"]

    # 按 unit 分组计算耗时
    unit_evs = {}
    for ev in events:
        unit_evs.setdefault(ev["unit"], []).append(ev)

    service_durations = []
    for unit, evs in unit_evs.items():
        deactivating_ns = None
        done_ns = None
        for ev in evs:
            if ev["to"] == "DEACTIVATING":
                deactivating_ns = ev["ns"]
            if ev["from"] == "DEACTIVATING" and ev["to"] in ("INACTIVE", "FAILED", "DEAD"):
                done_ns = ev["ns"]
        if deactivating_ns is not None and done_ns is not None:
            dur_ms = (done_ns - deactivating_ns) / 1_000_000
            service_durations.append({
                "unit": unit,
                "deactivating_ns": deactivating_ns,
                "done_ns": done_ns,
                "duration_ms": round(dur_ms, 1),
                "offset_ms": round((deactivating_ns - shutdown_start_ns) / 1_000_000, 1)
                             if shutdown_start_ns else None,
            })

    service_durations.sort(key=lambda x: -x["duration_ms"])
    return {
        "shutdown_start_ns": shutdown_start_ns,
        "umount_start_ns":   umount_start_ns,
        "service_durations": service_durations,
    }


def cmd_shutdown(args):
    if args.latest:
        s = latest_session(SHUTDOWN_BASE)
        if not s:
            print(f"[ERROR] 无关机 KPI 数据: {SHUTDOWN_BASE}"); return
        session_dir, session_name = s.path, s.name
    elif args.dir:
        session_dir = find_session(SHUTDOWN_BASE, args.dir)
        session_name = args.dir
        if not session_dir:
            print(f"[ERROR] 找不到目录: {args.dir}"); return
    else:
        print("[ERROR] 请指定 --latest 或 --dir <name>"); return

    sep(f"关机 KPI 分析: {session_name}")
    print(f"路径: {session_dir}\n")

    # 1. report.json
    report_path = os.path.join(session_dir, "report.json")
    if os.path.exists(report_path):
        sep("report.json 摘要")
        r = json.load(open(report_path))
        result_icon = "✓" if r.get("test_result") == "success" else "✗"
        print(f"  [{result_icon}] 测试结果    : {r.get('test_result', 'N/A')}")
        print(f"  reboot_duration  : {r.get('reboot_duration', 'N/A')} s")
        print(f"  build_id         : {r.get('build_id', 'N/A')}")
        print(f"  VIN              : {r.get('vin', 'N/A')}")
        print(f"  boot_counts      : {r.get('boot_counts_before', '?')} -> {r.get('boot_counts_after', '?')}")
        print(f"  has_lastlog      : {r.get('has_lastlog', False)}")
        if r.get("error_message"):
            print(f"  ⚠ error         : {r['error_message']}")
    else:
        print("[WARN] 无 report.json")

    # 2. shutdown-monitor-units.log
    print()
    log_path = os.path.join(session_dir, "shutdown-monitor-units.log")
    if not os.path.exists(log_path):
        # 有些目录里日志名可能不同
        candidates = [f for f in os.listdir(session_dir) if "shutdown" in f and f.endswith(".log")]
        if candidates:
            log_path = os.path.join(session_dir, candidates[0])

    if os.path.exists(log_path):
        events = parse_shutdown_log(log_path)
        if events:
            result = analyze_shutdown_events(events)
            sep("关机时序分析")
            ss_ns = result["shutdown_start_ns"]
            us_ns = result["umount_start_ns"]
            if ss_ns:
                print(f"  shutdown.target 激活时刻 (BPF ns): {ss_ns}")
            if us_ns and ss_ns:
                pre_umount_ms = (us_ns - ss_ns) / 1_000_000
                print(f"  umount.target 激活耗时 (关机前): {pre_umount_ms:.0f}ms ({pre_umount_ms/1000:.2f}s)")

            print()
            sep("各服务关机耗时 Top 20（DEACTIVATING -> INACTIVE）")
            durs = result["service_durations"]
            if durs:
                print(f"  {'耗时(ms)':>9}  {'启动偏移(ms)':>12}  服务名")
                print(f"  {'-'*9}  {'-'*12}  {'-'*40}")
                for d in durs[:20]:
                    off = f"{d['offset_ms']:>10.0f}" if d['offset_ms'] is not None else "          N/A"
                    print(f"  {d['duration_ms']:>9.1f}  {off}  {d['unit']}")
            else:
                print("  (未解析到 DEACTIVATING->INACTIVE 完整对)")

            # qcrosvm 关机
            print()
            sep("qcrosvm.service 关机事件")
            qcrosvm_evs = [e for e in events if "qcrosvm" in e["unit"]]
            if qcrosvm_evs:
                for ev in qcrosvm_evs:
                    off_s = ""
                    if ss_ns:
                        off_ms = (ev["ns"] - ss_ns) / 1_000_000
                        off_s = f"  (+{off_ms:.0f}ms)"
                    print(f"  {ev['unit']}: {ev['from']} -> {ev['to']}{off_s}")
            else:
                print("  (无 qcrosvm 关机事件)")
        else:
            print("[WARN] shutdown-monitor-units.log 无法解析到事件")
    else:
        print(f"[WARN] 未找到 shutdown-monitor-units.log: {session_dir}")


# ── cmd_both ─────────────────────────────────────────────────────────────────

def cmd_both(args):
    """同时分析最新/指定的开机 + 关机 KPI"""
    cmd_boot(args)
    print()
    print()
    cmd_shutdown(args)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SS4 Boot/Shutdown KPI 分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 analyze.py list
  python3 analyze.py boot --latest
  python3 analyze.py boot --dir 20260305_112056
  python3 analyze.py shutdown --latest
  python3 analyze.py shutdown --dir 20260305_112056
  python3 analyze.py both --latest
"""
    )
    sub = parser.add_subparsers(dest="cmd")

    # list
    sub.add_parser("list", help="列出所有可用数据目录")

    # boot
    p_boot = sub.add_parser("boot", help="分析开机 KPI")
    g_boot = p_boot.add_mutually_exclusive_group(required=True)
    g_boot.add_argument("--latest", action="store_true", help="使用最新数据")
    g_boot.add_argument("--dir", metavar="NAME", help="指定目录名（支持前缀匹配）")

    # shutdown
    p_shut = sub.add_parser("shutdown", help="分析关机 KPI")
    g_shut = p_shut.add_mutually_exclusive_group(required=True)
    g_shut.add_argument("--latest", action="store_true", help="使用最新数据")
    g_shut.add_argument("--dir", metavar="NAME", help="指定目录名（支持前缀匹配）")

    # both
    p_both = sub.add_parser("both", help="同时分析开机+关机 KPI")
    g_both = p_both.add_mutually_exclusive_group(required=True)
    g_both.add_argument("--latest", action="store_true", help="使用最新数据")
    g_both.add_argument("--dir", metavar="NAME", help="指定目录名（支持前缀匹配）")

    args = parser.parse_args()

    dispatch = {
        "list":     cmd_list,
        "boot":     cmd_boot,
        "shutdown": cmd_shutdown,
        "both":     cmd_both,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
