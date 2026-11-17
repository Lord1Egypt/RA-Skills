#!/usr/bin/env python3
"""run_eval.py — 回归比对器（ai-data-delivery v0.0.5，双模式）

模式 A · 活引擎（FDE 日常：改完一键回归）
  python run_eval.py --endpoint http://localhost:7100 --cases cases.json \
      [--gold-results gold_results.json] [--multihop multihop.json] [--out report.json]
  逐条 POST {endpoint}/api/ask，比对标量/行集合/拒绝判定，
  失败明细带 SQL 与推理链（route/value/sql/reasoning 全留痕）。

模式 B · 离线文件比对（无引擎环境 / CI 存档比对）
  python run_eval.py --gold gold.yaml --actual actual.jsonl [--report report.json]

用例格式自动识别（三种兼容）：
  fmt1  {"id","question","expect":{"type":"scalar|rows|refusal","value|rows","tolerance"}}
  fmt2  {"id","question","gold_rows":[[...]],"expect_reject":false}
  fmt3  {"id","question","gold_sql":"...","expect_table":"..."}  —— 需 --gold-results 提供期望行

声明式冲突：需要 ref/note/owner/expires_on/case_ids；无效或过期声明仍计入失败。
有效豁免单列，不计入 acc；不等于全部通过或业务验收。发布门禁不允许豁免拒答失败。
报告可用 --model/--db 绑定证据；缺绑定不能用于 validated 门禁。

actual 文件（模式 B）：jsonl/yaml/json，每条形如
  {"id":"q001","value":123,"rows":null,"refused":false}

退出码：0 = 非空有效用例通过（有效豁免单列）；1 = 失败/未知/无有效用例；2 = 用法错误。
"""
import os
import argparse
import json
import math
import sys

import yaml

from _contract import guard_endpoint
from _network import safe_json, response_error


# ---------- 载入 ----------

def load_structured(path):
    path = os.fspath(path)
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(f)
        return json.load(f)


def load_cases(path):
    data = load_structured(path)
    if isinstance(data, dict):
        for key in ("cases", "gold_results"):
            if key in data:
                return data[key]
        raise ValueError(f"用例文件缺少 cases/gold_results 键：{path}")
    return data


def load_actual_map(path):
    path = os.fspath(path)
    if path.endswith(".jsonl"):
        out = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    item = json.loads(line)
                    out[item["id"]] = item
        return out
    data = load_structured(path)
    if isinstance(data, dict):
        data = data.get("results", data.get("cases", data))
        if isinstance(data, dict):  # {id: record} 形态（如 gold_results.json）
            return data
    return {item["id"]: item for item in data}


# ---------- 断言归一 ----------

def norm_number(x):
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(str(x).replace(",", "").strip())
    except (ValueError, AttributeError):
        return x


def cmp_scalar(expected, actual, tol=1e-6):
    e, a = norm_number(expected), norm_number(actual)
    if isinstance(e, float) and isinstance(a, float):
        if math.isclose(e, a, rel_tol=tol, abs_tol=tol):
            return True, ""
        return False, f"期望 {e}，实际 {a}"
    ok = e == a
    return ok, "" if ok else f"期望 {e!r}，实际 {a!r}"


def norm_row(row):
    if isinstance(row, dict):
        return tuple(norm_number(v) for v in row.values())
    if isinstance(row, (list, tuple)):
        return tuple(norm_number(v) for v in row)
    return (norm_number(row),)


def cmp_rows(expected_rows, actual_rows):
    """多重集合比对：顺序无关，重复行计数敏感。"""
    if actual_rows is None:
        return False, "实际结果无 rows"
    exp = sorted(map(repr, (norm_row(r) for r in expected_rows)))
    act = sorted(map(repr, (norm_row(r) for r in actual_rows)))
    if exp == act:
        return True, ""
    missing = [r for r in exp if r not in act]
    extra = [r for r in act if r not in exp]
    return False, f"行集合不一致：缺少 {missing[:3]}，多出 {extra[:3]}"


# ---------- 用例期望归一（三种格式 → 统一 expect） ----------

