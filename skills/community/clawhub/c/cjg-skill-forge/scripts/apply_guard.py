#!/usr/bin/env python3
"""回归守卫（P1 · 防越做越差，C6/N4）——SkillForge apply 的质量门。

对应 skill2loop-benchmark-2026-08-21.md §3 P1「回归守卫」+ VA7 视频③「防止 Skill 越做越差」：
  apply 前必须：① 改前快照（可回滚）；② 写 CHANGELOG（原因+预期+测试）；
  apply 后必须：③ 对比近期采纳率增量；④ 下降 → 告警 + 一键回滚。

用法：
  python apply_guard.py --snapshot <skill_dir> [--label <说明>]   # ①改前快照 → 打印 snapshot_id
  python apply_guard.py --changelog <skill_dir> --snapshot <id> \
      --reason <原因> --impact <预期> [--tests <测试>]             # ②写 CHANGELOG（追加 CHANGELOG.md）
  python apply_guard.py --check <skill_dir> [--days 14]           # ③落地后对比采纳率 → 下降返回码 2 + 告警
  python apply_guard.py --rollback <skill_dir> <snapshot_id>      # ④一键回滚（从快照还原）

设计原则：
  - snapshot 只复制 SKILL.md / references/* / scripts/* 到 <skill_dir>/.apply-snapshots/<id>/
    （.apply-snapshots 是运行时产物，不进包/不进 git，发布工具排除清单已加）
  - rollback 只从指定快照还原，绝不删用户其他文件
  - check 只读 signals-log.jsonl，对比前/后窗口采纳率，下降超过阈值才告警
"""
import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
SNAP_ROOT = ".apply-snapshots"
CHANGELOG_NAME = "CHANGELOG.md"
TRACK = ("SKILL.md", "references", "scripts")
# 采纳率下降告警阈值（百分点）
DROP_THRESHOLD = 10


def _now():
    return datetime.now(CST).strftime("%Y%m%d-%H%M%S")


def _rel_tracked(skill_dir):
    """返回白名单内相对路径列表（SKILL.md + references/** + scripts/**）。"""
    out = []
    for root, dirs, files in os.walk(skill_dir):
        rel_root = os.path.relpath(root, skill_dir).replace("\\", "/")
        if rel_root == ".":
            rel_root = ""
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "cloud-enhancement",
                                                ".claude-plugin", SNAP_ROOT)]
        for fn in files:
            rel = f"{rel_root}/{fn}" if rel_root else fn
            if rel_root == "" and rel != "SKILL.md":
                continue
            # 只跟踪 references/** 与 scripts/**（含单层目录 references/scripts 本身）
            if rel_root and rel_root.split("/")[0] not in ("references", "scripts"):
                continue
            if fn in (".skill_edit_baseline.json", "signals-log.jsonl", ".uploaded_ids.txt"):
                continue
            out.append(rel)
    return sorted(out)


