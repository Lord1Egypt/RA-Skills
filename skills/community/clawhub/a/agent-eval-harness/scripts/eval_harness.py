#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent-eval-harness —— 智能体回归评测。

把"是否真在超越一线大模型"变成可度量：用一组回归测试用例驱动 agent，量化通过率，
并与历史基线比对，自动标记能力回退(regression)。这是超级智能体「可被度量」的落地层。

用法：
  python eval_harness.py --selftest
"""
import os, sys, json, datetime


class TestCase:
    def __init__(self, cid, prompt, expect_contains=None, expect_fn=None):
        self.cid = cid
        self.prompt = prompt
        self.expect_contains = expect_contains or []
        self.expect_fn = expect_fn


class EvalHarness:
    def __init__(self, regression_path=None):
        self.cases = []
        self.results = []
        self.regression_path = regression_path or os.path.join(
            os.path.dirname(__file__), "regression.jsonl"
        )
        self.baseline = self._load_baseline()

    def add(self, case):
        self.cases.append(case)

    def _check(self, case, output):
        if case.expect_fn:
            try:
                return bool(case.expect_fn(output))
            except Exception:
                return False
        return all(k in output for k in case.expect_contains)

    def run(self, agent_fn):
        self.results = []
        for c in self.cases:
            try:
                out = agent_fn(c.prompt)
            except Exception as e:
                out = "ERROR: %s" % e
            passed = self._check(c, out)
            self.results.append({
                "id": c.cid, "passed": passed,
                "output": (out or "")[:200],
            })
        return self.summary()

    def summary(self):
        n = len(self.results)
        p = sum(1 for r in self.results if r["passed"])
        rate = (p / n) if n else 0.0
        regressed = self._regression(rate)
        return {
            "total": n, "passed": p, "pass_rate": round(rate, 3),
            "regressed": regressed, "baseline": self.baseline,
        }

    def _regression(self, rate):
        if self.baseline is None:
            self._save_baseline(rate)
            return False
        dropped = self.baseline - rate
        if dropped > 0.1:  # 通过率回退超过 10 个百分点 -> 标记回归
            return True
        self._save_baseline(rate)
        return False

    def _load_baseline(self):
        if os.path.exists(self.regression_path):
            try:
                lines = [l for l in open(self.regression_path, encoding="utf-8") if l.strip()]
                if lines:
                    return float(json.loads(lines[-1])["pass_rate"])
            except Exception:
                pass
        return None

    def _save_baseline(self, rate):
        with open(self.regression_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                "pass_rate": round(rate, 3),
            }, ensure_ascii=False) + "\n")


def _selftest():
    tmp = os.path.join(os.path.dirname(__file__), "regression_selftest.jsonl")
    if os.path.exists(tmp):
        os.remove(tmp)

    def fake_agent_v1(prompt):
        if "2+2" in prompt:
            return "结果是 4"
        if "法国" in prompt:
            return "巴黎"
        return "unknown"

    def fake_agent_v2(prompt):
        return "unknown"

    # 第一轮：1/2 通过，首次无基线 -> 不报回归，写入基线 0.5
    h1 = EvalHarness(tmp)
    h1.add(TestCase("t1", "2+2=?", expect_contains=["4"]))
    h1.add(TestCase("t2", "法国首都是？", expect_contains=["Paris"]))
    s1 = h1.run(fake_agent_v1)
    assert s1["passed"] == 1 and s1["total"] == 2, "通过数异常: %s" % s1
    assert abs(s1["pass_rate"] - 0.5) < 1e-6, "通过率异常: %s" % s1
    assert s1["regressed"] is False, "首次运行不应报回归"
    assert s1["baseline"] is None, "首次基线应为 None"

    # 第二轮：agent 退化，0/2 通过，基线 0.5 -> 回退 0.5 > 0.1 报回归
    h2 = EvalHarness(tmp)
    h2.add(TestCase("t1", "2+2=?", expect_contains=["4"]))
    h2.add(TestCase("t2", "法国首都是？", expect_contains=["Paris"]))
    s2 = h2.run(fake_agent_v2)
    assert s2["pass_rate"] == 0.0, "第二轮通过率应为 0"
    assert s2["regressed"] is True, "能力回退应被标记"
    assert abs(s2["baseline"] - 0.5) < 1e-6, "基线应读到 0.5"

    os.remove(tmp)
    print("✅ agent-eval-harness selftest 全过 (通过率量化+回归检测)")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        _selftest()
        return
    print("用法: python eval_harness.py --selftest")


if __name__ == "__main__":
    main()
