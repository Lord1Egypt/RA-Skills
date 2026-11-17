# -*- coding: utf-8 -*-
"""AI事故记录器：AI 事故一键入账（JSONL 台账）。零依赖。

三律映射：LGD-II 有证 —— 事故有据可查，复盘有本可翻。

用法：
  python ai_incident_log.py --add "bot把内部报价发给客户" --severity 2 \
      --model kefu-bot --action "已撤回+改提示词" --file incidents.jsonl
  python ai_incident_log.py --list --file incidents.jsonl
  python ai_incident_log.py --report --file incidents.jsonl
"""
import argparse, datetime, json, pathlib, sys

SEV = {1: "低（可自愈/无影响）", 2: "中（有影响已控制）", 3: "高（客诉/资损/合规）"}


def load(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser(description="AI事故记录器 · 事故台账")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--add", help="事故描述")
    g.add_argument("--list", action="store_true")
    g.add_argument("--report", action="store_true")
    ap.add_argument("--severity", type=int, choices=[1, 2, 3], default=2)
    ap.add_argument("--model", default="unknown", help="涉事模型/智能体")
    ap.add_argument("--action", default="待复盘", help="已采取措施")
    ap.add_argument("--owner", default="", help="记录人")
    ap.add_argument("--file", default="ai_incidents.jsonl", help="台账文件")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.file)
    p.parent.mkdir(parents=True, exist_ok=True)

    if a.add:
        rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
               "severity": a.severity, "severity_label": SEV[a.severity],
               "model": a.model, "desc": a.add, "action": a.action,
               "owner": a.owner or "未署名"}
        with p.open("a", encoding="utf-8-sig") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(("已入账 #%d" % len(load(p))) + f"（{rec['severity_label']}）")
        sys.exit(0)

    recs = load(p)
    if a.list:
        if not recs:
            print("台账为空")
        for i, r in enumerate(recs, 1):
            print(f"#{i} [{r.get('severity_label','?')}] {r.get('time','')} "
                  f"{r.get('model','')}：{r.get('desc','')}（处置：{r.get('action','')}）")
        sys.exit(0)

    # report
    by_sev, by_model, no_action = {}, {}, 0
    for r in recs:
        by_sev[r.get("severity_label", "?")] = by_sev.get(r.get("severity_label", "?"), 0) + 1
        by_model[r.get("model", "?")] = by_model.get(r.get("model", "?"), 0) + 1
        if r.get("action") in ("", "待复盘"):
            no_action += 1
    out = {"total": len(recs), "by_severity": by_sev, "by_model": by_model,
           "pending_review": no_action}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"事故总数：{len(recs)}")
        for k, v in by_sev.items():
            print(f"  {k}：{v}")
        print("按模型：")
        for k, v in sorted(by_model.items(), key=lambda x: -x[1]):
            print(f"  {k}：{v}")
        print(f"待复盘（未填处置）：{no_action}")
    sys.exit(0)


if __name__ == "__main__":
    main()