def unify_expect(case, gold_results):
    """返回 dict：{kind: refusal|rows|scalar|sql_rows|none, value?, rows?, tolerance?}"""
    if "expect" in case and isinstance(case["expect"], dict):  # fmt1
        e = case["expect"]
        return {"kind": e.get("type", "scalar"), "value": e.get("value"),
                "rows": e.get("rows"), "tolerance": float(e.get("tolerance", 1e-6))}
    if case.get("expect_reject"):  # fmt2 refusal
        return {"kind": "refusal"}
    et = str(case.get("expect_table") or "")
    if "拒绝" in et or "追问" in et:  # 拒绝标记位（如 expect_table: 应拒绝/追问）
        return {"kind": "refusal"}
    if case.get("gold_rows") is not None:  # fmt2
        rows = case["gold_rows"]
        if len(rows) == 1 and len(rows[0]) == 1:
            return {"kind": "scalar", "value": rows[0][0]}
        return {"kind": "rows", "rows": rows}
    if isinstance(case.get("gold_results"), list) and case["gold_results"]:  # 用例行内结果（多跳集）
        rows = case["gold_results"]
        if len(rows) == 1 and len(rows[0]) == 1:
            return {"kind": "scalar", "value": rows[0][0]}
        return {"kind": "rows", "rows": rows}
    if case.get("gold_sql"):  # fmt3
        rec = (gold_results or {}).get(case["id"])
        if rec and rec.get("rows") is not None:
            rows = rec["rows"]
            if len(rows) == 1 and len(rows[0]) == 1:
                return {"kind": "scalar", "value": rows[0][0]}
            return {"kind": "rows", "rows": rows}
        return {"kind": "sql_only"}  # 有 SQL 无结果：只做可回答性检查
    return {"kind": "none"}


# ---------- 模式 A：活引擎 ----------

def ask(endpoint, question, timeout=30, allow_remote=False):
    try:
        result = safe_json(endpoint.rstrip("/") + "/api/ask", {"question": question}, timeout=timeout, allow_remote=allow_remote)
        return result if isinstance(result, dict) else {"error": "接口响应必须是 JSON 对象"}
    except Exception as e:
        return {"error": str(e)}


def check_forbidden(case, *payloads):
    """answer_must_not_contain：答案/行集/SQL 中不得出现禁用词（来源通常是概念 forbidden）。"""
    forbidden = case.get("answer_must_not_contain") or []
    if not forbidden:
        return []
    haystack = " ".join(str(p) for p in payloads if p is not None)
    return [w for w in forbidden if str(w) in haystack]


def judge_live(resp, expect, case=None):
    """活引擎响应 × 统一期望 → (pass|None, detail)。pass=None 表示无法判定。"""
    error = response_error(resp, allow_refusal=True, require_result=expect["kind"] in {"scalar", "rows"})
    if error:
        return False, error
    refused = bool(resp.get("rejected") or resp.get("refused") or str(resp.get("status", "")).lower() in {"rejected", "refused"})
    kind = expect["kind"]
    if kind == "none":
        # 期望不明绝不臆断：无论引擎应答还是拒答，都只能 skip 并汇总告警
        return None, "无期望定义（跳过判定）——请补 expect/expect_reject/gold_rows/gold_sql 之一"
    if kind == "refusal":
        return (True, "") if refused else (False, "期望拒绝，但引擎给出了答案")
    if refused:
        return False, "引擎拒绝了，但期望给出答案"
    if kind == "scalar":
        ok, why = cmp_scalar(expect["value"], resp.get("value"), expect.get("tolerance", 1e-6)) \
            if resp.get("value") is not None or ("value" in resp and resp.get("rows") is None) else \
            cmp_rows([[expect["value"]]], resp.get("rows"))
    elif kind == "rows":
        ok, why = cmp_rows(expect["rows"], resp.get("rows"))
    elif kind == "sql_only":
        return None, "仅有 SQL 无期望结果，需 --gold-results；可回答性不证明正确性"
    else:
        return None, "无期望定义（跳过判定）"
    if ok and case is not None:
        hits = check_forbidden(case, resp.get("value"), resp.get("rows"), resp.get("sql"))
        if hits:
            return False, f"答案含禁用词：{hits}"
    return ok, why


