#!/usr/bin/env python3
"""
candidates_review.py — 记忆候选审核机制 (P3)

Dreaming / auto-memory 产出的候选记忆不再直接写入，
而是进入 memory/.candidates/ 待审队列，经人工确认后写入。

流程：
  1. Dreaming → candidates.json → .candidates/YYYY-MM-DD.json
  2. auto-memory → 新条目 → .candidates/ 待审
  3. 用户确认 → 写入 ARCHIVE.md / MEMORY.md
  4. 拒绝 → 标记为 rejected

用法:
  python3 candidates_review.py list              # 列出待审候选
  python3 candidates_review.py approve --id X    # 批准指定候选
  python3 candidates_review.py reject --id X     # 拒绝指定候选
  python3 candidates_review.py approve-all       # 批准所有待审
  python3 candidates_review.py stats             # 审核统计
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
CANDIDATES_DIR = WORKSPACE / "memory" / ".candidates"
STATE_FILE = CANDIDATES_DIR / "review-state.json"
ARCHIVE_MD = WORKSPACE / "ARCHIVE.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"

CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"pending": {}, "approved": {}, "rejected": {}, "total_reviewed": 0}


def save_state(state: dict, *, sync: bool = True):
    """原子写入状态文件：临时文件 + rename + 可选 fsync"""
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if sync:
        try:
            os.fsync(tmp.open("wb"))
        except Exception:
            pass  # sync 失败不影响 rename
    tmp.rename(STATE_FILE)


def list_candidates(state: dict = None):
    """列出所有待审候选"""
    if state is None:
        state = load_state()

    pending = state.get("pending", {})
    if not pending:
        print(json.dumps({"status": "ok", "pending_count": 0, "message": "没有待审候选"}))
        return

    items = []
    for cid, candidate in pending.items():
        items.append({
            "id": cid,
            "date": candidate.get("date", ""),
            "category": candidate.get("category", ""),
            "content": candidate.get("content", "")[:120],
            "source": candidate.get("source", ""),
            "score": candidate.get("score", 0),
        })

    print(json.dumps({
        "status": "ok",
        "pending_count": len(items),
        "candidates": sorted(items, key=lambda x: x.get("score", 0), reverse=True),
    }, ensure_ascii=False, indent=2))


def _atomic_approve(state: dict, cid: str, candidate: dict, today: str):
    """原子地完成单个候选的 ARCHIVE 写入 + 状态更新。"""
    cat = candidate.get("category", "其他")
    content = candidate.get("content", "")
    entry = f"\n<!-- candidate:{cid} -->\n- **{cat}** (已审核 {today}): {content}"

    # 原子写入 ARCHIVE.md（临时文件 + rename）
    try:
        archive = ARCHIVE_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        archive = "# 详细档案 ARCHIVE.md\n"
    archive = archive.rstrip() + f"\n{entry}"
    tmp_archive = ARCHIVE_MD.with_suffix(".tmp")
    tmp_archive.write_text(archive, encoding="utf-8")
    tmp_archive.rename(ARCHIVE_MD)

    # 更新状态并原子保存
    state["approved"][cid] = {**candidate, "approved_at": today}
    del state["pending"][cid]
    state["total_reviewed"] = state.get("total_reviewed", 0) + 1
    save_state(state)


def approve_candidate(cid: str):
    """批准候选：写入 ARCHIVE.md"""
    state = load_state()
    candidate = state["pending"].get(cid)
    if not candidate:
        print(json.dumps({"status": "error", "message": f"候选 {cid} 不存在"}))
        return

    today = datetime.now().strftime("%Y-%m-%d")
    _atomic_approve(state, cid, candidate, today)

    print(json.dumps({
        "status": "approved",
        "id": cid,
        "written_to": str(ARCHIVE_MD),
    }, ensure_ascii=False))


def reject_candidate(cid: str):
    """拒绝候选"""
    state = load_state()
    candidate = state["pending"].get(cid)
    if not candidate:
        print(json.dumps({"status": "error", "message": f"候选 {cid} 不存在"}))
        return

    today = datetime.now().strftime("%Y-%m-%d")
    state["rejected"][cid] = {**candidate, "rejected_at": today}
    del state["pending"][cid]
    state["total_reviewed"] = state.get("total_reviewed", 0) + 1
    save_state(state)

    print(json.dumps({"status": "rejected", "id": cid}, ensure_ascii=False))


def approve_all():
    """批准所有待审候选（基于启动时的一致快照，避免循环内重载导致状态错位）"""
    state = load_state()
    pending_ids = list(state["pending"].keys())
    if not pending_ids:
        print(json.dumps({"status": "ok", "message": "没有待审候选"}))
        return

    today = datetime.now().strftime("%Y-%m-%d")
    for cid in pending_ids:
        # 每次从稳定 state 字典中取候选（不在循环内重载文件）
        candidate = state["pending"].get(cid)
        if candidate is None:
            continue  # 已被前面迭代处理过
        _atomic_approve(state, cid, candidate, today)

    print(json.dumps({"status": "ok", "approved": len(pending_ids)}, ensure_ascii=False))


def stats():
    """审核统计"""
    state = load_state()
    print(json.dumps({
        "status": "ok",
        "pending": len(state.get("pending", {})),
        "approved": len(state.get("approved", {})),
        "rejected": len(state.get("rejected", {})),
        "total_reviewed": state.get("total_reviewed", 0),
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="记忆候选审核机制 (P3)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="列出待审候选")
    sub.add_parser("approve-all", help="批准所有待审")
    sub.add_parser("stats", help="审核统计")

    app = sub.add_parser("approve", help="批准指定候选")
    app.add_argument("--id", required=True)

    rej = sub.add_parser("reject", help="拒绝指定候选")
    rej.add_argument("--id", required=True)

    args = parser.parse_args()

    if args.command == "list":
        list_candidates()
    elif args.command == "approve":
        approve_candidate(args.id)
    elif args.command == "reject":
        reject_candidate(args.id)
    elif args.command == "approve-all":
        approve_all()
    elif args.command == "stats":
        stats()


if __name__ == "__main__":
    main()
