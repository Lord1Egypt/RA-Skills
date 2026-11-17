#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Golden 回归校验：以官方《更正事项》为 ground truth，量化 skill 召回率。

为什么需要它：招标文件比对最容易犯「静默漏检」——小幅度数值/关键词修订被
相似度阈值一刀切跳过（已修），但肉眼看报告很难发现漏了几条。本脚本把官方
更正事项当标准答案，每次改完 skill 自动跑一遍，给出「自动可检项召回率」，
比人工比对报告可靠得多。

用法：
  # 1) 直接校验已生成的 diff.json
  python golden_regression.py --golden references/golden_longling_4vs5.json \
                              --diff workdir/diff.json

  # 2) 跑完整管线（extract + align）后再校验
  python golden_regression.py --golden references/golden_longling_4vs5.json \
                              --files A.docx B.docx --workdir workdir

退出码：自动可检项全部命中 -> 0；有未命中 -> 1。
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)


def _load_golden(path):
    d = json.load(open(path, encoding="utf-8"))
    return d.get("items", []), d.get("meta", {})


def _build_blob(diff):
    """把所有差异文本拼成一个可检索 blob（old/new 文本都纳入）。"""
    chunks = []
    for grp in ("modified", "added", "deleted"):
        for it in diff.get(grp, []):
            if it.get("old_text"):
                chunks.append(it["old_text"])
            if it.get("new_text"):
                chunks.append(it["new_text"])
    return "\n".join(chunks)


def _check(items, blob):
    rows = []
    auto_total = 0
    auto_caught = 0
    for it in items:
        probes = it.get("probes", [])
        if it.get("format_only"):
            rows.append((it["id"], "SKIP", "已知格式限制（不计入召回）"))
            continue
        auto_total += 1
        hit = [(p, blob.count(p)) for p in probes if p in blob]
        if hit:
            auto_caught += 1
            detail = "命中探针: " + ", ".join(f"{p}[{c}]" for p, c in hit)
            rows.append((it["id"], "CAUGHT", detail))
        else:
            rows.append((it["id"], "MISSED", "未命中任何探针: " + " / ".join(probes)))
    return rows, auto_total, auto_caught


def _run_pipeline(files, workdir):
    """调用 extract_documents + align_clauses 跑完整管线，返回 diff dict。"""
    sys.path.insert(0, HERE)
    import extract_documents as ext
    import align_clauses as aln

    os.makedirs(workdir, exist_ok=True)
    docs = []
    for f in files:
        low = f.lower()
        if low.endswith(".docx"):
            docs.append(ext.extract_docx(f))
        elif low.endswith(".pdf"):
            docs.append(ext.extract_pdf(f))
        else:
            docs.append(ext.extract_txt(f))
    # 数据质量检查：任一文件不可解析则终止管线并友好提示
    for d in docs:
        if d.get("meta", {}).get("parse_status") == "failed":
            sys.stderr.write(
                f"[ERROR] 文件解析失败: {d['meta'].get('file')} — {d['meta'].get('parse_error', '')}\n"
                f"[HINT] {d.get('data_gap', '请检查文件后重试')}\n"
            )
            sys.exit(2)
    extracted_path = os.path.join(workdir, "extracted.json")
    with open(extracted_path, "w", encoding="utf-8") as fh:
        json.dump({"documents": docs}, fh, ensure_ascii=False, indent=2)
    a, b = docs[0]["clauses"], docs[1]["clauses"]
    modified, added, deleted = aln.align(a, b)
    diff = {
        "old_file": docs[0]["meta"].get("file", "A"),
        "new_file": docs[1]["meta"].get("file", "B"),
        "summary": {
            "A_clauses": len(a), "B_clauses": len(b),
            "modified": len(modified), "added": len(added),
            "deleted": len(deleted),
            "total_changes": len(modified) + len(added) + len(deleted),
        },
        "modified": modified, "added": added, "deleted": deleted,
    }
    diff_path = os.path.join(workdir, "diff.json")
    with open(diff_path, "w", encoding="utf-8") as fh:
        json.dump(diff, fh, ensure_ascii=False, indent=2)
    return diff, diff_path


def main():
    ap = argparse.ArgumentParser(description="golden 召回率回归校验")
    ap.add_argument("--golden", required=True, help="golden 标注 JSON")
    ap.add_argument("--diff", help="直接校验的 diff.json（跳过管线）")
    ap.add_argument("--files", nargs=2, help="跑完整管线用的 A/B 文档")
    ap.add_argument("--workdir", default=".", help="完整管线输出目录")
    args = ap.parse_args()

    items, meta = _load_golden(args.golden)
    if not items:
        sys.stderr.write("golden 数据集为空\n")
        sys.exit(2)

    if args.diff:
        diff = json.load(open(args.diff, encoding="utf-8"))
        src = args.diff
    elif args.files:
        diff, src = _run_pipeline(args.files, args.workdir)
    else:
        sys.stderr.write("需提供 --diff 或 --files\n")
        sys.exit(2)

    blob = _build_blob(diff)
    rows, auto_total, auto_caught = _check(items, blob)

    print("=" * 72)
    print("GOLDEN 回归校验:", meta.get("name", args.golden))
    print("diff 来源:", src)
    print("diff 差异总数:", diff.get("summary", {}).get("total_changes", "?"),
          diff.get("summary", {}))
    print("-" * 72)
    print(f"{'ID':<5}{'状态':<8}{'说明'}")
    print("-" * 72)
    for rid, status, detail in rows:
        print(f"{rid:<5}{status:<8}{detail}")
    print("-" * 72)
    skip = sum(1 for r in rows if r[1] == "SKIP")
    recall = (auto_caught / auto_total * 100) if auto_total else 100.0
    print(f"自动可检项: {auto_caught}/{auto_total} 命中  ->  召回率 {recall:.1f}%")
    print(f"已知格式限制(SKIP): {skip} 项（不计入召回分母）")
    print("=" * 72)

    if auto_total and auto_caught == auto_total:
        print("✅ PASS：全部自动可检项召回")
        sys.exit(0)
    else:
        print("❌ FAIL：存在未召回的自动可检项")
        sys.exit(1)


if __name__ == "__main__":
    main()