def apply_declared(case, ok, why):
    """声明式冲突处理：返回 (declared, why)。declared=True 表示失败被声明豁免。"""
    conf = case.get("declared_conflict")
    if not conf or ok is None:
        return False, why
    if ok is True:
        return False, "声明冲突但实测通过——冲突或已消解，建议移除 declared_conflict 标记"
    from _evaluation import valid_waiver
    if not valid_waiver(case):
        return False, f"无效/过期豁免（需 ref、note、owner、expires_on、case_ids）：{why}"
    if isinstance(conf, dict):
        ref, note = conf.get("ref"), conf.get("note")
        tag = f"已声明冲突（{ref or '⚠ 无出处引用'}）"
        return True, f"{tag}：{note or why}"
    return True, f"已声明冲突（⚠ 无出处引用）：{conf}；实测：{why}"


def run_live(args):
    from _evaluation import report_evidence
    ev = report_evidence(args, args.cases)
    cases = load_cases(args.cases)
    gold_results = load_actual_map(args.gold_results) if args.gold_results else None
    suites = [("main", cases)]
    if args.multihop:
        suites.append(("multihop", load_cases(args.multihop)))

    records = []
    for label, suite in suites:
        for c in suite:
            expect = unify_expect(c, gold_results)
            resp = ask(args.endpoint, c["question"], allow_remote=getattr(args, "allow_remote", False))
            ok, why = judge_live(resp, expect, c)
            declared, why = apply_declared(c, ok, why)
            records.append({
                "id": c["id"], "type": c.get("type", label), "pass": ok, "why": why,
                "declared": declared or None, "waiver": c.get("declared_conflict") if declared else None,
                "route": "reject" if resp.get("rejected") or resp.get("refused")
                         else ("table" if resp.get("rows") else "scalar"),
                "value": resp.get("value"), "sql": resp.get("sql"),
                "reasoning": resp.get("reasoning")})
            mark = "DECL" if declared else ("pass" if ok else ("skip" if ok is None else "FAIL"))
            print(f"{c['id']} [{label}] {mark}  {c['question'][:32]}"
                  + ("" if ok and not why else f"  << {why}" if why else ""))

    judged = [r for r in records if r["pass"] is not None]
    unknown = [r for r in records if r["pass"] is None]
    declared = [r for r in judged if r.get("declared")]
    effective = [r for r in judged if not r.get("declared")]
    passed = sum(1 for r in effective if r["pass"])
    by_type = {}
    for r in effective:
        t = by_type.setdefault(r["type"] or "main", [0, 0])
        t[1] += 1
        t[0] += bool(r["pass"])
    summary = {"total": len(effective), "passed": passed,
               "acc": round(passed / len(effective), 4) if effective else 0,
               "unknown": len(unknown),
               "declared": len(declared),
               "declared_cases": [{"id": r["id"], "why": r["why"]} for r in declared],
               "by_type": {k: {"pass": v[0], "total": v[1], "acc": round(v[0] / v[1], 4)}
                           for k, v in sorted(by_type.items())},
               "failures": [r for r in effective if not r["pass"]]}
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        from _evaluation import report_evidence
        summary["all_cases"] = len(records)
        json.dump({"summary": summary, "records": records,
                   "evidence": ev}, f, ensure_ascii=False, indent=1)
    if unknown:
        print(f"\n⚠ {len(unknown)} 条用例期望不明（未计入 acc）："
              f"{[r['id'] for r in unknown]}")
        print("  这些用例既无 expect/expect_reject/gold_rows/gold_sql，也未标拒绝标记——"
              "请补齐期望后重跑，否则等于没测。")
    if declared:
        print(f"\n◆ {len(declared)} 条声明式冲突未计入 acc（豁免留痕）："
              f"{[r['id'] for r in declared]}")
        noref = [r["id"] for r in declared if "无出处引用" in (r["why"] or "")]
        if noref:
            print(f"  ⚠ 其中 {len(noref)} 条缺决策出处 ref：{noref}——"
                  "无留痕的豁免是后门，请补 declared_conflict.ref 指向评审纪要/决策日志")
    print("\n==== SUMMARY ====")
    print(json.dumps(summary, ensure_ascii=False, indent=1, default=str)[:2000])
    return 0 if effective and not unknown and passed == len(effective) else 1


# ---------- 模式 B：离线文件比对 ----------

