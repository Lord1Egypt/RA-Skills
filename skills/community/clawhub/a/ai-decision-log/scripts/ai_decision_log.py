# -*- coding: utf-8 -*-
"""AI决策留痕器：AI 参与的决策一键留痕（JSONL）。零依赖。

三律映射：LGD-I 有籍 + LGD-II 有证 —— 谁、用哪个 AI、凭什么证据、谁人审。

用法：
  python ai_decision_log.py --add --decision "驳回该供应商" --model glm-x \
      --evidence dd_report.md --reviewer 张三 --file decisions.jsonl
  python ai_decision_log.py --report --file decisions.jsonl
"""
import argparse, datetime, json, pathlib, sys


def load(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser(description="AI决策留痕器 · 决策留痕")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--add", action="store_true", help="追加一条决策")
    g.add_argument("--list", action="store_true")
    g.add_argument("--report", action="store_true")
    ap.add_argument("--decision", default="", help="决策内容（--add 必填）")
    ap.add_argument("--model", default="unknown", help="使用的 AI/模型")
    ap.add_argument("--evidence", default="", help="证据（内联摘要/@文件/纯路径，记哈希前 12 位）")
    ap.add_argument("--reviewer", default="", help="人审人（空=无人审，report 重点标出）")
    ap.add_argument("--file", default="ai_decisions.jsonl")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.file)
    p.parent.mkdir(parents=True, exist_ok=True)

    if a.add:
        if not a.decision:
            print("--add 需 --decision", file=sys.stderr)
            sys.exit(2)
        import hashlib
        q = a.evidence[1:] if a.evidence.startswith("@") else a.evidence
        if q and pathlib.Path(q).is_file():
            ev = hashlib.sha256(pathlib.Path(q).read_bytes()).hexdigest()[:12] + "@" + pathlib.Path(q).name
        else:
            ev = hashlib.sha256((q or "no-evidence").encode()).hexdigest()[:12]
        rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
               "decision": a.decision, "model": a.model, "evidence": ev,
               "reviewer": a.reviewer or None}
        with p.open("a", encoding="utf-8-sig") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(("已留痕 #%d" % len(load(p))) + (f"（人审：{a.reviewer}）" if a.reviewer else "（⚠ 无人审）"))
        sys.exit(0)

    recs = load(p)
    if a.list:
        for i, r in enumerate(recs, 1):
            print(f"#{i} {r.get('time','')} {r.get('decision','')} "
                  f"[{r.get('model','')}] 证据:{r.get('evidence','')} "
                  f"人审:{r.get('reviewer') or '⚠无'}")
        if not recs:
            print("台账为空")
        sys.exit(0)

    by_model, no_review = {}, []
    for r in recs:
        by_model[r.get("model", "?")] = by_model.get(r.get("model", "?"), 0) + 1
        if not r.get("reviewer"):
            no_review.append(r.get("decision", "")[:30])
    out = {"total": len(recs), "by_model": by_model, "unreviewed": no_review}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"决策总数：{len(recs)}")
        for k, v in sorted(by_model.items(), key=lambda x: -x[1]):
            print(f"  {k}：{v}")
        print(f"无人审决策：{len(no_review)} 条" + ("（⚠ 高风险，须补人审）" if no_review else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