def cmd_snapshot(skill_dir, label=""):
    snap_dir = os.path.join(skill_dir, SNAP_ROOT)
    os.makedirs(snap_dir, exist_ok=True)
    sid = _now()
    dest = os.path.join(snap_dir, sid)
    os.makedirs(dest, exist_ok=True)
    files = _rel_tracked(skill_dir)
    for rel in files:
        src = os.path.join(skill_dir, rel.replace("/", os.sep))
        if os.path.isfile(src):
            d = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(src, d)
    meta = {"id": sid, "label": label, "files": files,
            "created_at": datetime.now(CST).isoformat(timespec="seconds")}
    with open(os.path.join(dest, "_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(f"[guard] 快照已保存: {sid}（{len(files)} 文件）")
    print(f"[guard] 回滚命令: python {os.path.abspath(__file__)} --rollback \"{skill_dir}\" {sid}")
    return sid


def cmd_changelog(skill_dir, snapshot_id, reason, impact, tests):
    path = os.path.join(skill_dir, CHANGELOG_NAME)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# 变更日志（回归守卫 · 防越做越差）\n\n")
    entry = (
        f"## {datetime.now(CST).strftime('%Y-%m-%d %H:%M')} · snapshot {snapshot_id}\n"
        f"- **原因**：{reason}\n"
        f"- **预期影响**：{impact or '—'}\n"
        f"- **测试**：{tests or '（待补）'}\n\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"[guard] CHANGELOG 已追加: {path}")
    return True


def _load_signals(skill_dir):
    path = os.path.join(skill_dir, "signals-log.jsonl")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except Exception:
        return []


def _adopt_rate(rows):
    """采纳率：accepted=1 / accepted 非 NULL。数据不足返回 None。"""
    judged = [r for r in rows if r.get("accepted") is not None]
    if not judged:
        return None
    adopted = sum(1 for r in judged if r["accepted"] in (1, True, "1", "true"))
    return adopted / len(judged) * 100


def cmd_check(skill_dir, days=14):
    """落地后对比：近 N 天 vs 前 N 天采纳率。下降超阈值 → 返回码 2 + 告警 + 回滚提示。"""
    rows = _load_signals(skill_dir)
    if not rows:
        print("[guard] 无信号数据，跳过对比（等有闭环信号后再跑 --check）")
        return 0
    now = datetime.now(timezone.utc)
    cutoff_cur = now - timedelta(days=days)
    cutoff_prev = now - timedelta(days=days * 2)

    def _ts(s):
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    cur = [r for r in rows if (_ts(r.get("ts")) or now) >= cutoff_cur]
    prev = [r for r in rows if cutoff_prev <= (_ts(r.get("ts")) or now) < cutoff_cur]
    cur_rate = _adopt_rate(cur)
    prev_rate = _adopt_rate(prev)
    print(f"[guard] 采纳率对比：近 {days} 天 {cur_rate if cur_rate is not None else '数据不足'}"
          f" vs 前 {days} 天 {prev_rate if prev_rate is not None else '数据不足'}")
    if cur_rate is None or prev_rate is None:
        print("[guard] 任一侧数据不足，无法判定（正常，闭环数据积累中）")
        return 0
    drop = prev_rate - cur_rate
    if drop >= DROP_THRESHOLD:
        print(f"[guard] 🚨 采纳率下降 {drop:.0f} 个百分点（≥{DROP_THRESHOLD}）——技能疑似退步！")
        print(f"[guard] 建议：查看最近快照 `ls {os.path.join(skill_dir, SNAP_ROOT)}` 并回滚，"
              f"或先本地模拟测试再 apply")
        return 2
    if cur_rate < prev_rate:
        print(f"[guard] ⚠️ 采纳率小幅下降 {drop:.0f} 个百分点（低于阈值 {DROP_THRESHOLD}），继续观察")
        return 0
    print(f"[guard] ✅ 采纳率 {cur_rate:.0f}%（{('上升' if cur_rate > prev_rate else '持平')}），未退化")
    return 0


def cmd_rollback(skill_dir, snapshot_id):
    dest = os.path.join(skill_dir, SNAP_ROOT, snapshot_id)
    meta_path = os.path.join(dest, "_meta.json")
    if not os.path.isdir(dest):
        print(f"[guard] ❌ 快照不存在: {snapshot_id}", file=sys.stderr)
        return 2
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
    files = meta.get("files") or [f for f in os.listdir(dest) if f != "_meta.json"]
    restored = 0
    for rel in files:
        src = os.path.join(dest, rel.replace("/", os.sep))
        if not os.path.isfile(src):
            continue
        dst = os.path.join(skill_dir, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        restored += 1
    print(f"[guard] ✅ 已从快照 {snapshot_id} 还原 {restored} 个文件")
    return 0


def main():
    ap = argparse.ArgumentParser(description="回归守卫（apply 质量门）")
    ap.add_argument("--snapshot", metavar="SKILL_DIR", help="① 改前快照")
    ap.add_argument("--label", default="", help="快照说明")
    ap.add_argument("--changelog", metavar="SKILL_DIR", help="② 追加 CHANGELOG")
    ap.add_argument("--snapshot-id", default=None, help="本次改动的快照 id")
    ap.add_argument("--reason", default="", help="改动原因")
    ap.add_argument("--impact", default="", help="预期影响")
    ap.add_argument("--tests", default="", help="测试说明")
    ap.add_argument("--check", metavar="SKILL_DIR", help="③ 落地后对比采纳率")
    ap.add_argument("--days", type=int, default=14, help="对比窗口天数")
    ap.add_argument("--rollback", nargs=2, metavar=("SKILL_DIR", "SNAPSHOT_ID"), help="④ 一键回滚")
    args = ap.parse_args()

    if args.snapshot:
        sys.exit(0 if cmd_snapshot(os.path.abspath(args.snapshot), args.label) else 2)
    if args.changelog:
        sys.exit(0 if cmd_changelog(os.path.abspath(args.changelog), args.snapshot_id or "?",
                                    args.reason, args.impact, args.tests) else 2)
    if args.check:
        sys.exit(cmd_check(os.path.abspath(args.check), args.days))
    if args.rollback:
        sys.exit(cmd_rollback(os.path.abspath(args.rollback[0]), args.rollback[1]))
    ap.print_help()


if __name__ == "__main__":
    main()
