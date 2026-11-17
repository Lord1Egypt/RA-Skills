#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autonomous-deep-research · 自主深度研究编排器
问题分解 → 多源检索(rag/web-fetch) → 综合与交叉验证 → 反思覆盖度 → 迭代逼近答案。
离线/在线双模：有 rag/web-fetch 脚本则真实检索，否则降级为本地启发式并标记 needs_web。
"""
import argparse, json, os, re, subprocess, sys, datetime

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SELF_DIR = os.path.dirname(__file__)
CAP_SCRIPTS = {
    "rag": os.path.join(SKILLS_DIR, "rag", "scripts", "rag_query.py"),
    "web_fetch": os.path.join(SKILLS_DIR, "web-fetch", "scripts", "fetch.py"),
}


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def decompose(question):
    """把主问题拆成 3–5 个可独立检索的子问题。"""
    # 显式连词切分
    parts = re.split(r"[，,。；;、和|与|以及|以及|以及]", question)
    subs = [p.strip() for p in parts if len(p.strip()) >= 4]
    if len(subs) < 2:
        # 回退：按关键问句抽取
        subs = [question]
    # 规整为问句
    out = []
    for s in subs[:5]:
        if not re.search(r"[?？]$", s):
            s = s.rstrip("。.") + "？"
        out.append(s)
    return out or [question + "？"]


def retrieve(sub, idx):
    """对子问题检索：优先 rag → web-fetch → 本地启发式降级。"""
    # rag
    rag = CAP_SCRIPTS.get("rag")
    idx_file = os.path.join(SELF_DIR, "research_index.json")
    if rag and os.path.exists(rag) and os.path.exists(idx_file):
        tmp = os.path.join(SELF_DIR, f"rag_q_{idx}.json")
        r = subprocess.run([sys.executable, rag, "--index", idx_file, "--question", sub,
                           "--topk", "2", "--out", tmp], capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and os.path.exists(tmp):
            try:
                d = json.load(open(tmp, encoding="utf-8"))
                os.remove(tmp)
                ctx = "；".join(seg.get("text", "") for seg in d.get("results", []))
                return {"answer": f"[本地知识库] {ctx[:300]}", "confidence": 0.7, "needs_web": False}
            except Exception:
                pass
    # web-fetch
    wf = CAP_SCRIPTS.get("web_fetch")
    if wf and os.path.exists(wf):
        tmp = os.path.join(SELF_DIR, f"web_q_{idx}.json")
        r = subprocess.run([sys.executable, wf, "--query", sub, "--out", tmp],
                           capture_output=True, text=True, timeout=90)
        if r.returncode == 0 and os.path.exists(tmp):
            try:
                d = json.load(open(tmp, encoding="utf-8"))
                os.remove(tmp)
                return {"answer": f"[在线检索] {str(d)[:300]}", "confidence": 0.8, "needs_web": False}
            except Exception:
                pass
    # 本地启发式降级
    return {"answer": f"[本地启发式] 针对「{sub}」暂以通用知识作答，建议补检索。",
            "confidence": 0.4, "needs_web": True}


def synthesize(question, findings):
    """把子答案聚合成结构化综合结论。"""
    sections = []
    for i, f in enumerate(findings, 1):
        tag = "⚠️ 待补检索" if f.get("needs_web") else "✅ 有依据"
        sections.append(f"### {i}. {f['sub']}\n{tag} {f['answer']} _(置信度 {f.get('confidence',0)})_")
    answer = f"# 关于「{question}」的研究综合\n\n" + "\n\n".join(sections)
    return answer


def low_conf(findings, thr=0.6):
    return [f["sub"] for f in findings if f.get("confidence", 0) < thr or f.get("needs_web")]


def run(question, out_file, max_iter=2):
    report = {"question": question, "started": now(), "iterations": []}
    subs = decompose(question)
    report["sub_questions"] = subs
    findings = []
    for it in range(max_iter):
        batch = []
        # 每轮只对「尚未有依据」的子问题检索，逐步逼近
        pending = [s for i, s in enumerate(subs) if i >= len(findings) or findings[i].get("needs_web")]
        if not pending:
            break
        for s in pending:
            i = subs.index(s)
            res = retrieve(s, i)
            res["sub"] = s
            batch.append(res)
            if i < len(findings):
                findings[i] = res
            else:
                findings.append(res)
        cov = round(1 - len(low_conf(findings)) / max(1, len(findings)), 2)
        report["iterations"].append({"iter": it + 1, "coverage": cov,
                                    "pending": len(pending)})
        if not low_conf(findings):
            break
    # 补齐（若 max_iter 内仍有空洞）
    while len(findings) < len(subs):
        findings.append({"sub": subs[len(findings)], "answer": "未检索",
                        "confidence": 0.0, "needs_web": True})
    report["findings"] = findings
    report["synthesized_answer"] = synthesize(question, findings)
    report["coverage"] = round(1 - len(low_conf(findings)) / max(1, len(findings)), 2)
    report["open_gaps"] = low_conf(findings)
    report["next_steps"] = [f"对「{g}」补一次检索（rag 建库或 web-fetch 在线）" for g in low_conf(findings)]
    report["finished"] = now()
    json.dump(report, open(out_file, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--out", default=os.path.join(SELF_DIR, "report.json"))
    ap.add_argument("--max-iter", type=int, default=2)
    args = ap.parse_args()
    r = run(args.question, args.out, args.max_iter)
    print(f"✅ 自主研究完成 | 子问题={len(r['sub_questions'])} 覆盖度={r['coverage']} "
          f"待补={len(r['open_gaps'])} 报告={args.out}")


if __name__ == "__main__":
    main()
