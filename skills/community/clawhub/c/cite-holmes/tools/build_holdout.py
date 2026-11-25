#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.5.0 F58：留出集半自动构建管线（真实数据铁律的工装化）。

背景：独立留出集的铁律=每条 clean 条目经真实网络逐条核验后才能入集
（v6.2.0 曾因凭记忆书写 DOI 被真网处决 9 条）；此前该流程是手工逐条跑
引擎再誊写——本工具把它机制化，防止未来扩容再走「记忆书写」回头路。

两阶段：
  ① 草案：python3 tools/build_holdout.py --candidates cand.json --out draft.json
     真网逐条核验（verify_one 直调，逐条隔离——与 run_eval 同通路，不走
     CLI 批内缓存），产出每条的实测判定/关键字 note/建议标签：
       verified|partial → 建议 clean
       invalid|unreachable → 不建议 clean（须人工复核形态后作为 planted 候选）
     --expect-planted i,j 标记的条目反向断言（实测非 verified 才放行）。
  ② 冻结：python3 tools/build_holdout.py --draft draft.json --freeze out.json
     每条必须带人工确认的 reviewed 字段（"clean"|"planted"）——管线只出
     建议，冻结动作永远需要人（或代理）逐条拍板，防草案直通入集。

条目纪律（写进草案 header，冻结时校验）：
  - 批内 DOI 唯一（M5 教训：CLI 批内缓存按 DOI 复用判定，同 DOI 多条掩蔽
    腐蚀；run_eval 逐条隔离不受影响，但集合本身须对两种通路都诚实）；
  - clean 条目必须带可核验标识符（F55 静态锁同源）；
  - planted 条目必须写 planted_notes 形态说明（公开可查，F55 锁同源）。
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import verify_refs as vr  # noqa: E402


def _label(verdict: str) -> str:
    return "clean" if verdict in ("verified", "partial") else "review"


def _norm_doi(doi: str) -> str:
    """DOI 归一：strip+lower+剥常见包装形态（URL 前缀/doi: 前缀）——
    唯一性检查对异写法也生效（审计 P2：仅 strip+lower 可被 doi.org/ 前缀绕过）。"""
    d = str(doi or "").strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if d.startswith(p):
            d = d[len(p) :]
    return d.strip()


def build_draft(cand_path: str, out_path: str, expect_planted: str, timeout: float) -> int:
    cands = json.load(open(cand_path, encoding="utf-8"))
    refs = cands["refs"] if isinstance(cands, dict) else cands
    if isinstance(cands, dict) and cands.get("expect_planted"):
        planted_ids = {int(i) for i in cands["expect_planted"]}
    else:
        planted_ids = (
            {int(i) for i in expect_planted.split(",") if i.strip()} if expect_planted else set()
        )
    # 批内 DOI 唯一性前置检查（M5 教训：进集前先拦，不等 CLI 批内掩蔽）
    doi_seen, collisions = {}, []
    for i, r in enumerate(refs, 1):
        d = _norm_doi(r.get("doi"))
        if d:
            if d in doi_seen:
                collisions.append(f"#{i} 与 #{doi_seen[d]} 同 DOI {d}")
            doi_seen[d] = i
    if collisions:
        print("DOI 唯一性冲突（M5 批内缓存掩蔽风险，先改候选再核验）：")
        for c in collisions:
            print(f"  ✗ {c}")
        return 2
    entries, problems = [], []
    for i, ref in enumerate(refs, 1):
        r = vr.verify_one(ref, i, False, timeout, False)
        v, note = r["verdict"], r.get("note", "")
        sug = _label(v)
        status = "OK"
        if i in planted_ids:
            if v == "verified":
                status = "FAIL(预埋未捕获)"
                problems.append(i)
            sug = "planted"
        elif v in ("invalid", "unreachable"):
            status = f"REVIEW({v}——真实条目不应判死/不可达；转 planted 候选需人工确认)"
        entries.append(
            {
                "index": i,
                "ref": ref,
                "verdict": v,
                "note": note,
                "suggest": sug,
                "status": status,
            }
        )
        print(
            f"[{i}/{len(refs)}] {v:11s} → 建议 {sug:7s} "
            f"{str(ref.get('title') or ref.get('url') or '')[:46]}"
        )
    draft = {
        "description": f"留出集草案（build_holdout.py 真网逐条核验 "
        f"{vr.VERSION}）——suggest 是建议，冻结前逐条人工拍板 reviewed 字段",
        "engine_version": vr.VERSION,
        "entries": entries,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False, indent=2)
    n_clean = sum(1 for e in entries if e["suggest"] == "clean")
    print(
        f"\n草案已写：{out_path}（{len(entries)} 条：clean 建议 {n_clean}，"
        f"复核 {len(entries) - n_clean}）"
    )
    if problems:
        print(f"预埋未捕获：{problems}——形态或引擎问题，修完重跑")
        return 1
    return 0


def freeze(draft_path: str, out_path: str, description: str) -> int:
    d = json.load(open(draft_path, encoding="utf-8"))
    entries = d.get("entries") or []
    assert entries, "草案无条目"
    refs, expected, notes, missing = [], {}, {}, []
    for e in entries:
        rev = e.get("reviewed")
        if rev not in ("clean", "planted"):
            missing.append(str(e.get("index")))
            continue
        refs.append(e["ref"])
        expected[str(e["index"])] = rev
        if rev == "planted":
            nt = e.get("planted_note") or e.get("note", "")
            assert nt, f"#{e['index']} planted 缺形态说明（公开可查纪律）"
            notes[str(e["index"])] = nt
    if missing:
        print(
            f"冻结拦截：{len(missing)} 条未拍板 reviewed 字段：{','.join(missing)}"
            "（管线只出建议，冻结须逐条人工确认）"
        )
        return 2
    doc = {"description": description, "refs": refs, "expected": expected}
    if notes:
        doc["planted_notes"] = notes
    # 冻结面终检：DOI 唯一 + clean 带标识符（F55 静态锁同源）
    dois = [d for d in (_norm_doi(r.get("doi")) for r in refs) if d]
    if len(dois) != len(set(dois)):
        print("冻结拦截：批内 DOI 冲突（M5 教训）")
        return 2
    for i, r in enumerate(refs, 1):
        if expected[str(i)] == "clean" and not any(
            str(r.get(k) or "").strip() for k in ("doi", "pmid", "arxiv", "url")
        ):
            print(f"冻结拦截：clean #{i} 无可核验标识符")
            return 2
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"已冻结：{out_path}（{len(refs)} 条，planted {len(notes)}）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="留出集半自动构建管线（F58）")
    ap.add_argument(
        "--candidates", default="", help="候选集 JSON（refs 数组；可含 expect_planted）"
    )
    ap.add_argument(
        "--expect-planted",
        default="",
        help="预埋条目序号（逗号分隔；候选文件内 expect_planted 优先）",
    )
    ap.add_argument("--draft", default="", help="草案输出/输入路径")
    ap.add_argument("--freeze", default="", help="冻结输出路径（入 examples/holdout_*.json）")
    ap.add_argument("--description", default="", help="冻结集 description 文案")
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()
    if args.candidates and args.draft:
        return build_draft(args.candidates, args.draft, args.expect_planted, args.timeout)
    if args.draft and args.freeze:
        return freeze(args.draft, args.freeze, args.description)
    print(
        "用法：--candidates+--draft（草案）｜--draft+--freeze（冻结）；"
        "两阶段分离，冻结须逐条 reviewed",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
