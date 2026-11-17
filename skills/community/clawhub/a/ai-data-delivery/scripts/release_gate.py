#!/usr/bin/env python3
"""Scope-specific gates. Missing, stale, unknown or failed evidence never passes."""
import argparse
from pathlib import Path
import subprocess
import sys
import os

from _contract import binding_errors, digest, evidence, load, minimal_env, snapshot, write
from _evaluation import valid_waiver
from check_constraints import check_all
from check_join_graph import analyze
from run_eval import load_cases

HERE = Path(__file__).resolve().parent


def run_gate(name, command):
    result = subprocess.run([sys.executable, str(HERE / command[0]), *command[1:]],
                            capture_output=True, text=True, encoding="utf-8", errors="replace",
                            env=minimal_env())
    return {"gate": name, "status": "pass" if result.returncode == 0 else "fail",
            "detail": "\n".join((result.stdout + result.stderr).splitlines()[-5:])}


def assess_eval(report, model, cases_path, minimum=1.0, max_age=24, multihop=None):
    errors = binding_errors(report, model, cases_path, max_age)
    cases = load_cases(cases_path)
    if multihop:
        cases += load_cases(multihop)
    expected_multi = digest(multihop) if multihop else None
    if report.get("evidence", {}).get("multihop_sha256") != expected_multi:
        errors.append("multihop evidence mismatch")
    records = report.get("records", report.get("cases", []))
    ids = [c.get("id") for c in cases]
    actual_ids = [r.get("id") for r in records]
    if not cases or len(set(ids)) != len(ids) or sorted(ids) != sorted(actual_ids):
        errors.append("case coverage/identity mismatch or empty suite")
    index = {c["id"]: c for c in cases}
    passed, judged, waived = 0, 0, 0
    for record in records:
        case = index.get(record.get("id"), {})
        if record.get("declared"):
            if case.get("expect_reject") or (case.get("expect") or {}).get("type") == "refusal":
                errors.append("refusal cases cannot be waived")
            if record.get("pass") is not False or not valid_waiver(case) or record.get("waiver") != case.get("declared_conflict"):
                errors.append("invalid/stale waiver: " + str(record.get("id")))
            waived += 1
        elif record.get("pass") is True or record.get("pass") is False:
            judged += 1
            passed += record["pass"] is True
            refusal = case.get("expect_reject") or (case.get("expect") or {}).get("type") == "refusal"
            if refusal and not record["pass"]:
                errors.append("required refusal failed: " + str(record.get("id")))
        else:
            errors.append("unknown case: " + str(record.get("id")))
    if not judged or passed / judged < minimum:
        errors.append("insufficient evaluated cases/accuracy")
    summary = report.get("summary", {})
    if report.get("evidence", {}).get("mode") not in {"live", "offline", "mock"}:
        errors.append("unknown evaluation mode")
    if summary.get("passed") != passed or summary.get("total") != judged or summary.get("declared", 0) != waived:
        errors.append("summary inconsistent with records")
    return {"gate": "evaluation", "status": "fail" if errors else ("waived" if waived else "pass"),
            "errors": errors, "passed": passed, "evaluated": judged, "waived": waived,
            "mode": report.get("evidence", {}).get("mode")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--eval-report")
    ap.add_argument("--db", help="current SQLite snapshot; required for validated/production")
    ap.add_argument("--profile", choices=["static", "validated", "production"], default="validated")
    ap.add_argument("--endpoint")
    ap.add_argument("--min-acc", type=float, default=1.0)
    ap.add_argument("--max-age-hours", type=float, default=24)
    ap.add_argument("--log", default="release_log.yaml")
    ap.add_argument("--out", help="current gate report JSON")
    ap.add_argument("--results", help="gold_results file used during evaluation")
    ap.add_argument("--multihop")
    ap.add_argument("--session", help="optional scoped onboarding session to enforce unresolved blockers")
    args = ap.parse_args()
    if not 0 < args.min_acc <= 1 or args.max_age_hours <= 0:
        ap.error("min-acc must be (0,1], max-age-hours > 0")
    try:
        model = load(args.model)
        from _contract import top_shape_error
        shape_err = top_shape_error(model)
        if shape_err:
            print(f"gate error (not passed): {shape_err}\n"
                  f"先运行 check_model.py -f {args.model} 按提示修正模型结构。", file=sys.stderr)
            return 2
        gates = [run_gate("model", ["check_model.py", "-f", args.model])]
        lint_cmd = ["gold_lint.py", "--cases", args.cases, "--model", args.model]
        if args.results:
            lint_cmd += ["--results", args.results]
        gates.append(run_gate("gold", lint_cmd))
        if args.multihop:
            gates.append(run_gate("gold_multihop", ["gold_lint.py", "--cases", args.multihop, "--model", args.model]))
        if args.session:
            from guide_model import blockers
            from _contract import object_digest
            session = load(args.session)
            gaps = blockers(session)
            matched = object_digest(session["model"]) == object_digest(model)
            gates.append({"gate": "semantic_decisions", "status": "pass" if matched and not gaps else "unknown", "blockers": gaps, "model_matched": matched})
        data_hash, mode = None, "static"
        if args.profile == "static":
            gates.extend({"gate": name, "status": "not_applicable", "detail": "outside static profile"}
                         for name in ("evaluation", "data_constraints", "join_graph", "stability"))
        else:
            report = load(args.eval_report) if args.eval_report else None
            if report:
                eval_gate = assess_eval(report, args.model, args.cases, args.min_acc, args.max_age_hours, args.multihop)
                expected_results = digest(args.results) if args.results else None
                if report.get("evidence", {}).get("gold_results_sha256") != expected_results:
                    eval_gate.update(status="fail")
                    eval_gate["errors"].append("gold results binding mismatch")
                gates.append(eval_gate)
                mode = report.get("evidence", {}).get("mode", "unknown")
            else:
                gates.append({"gate": "evaluation", "status": "unknown", "detail": "missing --eval-report"})
            if args.db:
                conn, data_hash = snapshot(args.db)
                try:
                    for name, result in (("data_constraints", check_all(model, conn)), ("join_graph", analyze(model, conn))):
                        gates.append({"gate": name, "status": result["status"], "report": result})
                finally:
                    conn.close()
                bound = bool(report and report.get("evidence", {}).get("data_snapshot_sha256") == data_hash)
                gates.append({"gate": "data_binding", "status": "pass" if bound else "unknown", "detail": "evaluation must bind this current data snapshot"})
            else:
                gates.append({"gate": "data", "status": "unknown", "detail": "missing --db"})
            if args.profile == "production":
                live = bool(args.endpoint and mode == "live" and report and report.get("evidence", {}).get("endpoint") == args.endpoint)
                gates.append({"gate": "live_evidence", "status": "pass" if live else "unknown"})
                if args.endpoint:
                    gates.append(run_gate("stability", ["plan_stability.py", "--endpoint", args.endpoint, "--cases", args.cases, "--times", "3", "--limit", "10"]))
                else:
                    gates.append({"gate": "stability", "status": "unknown", "detail": "missing endpoint"})
            else:
                gates.append({"gate": "stability", "status": "not_applicable", "detail": "validated profile is not production readiness"})
        acceptable = {"pass", "waived", "not_applicable"}
        hints = {
            "model": "模型 lint 未过：先 check_model.py -f <模型> 逐项修 ERROR 再跑门禁",
            "evaluation": "缺/过期/失配评测报告：先 run_eval 生成绑定当前模型+用例+快照的报告，再重跑门禁",
            "data_constraints": "约束未通过或未声明：在模型 constraints 段补声明后重跑 check_constraints；空 records 视为未验证而非通过",
            "join_graph": "关联键/扇出检查未过：check_join_graph 逐项看 from_key/to_key 唯一性与 fanout",
            "data_binding": "评测报告未绑定当前数据快照：用同一 --db 重跑 run_eval 与本门禁",
            "data": "缺 --db：validated/production 档必须给当前 SQLite 快照",
            "live_evidence": "缺 live 证据：--endpoint 与 mode=live 的评测报告缺一不可",
            "stability": "计划稳定性抽查未过/未跑：plan_stability 同句连跑比对 SQL 哈希",
            "semantic_decisions": "存在未清零缺口或会话模型失配：guide_model status 看 outstanding，清零后再来",
        }
        for g in gates:
            if g["status"] not in acceptable and g["gate"] in hints:
                g["hint"] = hints[g["gate"]]
        ready = all(g["status"] in acceptable for g in gates)
        waived = any(g["status"] == "waived" for g in gates)
        decision = (("static_ready" if args.profile == "static" else args.profile + "_" + mode)
                    + ("_with_waivers" if waived else "")) if ready else "not_ready"
        result = {"status": "pass_with_waivers" if ready and waived else ("pass" if ready else "not_ready"),
                  "decision": decision, "profile": args.profile, "gates": gates,
                  "model_version": model.get("version"), "min_acc": args.min_acc,
                  "scope": "technical evidence only; business acceptance, access control, deployment and source freshness require separate confirmation",
                  "evidence": evidence(args.model, args.cases, mode=mode, data_snapshot_sha256=data_hash)}
        log = load(args.log) if Path(args.log).exists() else []
        if not isinstance(log, list):
            raise ValueError("release log must be a list")
        write(args.log, log + [result])
        if args.out:
            write(args.out, result)
        for gate in gates:
            line = f"[{gate['status']}] {gate['gate']}"
            if gate.get("hint"):
                line += f" —— {gate['hint']}"
            print(line)
        print("decision: " + decision)
        return 0 if ready else 1
    except Exception as exc:
        print(f"gate error (not passed): {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
