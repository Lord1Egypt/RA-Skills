#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_chain.py — 给任何项目生成可复算的治理证据链

三件事：
  L1 立籍  init     记录「谁在干、干什么、依据什么」
  L2 留证  seal     记录「改了什么、指纹是什么、怎么复算」
  L2 校验  verify   复算指纹，判定有没有「未记录的改动」
  L3 门禁  gate     登记高风险动作，等待人工确认

零依赖，只用标准库。所有产物落在 <root>/.governance/ 下，只增不改。

用法：
  python audit_chain.py init   --root . --task "任务目标" --actor "谁在干" [--basis "依据.md"]
  python audit_chain.py seal   --root . --note "本轮做了什么"
  python audit_chain.py verify --root . [--report EVIDENCE_REPORT.md]
  python audit_chain.py gate   --root . --action "对外发邮件" --detail "收件人/内容摘要"
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GOV = ".governance"
SKIP_DIRS = {
    ".git", ".governance", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build", ".idea", ".vscode", ".mypy_cache", ".pytest_cache",
}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


# ---------- 基础工具 ----------

def stamps():
    """返回 (UTC 时间戳, 本地时间戳) —— 双时间戳，避免时区争议"""
    u = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    l = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    return u, l


def gov_path(root):
    p = os.path.join(root, GOV)
    os.makedirs(p, exist_ok=True)
    return p


def append_jsonl(root, name, record):
    path = os.path.join(gov_path(root), name)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def read_jsonl(root, name):
    path = os.path.join(gov_path(root), name)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def iter_files(root):
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
        )
        for fn in sorted(filenames):
            if fn in SKIP_FILES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            yield rel, full


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root):
    """给当前所有文件拍一次指纹快照"""
    snap = {}
    for rel, full in iter_files(root):
        try:
            st = os.stat(full)
            snap[rel] = {"sha256": sha256_of(full), "size": st.st_size}
        except OSError:
            continue
    return snap


def latest_snapshot(root):
    records = read_jsonl(root, "evidence.jsonl")
    for rec in reversed(records):
        if rec.get("kind") == "snapshot":
            return rec
    return None


# ---------- L1 立籍 ----------

def cmd_init(args):
    utc, local = stamps()
    root = os.path.abspath(args.root)

    basis = []
    for b in (args.basis or []):
        bp = os.path.join(root, b)
        item = {"path": b.replace("\\", "/"), "exists": os.path.exists(bp)}
        if item["exists"]:
            try:
                item["sha256"] = sha256_of(bp)
            except OSError:
                item["sha256"] = None
        basis.append(item)

    registry = {
        "kind": "registry",
        "task_id": "T-%s" % datetime.now().strftime("%Y%m%d%H%M%S"),
        "actor": args.actor or "未填写",
        "task": args.task or "未填写",
        "basis": basis,
        "approved_by": args.approved_by or None,
        "root": root,
        "ts_utc": utc,
        "ts_local": local,
    }
    p = append_jsonl(root, "registry.jsonl", registry)

    snap = snapshot(root)
    append_jsonl(root, "evidence.jsonl", {
        "kind": "snapshot",
        "task_id": registry["task_id"],
        "note": "建档基线快照",
        "file_count": len(snap),
        "files": snap,
        "ts_utc": utc,
        "ts_local": local,
    })

    print("[L1 OK] 任务籍已建立  task_id=%s" % registry["task_id"])
    print("        谁=%s  干什么=%s  依据=%d 项" % (
        registry["actor"], registry["task"], len(basis)))
    print("[L2 OK] 基线快照已记录  %d 个文件" % len(snap))
    print("        台账位置: %s" % p)
    print("        复算命令: python scripts/audit_chain.py verify --root .")
    return 0


# ---------- L2 留证 ----------