def judge_file(case, actual):
    expect = unify_expect(case, None)
    kind = expect["kind"]
    if kind == "none":
        return None, "无期望定义（跳过判定）"
    if actual is None:
        return False, "无实际输出（引擎未返回该用例）"
    error = response_error(actual, allow_refusal=True, require_result=kind in {"scalar", "rows"})
    if error:
        return False, error
    refused = bool(actual.get("refused") or actual.get("rejected") or str(actual.get("status", "")).lower() in {"rejected", "refused"})
    if kind == "refusal":
        return (True, "") if refused else (False, "期望拒绝，但引擎给出了答案")
    if refused:
        return False, "引擎拒绝了，但期望给出答案"
    if kind == "scalar":
        ok, why = cmp_scalar(expect["value"], actual.get("value"), expect.get("tolerance", 1e-6)) \
            if actual.get("value") is not None or ("value" in actual and actual.get("rows") is None) else \
            cmp_rows([[expect["value"]]], actual.get("rows"))
    elif kind == "rows":
        ok, why = cmp_rows(expect["rows"], actual.get("rows"))
    else:
        return False, f"离线模式不支持的断言类型：{kind}"
    if ok:
        hits = check_forbidden(case, actual.get("value"), actual.get("rows"), actual.get("sql"))
        if hits:
            return False, f"答案含禁用词：{hits}"
    return ok, why


def run_offline(args):
    from _evaluation import report_evidence
    ev = report_evidence(args, args.gold)
    cases = load_cases(args.gold)
    actuals = load_actual_map(args.actual)
    results, passed, unknown, declared = [], 0, 0, 0
    for case in cases:
        ok, detail = judge_file(case, actuals.get(case["id"]))
        decl, detail = apply_declared(case, ok, detail)
        if ok is None:
            unknown += 1
        elif decl:
            declared += 1
        else:
            passed += bool(ok)
        mark = "SKIP" if ok is None else ("DECL" if decl else ("PASS" if ok else "FAIL"))
        results.append({"id": case["id"], "pass": ok, "declared": decl or None,
                        "waiver": case.get("declared_conflict") if decl else None,
                        "detail": detail})
        print(f"[{mark}] {case['id']}" + (f" —— {detail}" if detail else ""))
    effective = len(cases) - unknown - declared
    print(f"\n回归结果：{passed}/{effective} 通过"
          + (f"（另 {unknown} 条期望不明跳过）" if unknown else "")
          + (f"（另 {declared} 条声明冲突豁免留痕）" if declared else ""))
    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            from _evaluation import report_evidence
            summary = {"passed": passed, "total": effective, "unknown": unknown,
                       "all_cases": len(cases), "declared": declared,
                       "acc": passed / effective if effective else 0}
            json.dump({**summary, "summary": summary, "cases": results,
                       "evidence": ev}, f, ensure_ascii=False, indent=2)
    return 0 if effective and not unknown and passed == effective else 1


def main():
    ap = argparse.ArgumentParser(description="回归比对器 v0.0.5（活引擎 / 离线双模式）")
    ap.add_argument("--endpoint", help="活引擎地址（模式 A）")
    ap.add_argument("--cases", help="用例集 json/yaml（模式 A）")
    ap.add_argument("--gold-results", dest="gold_results", default=None,
                    help="fmt3 用例的期望行（gold_results.json）")
    ap.add_argument("--multihop", default=None, help="多跳用例（可选，单独汇总）")
    ap.add_argument("--out", default="eval_report.json")
    ap.add_argument("--gold", help="gold 用例集（模式 B）")
    ap.add_argument("--actual", help="引擎实际输出 jsonl/yaml/json（模式 B）")
    ap.add_argument("--report", default=None, help="模式 B 报告输出路径")
    ap.add_argument("--model", help="绑定当前模型文件哈希；缺失时报告不能用于验证门禁")
    ap.add_argument("--db", help="绑定 SQLite 数据快照；不证明端点使用了此快照")
    ap.add_argument("--mode", choices=["mock"], help="显式标记合成模拟证据")
    ap.add_argument("--allow-remote", action="store_true",
                    help="允许非本机/内网端点（默认拒绝，防误发业务内容到公网）")
    args = ap.parse_args()

    if args.endpoint:
        try:
            guard_endpoint(args.endpoint, args.allow_remote)
        except ValueError as exc:
            print(f"错误：{exc}", file=sys.stderr)
            return 2
        if not args.cases:
            print("错误：模式 A 需要 --cases", file=sys.stderr)
            return 2
        return run_live(args)
    if args.gold and args.actual:
        return run_offline(args)
    print("错误：二选一——模式 A 用 --endpoint + --cases；模式 B 用 --gold + --actual",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
