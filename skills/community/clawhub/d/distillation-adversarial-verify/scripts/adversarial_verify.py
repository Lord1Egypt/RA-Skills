#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""distillation-adversarial-verify: 对蒸馏出的决策规则做对抗验证，量化蒸馏质量。

用法:
  python adversarial_verify.py --selftest
  python adversarial_verify.py <学生技能目录>

规则约定：每条规则是 (name, callable, weight, cases) 四元组。
  callable(input) -> bool  表示 "该输入应被规则放行/判为真"。
  对抗用例 cases 为 [(input, expect_pass:bool), ...]。
  翻转(flip) = 规则输出与 expect_pass 相反。robustness = 1 - flips/total。
"""
import os, sys, json, importlib.util


def verify_rule(rule_fn, cases):
    """返回 (robustness, flips, details)。"""
    flips = 0
    details = []
    for inp, expect_pass in cases:
        try:
            got = bool(rule_fn(inp))
        except Exception as e:
            details.append({"input": inp, "error": str(e), "flip": True})
            flips += 1
            continue
        ok = (got == expect_pass)
        if not ok:
            flips += 1
        details.append({"input": inp, "expected_pass": expect_pass, "got": got, "flip": not ok})
    robustness = 1.0 - (flips / len(cases) if cases else 0.0)
    return robustness, flips, details


def verify_all(rules_with_cases, threshold=0.8):
    """rules_with_cases: [(name, fn, weight, cases)]。返回汇总 dict。"""
    per, wsum, qsum, weak = [], 0.0, 0.0, []
    for name, fn, weight, cases in rules_with_cases:
        rob, flips, _ = verify_rule(fn, cases)
        per.append({"name": name, "robustness": round(rob, 3), "flips": flips, "weight": weight})
        wsum += weight
        qsum += rob * weight
        if rob < threshold:
            weak.append(name)
    quality = round(qsum / wsum, 3) if wsum else 0.0
    verdict = "PASS" if (quality >= threshold and not weak) else "NEEDS_REWORK"
    return {"rules": per, "overall_quality": quality, "verdict": verdict, "weak_rules": weak}


def selftest():
    # 规则A：正数放行（正确实现）
    def rule_a(x): return x > 0
    # 规则B：本应"偶数放行"，但蒸馏出了错误实现（>0），对抗用例会戳穿
    def rule_b(x): return x > 0  # 错误：与"偶数"语义不符
    rules = [
        ("正数放行", rule_a, 1.0, [(5, True), (-3, False), (0, False)]),
        ("偶数放行(脆弱)", rule_b, 1.0, [(2, True), (4, True), (3, False), (1, False)]),
    ]
    res = verify_all(rules)
    try:
        assert res["rules"][0]["robustness"] == 1.0, f"规则A 应满分: {res['rules'][0]}"
        assert res["rules"][1]["flips"] >= 2, f"规则B 应被戳穿: {res['rules'][1]}"
        assert res["verdict"] == "NEEDS_REWORK", f"整体应判重做: {res['verdict']}"
        assert "偶数放行(脆弱)" in res["weak_rules"], f"薄弱规则未标记: {res['weak_rules']}"
        assert 0.6 <= res["overall_quality"] <= 0.85, f"质量分应在中段: {res['overall_quality']}"
        print("🧪 selftest PASS：ruleA_rob=%.2f ruleB_flips=%d quality=%.2f verdict=%s"
              % (res["rules"][0]["robustness"], res["rules"][1]["flips"],
                 res["overall_quality"], res["verdict"]))
        return 0
    except AssertionError as e:
        print("❌ selftest FAIL:", e); return 1


def _load_rules_from_skill(skill_dir):
    """尝试从学生技能的 scripts/adv_rules.py 载入 RULES（可选）。"""
    cand = os.path.join(skill_dir, "scripts", "adv_rules.py")
    if not os.path.isfile(cand):
        return None
    spec = importlib.util.spec_from_file_location("adv_rules", cand)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "RULES", None)


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if not args or args[0].startswith("--"):
        raise SystemExit("用法: adversarial_verify.py <学生技能目录> | --selftest")
    rules = _load_rules_from_skill(args[0])
    if not rules:
        print("⚠️ 该学生技能未提供 scripts/adv_rules.py，改用 --selftest 演示。")
        return selftest()
    res = verify_all(rules)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
