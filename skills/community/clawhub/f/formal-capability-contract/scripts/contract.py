#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract.py — 形式化能力契约与可证正确（零依赖纯标准库）。

这是北极星"超越一线大模型"里把"能力信任"从「启发式/话术」升级为「可机器验证」的元能力：
给 agent 的每个能力（动作/函数/规划步骤）定义 **前置条件(pre) / 后置条件(post) / 不变量(invariant)**，
用契约校验器对一次真实执行轨迹做**可证明正确**的判定——not just "看起来对"。

与 reason-verify（文本可靠性）的区别：这里是**结构化契约**（输入/输出/状态的可执行断言），
给出"该能力这次执行是否满足其形式化规约"的确定性结论，而非模糊的可靠性打分。

用法：
  python contract.py --selftest
  python contract.py --demo
"""
import os, sys, json


class Contract:
    """一个能力的形式化契约：前置 / 后置 / 不变量（均为可执行断言）。"""

    def __init__(self, name, pre, post, invariant=None, desc=""):
        self.name = name
        self.pre = pre              # callable(trace) -> bool
        self.post = post            # callable(trace) -> bool
        self.invariant = invariant  # callable(trace) -> bool （可空）
        self.desc = desc

    def check(self, trace):
        """对一条执行轨迹做契约校验，返回结构化结论。"""
        failed = []
        try:
            if not self.pre(trace):
                failed.append("pre")
        except Exception as e:
            failed.append("pre(error:%s)" % e)
        try:
            if not self.post(trace):
                failed.append("post")
        except Exception as e:
            failed.append("post(error:%s)" % e)
        if self.invariant is not None:
            try:
                if not self.invariant(trace):
                    failed.append("invariant")
            except Exception as e:
                failed.append("invariant(error:%s)" % e)
        satisfied = len(failed) == 0
        return {
            "capability": self.name,
            "satisfied": satisfied,
            "failed_clause": failed,
            "verdict": "可证明正确" if satisfied else "契约违反",
        }


def verify_capability(contract, traces):
    """对一个能力的一组执行轨迹做契约校验，产出可证正确率。"""
    results = [contract.check(t) for t in traces]
    passed = sum(1 for r in results if r["satisfied"])
    n = len(results)
    return {
        "capability": contract.name,
        "total": n,
        "passed": passed,
        "provable_score": round(passed / n, 3) if n else 0.0,
        "verdict": "可证明正确" if passed == n else "存在契约违反",
        "results": results,
    }


# —— 演示用契约：安全除法 ——
def _safe_divide_pre(t):
    return isinstance(t.get("input"), (list, tuple)) and len(t["input"]) == 2 \
        and t["input"][1] != 0


def _safe_divide_post(t):
    a, b = t["input"]
    return t["output"] * b == a


# —— 演示用契约：列表排序（含不变量：长度守恒）——
def _sort_pre(t):
    return isinstance(t.get("input"), list)


def _sort_post(t):
    return t["output"] == sorted(t["input"]) and len(t["output"]) == len(t["input"])


def _sort_invariant(t):
    return len(t.get("post_state", [])) == len(t.get("pre_state", []))


def selftest():
    # 契约：安全除法
    div = Contract("safe_divide", _safe_divide_pre, _safe_divide_post,
                   desc="pre: 除数!=0；post: output*b==a")
    # 契约：列表排序（不变量 长度守恒）
    srt = Contract("sort_list", _sort_pre, _sort_post, _sort_invariant,
                   desc="pre: 输入是 list；post: 有序且等长；invariant: 状态长度守恒")

    # —— safe_divide：good 通过 / bad_pre 触发 pre 违反 / bad_post 触发 post 违反 ——
    good_div = {"input": (10, 2), "output": 5}
    bad_pre = {"input": (10, 0), "output": None}
    bad_post = {"input": (10, 2), "output": 6}
    rd = verify_capability(div, [good_div, bad_pre, bad_post])
    assert rd["results"][0]["satisfied"] is True, "❌ good 除法应通过"
    assert "pre" in rd["results"][1]["failed_clause"], "❌ 除数为0 应触发 pre 违反"
    assert "post" in rd["results"][2]["failed_clause"], "❌ 错误商应触发 post 违反"
    assert rd["provable_score"] == round(1 / 3, 3), "❌ 可证正确率应为 1/3"

    # —— sort_list：good 通过 / bad 触发 post（长度丢失）违反，且 invariant 同时破 ——
    good_srt = {"input": [3, 1, 2], "output": [1, 2, 3],
                "pre_state": [3, 1, 2], "post_state": [1, 2, 3]}
    bad_srt = {"input": [3, 1, 2], "output": [1, 2],
               "pre_state": [3, 1, 2], "post_state": [1, 2]}
    rs = verify_capability(srt, [good_srt, bad_srt])
    assert rs["results"][0]["satisfied"] is True, "❌ good 排序应通过"
    assert "post" in rs["results"][1]["failed_clause"], "❌ 长度丢失应触发 post 违反"
    assert "invariant" in rs["results"][1]["failed_clause"], "❌ 长度丢失应同时破不变量"
    assert rs["provable_score"] == 0.5, "❌ 排序可证正确率应为 0.5"

    # —— 全绿套件 → 可证明正确 ——
    all_green = verify_capability(div, [good_div])["verdict"] == "可证明正确"
    assert all_green, "❌ 全绿套件应判为可证明正确"

    print("✅ formal-capability-contract selftest ALL PASS（pre/post/invariant 三 clauses 可机器验证，"
          "good 通过 / bad 精准定位违反子句 / 全绿判可证明正确）")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "--demo":
        div = Contract("safe_divide", _safe_divide_pre, _safe_divide_post)
        print(json.dumps(verify_capability(div, [
            {"input": (10, 2), "output": 5},
            {"input": (10, 0), "output": None},
        ]), ensure_ascii=False, indent=2))
    else:
        print("用法: python contract.py --selftest")