def cmd_seal(args):
    root = os.path.abspath(args.root)
    prev = latest_snapshot(root)
    snap = snapshot(root)

    added, modified, removed = [], [], []
    if prev:
        old = prev.get("files", {})
        for rel, meta in snap.items():
            if rel not in old:
                added.append(rel)
            elif old[rel].get("sha256") != meta["sha256"]:
                modified.append(rel)
        for rel in old:
            if rel not in snap:
                removed.append(rel)

    utc, local = stamps()
    entry = {
        "kind": "snapshot",
        "task_id": (prev or {}).get("task_id") or "未登记",
        "note": args.note or "",
        "file_count": len(snap),
        "files": snap,
        "delta": {"added": added, "modified": modified, "removed": removed},
        "ts_utc": utc,
        "ts_local": local,
    }
    append_jsonl(root, "evidence.jsonl", entry)

    print("[L2 OK] 证据已追加  %s" % local)
    print("        新增 %d / 修改 %d / 删除 %d  共 %d 个文件" % (
        len(added), len(modified), len(removed), len(snap)))
    for rel in added[:10]:
        print("        + %s" % rel)
    for rel in modified[:10]:
        print("        ~ %s" % rel)
    for rel in removed[:10]:
        print("        - %s" % rel)
    return 0


# ---------- L3 门禁 ----------

def cmd_gate(args):
    root = os.path.abspath(args.root)
    utc, local = stamps()
    rec = {
        "kind": "gate",
        "action": args.action,
        "detail": args.detail or "",
        "status": "pending",
        "confirmed_by": None,
        "ts_utc": utc,
        "ts_local": local,
    }
    p = append_jsonl(root, "gates.jsonl", rec)
    print("[L3 GATE] 高风险动作已登记，等待人工确认")
    print("          动作: %s" % rec["action"])
    print("          详情: %s" % (rec["detail"] or "-"))
    print("          状态: pending  ← 未确认前不应执行该动作")
    print("          台账: %s" % p)
    print("          确认后由人工在 gates.jsonl 该行补 confirmed_by 与时间（或由审批系统回写）")
    return 0


# ---------- L2 校验 + 举证报告 ----------

