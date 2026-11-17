#!/usr/bin/env python3
"""Free Model Auditor — safe, deterministic models.json differ/applier.

Why this exists
---------------
The audit skill must never *rebuild* a user's `models.json` from scratch. A naive
"rewrite the whole file as pretty JSON" step (done by an LLM or by hand) silently
drops every entry the agent didn't track in context — which is exactly the bug that
wiped first-time users' pre-existing custom models.

This script is the *only* sanctioned writer of `models.json` for the audit. It
performs strictly two kinds of mutations, and preserves everything else verbatim:

  - ADD    : append entries from `diff["add"]` that are not already present (by id)
  - REMOVE : delete entries whose `id` is listed in `diff["remove"]`

It then enforces an invariant and refuses to write on any anomaly:

    out_count == in_count + added - removed

and backs up `models.json` to `models.json.bak` before writing.

Stdlib only. Importable: `from apply_diff import apply_diff`.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile


def _load(path):
    """Load models.json. Returns (container, is_wrapped).

    container is the *list* of model entries.
    is_wrapped True means the file is {"models": [...]} and we must preserve that.
    A bare top-level [...] array is also supported (is_wrapped False).
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("models"), list):
        return data["models"], True, data
    if isinstance(data, list):
        return data, False, None
    raise ValueError("models.json 既不是 {'models':[...]} 也不是 [...]，结构无法识别")


def _wrap(container, is_wrapped, original):
    if is_wrapped:
        original["models"] = container
        return original
    return container


def apply_diff(models_path, diff, dry_run=False, backup=True):
    """Apply a structured diff to models.json safely.

    diff: dict with keys
        "add":    list of full entry dicts (each must have a unique "id")
        "remove": list of entry ids (strings) to delete
    Returns a result dict (also printed as JSON when run as CLI).
    """
    add = diff.get("add") or []
    remove = diff.get("remove") or []

    # ---- validate diff shape ----
    if not isinstance(add, list) or not isinstance(remove, list):
        raise ValueError("diff 的 add/remove 必须都是列表")
    for e in add:
        if not isinstance(e, dict) or not e.get("id"):
            raise ValueError("diff.add 中每个条目必须是含 'id' 的对象：%r" % (e,))

    container, is_wrapped, original = _load(models_path)
    in_count = len(container)
    existing_ids = {e.get("id") for e in container if isinstance(e, dict)}

    # ---- REMOVE (only ids that actually exist) ----
    remove_set = set(remove)
    removed = [e["id"] for e in container if isinstance(e, dict) and e.get("id") in remove_set]
    kept = [e for e in container if not (isinstance(e, dict) and e.get("id") in remove_set)]

    # ---- ADD (skip ids already present, including those just kept) ----
    kept_ids = {e.get("id") for e in kept if isinstance(e, dict)}
    added, skipped = [], []
    for e in add:
        eid = e.get("id")
        if eid in kept_ids:
            skipped.append(eid)
            continue
        kept.append(e)
        kept_ids.add(eid)
        added.append(eid)

    out_count = len(kept)

    # ---- invariant check ----
    expected = in_count + len(added) - len(removed)
    invariant_ok = (out_count == expected)

    # ---- duplicate id check on the result ----
    seen, dups = set(), []
    for e in kept:
        eid = e.get("id") if isinstance(e, dict) else None
        if eid in seen:
            dups.append(eid)
        seen.add(eid)

    result = {
        "models_path": models_path,
        "in_count": in_count,
        "out_count": out_count,
        "added": added,
        "skipped_already_present": skipped,
        "removed": removed,
        "invariant_ok": invariant_ok,
        "duplicate_ids": dups,
        "dry_run": dry_run,
        "written": False,
        "backup": None,
    }

    # Validate the JSON we would write (catches any structural problem early)
    candidate = _wrap(kept, is_wrapped, original if is_wrapped else None)
    json.dumps(candidate, ensure_ascii=False)

    if not invariant_ok or dups:
        # Never write when the math or uniqueness is off.
        result["error"] = (
            "拒绝写入：不变量或不变量校验失败"
            + ("（out=%d 但 in+add-remove=%d）" % (out_count, expected) if not invariant_ok else "")
            + ("；存在重复 id：%s" % dups if dups else "")
        )
        return result

    if dry_run:
        return result

    # ---- backup then write ----
    if backup:
        bak = models_path + ".bak"
        shutil.copy2(models_path, bak)
        result["backup"] = bak

    text = json.dumps(candidate, ensure_ascii=False, indent=2) + "\n"
    # Atomic-ish write: temp file in same dir, then replace.
    d = os.path.dirname(os.path.abspath(models_path))
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, models_path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
    result["written"] = True
    return result


def _cli():
    ap = argparse.ArgumentParser(description="免费模型审计员 — 安全应用差异到 models.json")
    ap.add_argument("--models", required=True, help="models.json 的绝对路径")
    ap.add_argument("--diff", required=True, help="差异文件 JSON 路径，含 add[] / remove[]")
    ap.add_argument("--dry-run", action="store_true", help="只计算并报告，不写文件")
    ap.add_argument("--no-backup", action="store_true", help="写前不做 .bak 备份（不推荐）")
    args = ap.parse_args()

    with open(args.diff, "r", encoding="utf-8") as f:
        diff = json.load(f)
    res = apply_diff(args.models, diff, dry_run=args.dry_run, backup=not args.no_backup)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if (res.get("written") or res.get("dry_run")) and not res.get("error") else 1)


if __name__ == "__main__":
    _cli()