def cmd_verify(args):
    root = os.path.abspath(args.root)
    prev = latest_snapshot(root)
    regs = read_jsonl(root, "registry.jsonl")
    gates = read_jsonl(root, "gates.jsonl")
    utc, local = stamps()

    if not prev:
        print("[L1 MISS] 未找到任何任务籍 —— 先跑 init 建立基线")
        print("[L2 FAIL] 无基线快照，无法复算")
        return 1

    cur = snapshot(root)
    old = prev.get("files", {})
    added = [r for r in cur if r not in old]
    modified = [r for r in cur if r in old and old[r].get("sha256") != cur[r]["sha256"]]
    removed = [r for r in old if r not in cur]

    registry = regs[-1] if regs else {}
    l1_ok = bool(registry.get("actor")) and registry.get("actor") != "未填写" \
        and bool(registry.get("task")) and registry.get("task") != "未填写"
    l2_ok = not (modified or removed)
    pending_gates = [g for g in gates if g.get("status") == "pending"]

    print("=" * 62)
    print("治理证据链复算报告  %s" % local)
    print("=" * 62)
    print("[L1] 任务籍 : %s" % ("PASS  谁=%s 任务=%s" % (
        registry.get("actor"), registry.get("task")) if l1_ok else "MISS  缺「谁」或「干什么」"))
    print("[L2] 指纹   : %s" % ("PASS  与基线一致" if l2_ok else "FAIL  存在未记录的改动"))
    if modified:
        print("       修改未记录 %d 个:" % len(modified))
        for r in modified[:15]:
            print("         ~ %s  (基线 %s… → 现 %s…)" % (
                r, old[r].get("sha256", "")[:12], cur[r]["sha256"][:12]))
    if removed:
        print("       删除未记录 %d 个:" % len(removed))
        for r in removed[:15]:
            print("         - %s" % r)
    if added:
        print("       新增未记录 %d 个（新增不算破坏，但应补 seal）:" % len(added))
        for r in added[:10]:
            print("         + %s" % r)
    print("[L3] 门禁   : %s" % (
        "PASS  无待确认动作" if not pending_gates
        else "WAIT  %d 个高风险动作待人工确认" % len(pending_gates)))
    for g in pending_gates[:10]:
        print("         ! %s  (%s)" % (g.get("action"), g.get("detail") or "-"))

    verdict = "可举证" if (l1_ok and l2_ok and not pending_gates) else "有缺口"
    print("-" * 62)
    print("结论: %s" % verdict)
    print("复算命令: python scripts/audit_chain.py verify --root .")

    if args.report:
        rp = os.path.join(root, args.report)
        with open(rp, "w", encoding="utf-8") as f:
            f.write("# 治理证据链复算报告\n\n")
            f.write("- 生成时间（本地）：%s\n" % local)
            f.write("- 生成时间（UTC）：%s\n" % utc)
            f.write("- 基线快照时间：%s\n" % (prev.get("ts_local") or "-"))
            f.write("- 结论：**%s**\n\n" % verdict)
            f.write("## L1 任务籍\n\n")
            if registry:
                f.write("| 字段 | 值 |\n|---|---|\n")
                f.write("| task_id | %s |\n" % registry.get("task_id", "-"))
                f.write("| 谁在干 | %s |\n" % registry.get("actor", "-"))
                f.write("| 干什么 | %s |\n" % registry.get("task", "-"))
                f.write("| 谁批的 | %s |\n" % (registry.get("approved_by") or "未登记"))
                f.write("| 依据 | %s |\n\n" % (
                    "、".join(b.get("path", "") for b in registry.get("basis", [])) or "未登记"))
            else:
                f.write("未找到任务籍。\n\n")
            f.write("## L2 指纹复算\n\n")
            f.write("| 项目 | 数量 |\n|---|---|\n")
            f.write("| 当前文件 | %d |\n| 基线文件 | %d |\n" % (len(cur), len(old)))
            f.write("| 修改未记录 | %d |\n| 删除未记录 | %d |\n| 新增未记录 | %d |\n\n" % (
                len(modified), len(removed), len(added)))
            if modified:
                f.write("### 修改明细\n\n| 文件 | 基线指纹 | 现指纹 |\n|---|---|---|\n")
                for r in modified:
                    f.write("| %s | %s… | %s… |\n" % (
                        r, old[r].get("sha256", "")[:16], cur[r]["sha256"][:16]))
                f.write("\n")
            f.write("## L3 门禁确认\n\n")
            if gates:
                f.write("| 动作 | 详情 | 状态 |\n|---|---|---|\n")
                for g in gates:
                    f.write("| %s | %s | %s |\n" % (
                        g.get("action"), g.get("detail") or "-", g.get("status")))
            else:
                f.write("未登记高风险动作。\n")
            f.write("\n---\n\n")
            f.write("本报告由 audit_chain.py 生成，可复算：`python scripts/audit_chain.py verify --root .`\n")
        print("报告已写入: %s" % rp)

    return 0 if verdict == "可举证" else 1


# ---------- 入口 ----------

def build_parser():
    p = argparse.ArgumentParser(
        prog="audit_chain.py",
        description="生成可复算的 AI 治理证据链（L1 籍 / L2 证 / L3 门）")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("init", help="L1：建立任务籍 + 基线快照")
    a.add_argument("--root", default=".")
    a.add_argument("--task", required=True, help="干什么（一句话目标）")
    a.add_argument("--actor", required=True, help="谁在干（人/模型/工具链）")
    a.add_argument("--basis", action="append", help="依据材料路径，可多次指定")
    a.add_argument("--approved-by", dest="approved_by", default=None, help="谁批的")
    a.set_defaults(func=cmd_init)

    b = sub.add_parser("seal", help="L2：追加一次指纹快照（收工时跑）")
    b.add_argument("--root", default=".")
    b.add_argument("--note", default="", help="本轮做了什么")
    b.set_defaults(func=cmd_seal)

    c = sub.add_parser("gate", help="L3：登记高风险动作，等待人工确认")
    c.add_argument("--root", default=".")
    c.add_argument("--action", required=True, help="动作名，如「对外发邮件」")
    c.add_argument("--detail", default="", help="详情，如收件人与内容摘要")
    c.set_defaults(func=cmd_gate)

    d = sub.add_parser("verify", help="L2：复算指纹并出举证报告")
    d.add_argument("--root", default=".")
    d.add_argument("--report", default=None, help="输出 Markdown 报告文件名")
    d.set_defaults(func=cmd_verify)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
