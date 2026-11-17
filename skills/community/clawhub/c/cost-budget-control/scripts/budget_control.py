#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cost-budget-control —— 成本与算力预算控制。

让超级智能体的每次推理/工具调用都在 token 与成本预算内执行，超预算硬性拦截，
并提供压缩建议降低单位算力产出成本。这是「可规模化、可靠地超越」的落地前提。

用法：
  python budget_control.py --selftest
  python budget_control.py estimate --prompt-tokens 1000 --completion-tokens 500 --price-per-1k 0.01
  python budget_control.py enforce --estimated 0.03 --budget 0.02
  python budget_control.py compress --text "..." --keep-ratio 0.5
"""
import os, sys, re, json


class Budget:
    def __init__(self, token_budget=None, cost_budget=None, price_per_1k=0.01):
        self.token_budget = token_budget
        self.cost_budget = cost_budget
        self.price_per_1k = price_per_1k

    def estimate(self, prompt_tokens, completion_tokens):
        total = prompt_tokens + completion_tokens
        cost = total / 1000.0 * self.price_per_1k
        return {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                "total_tokens": total, "estimated_cost": round(cost, 6)}

    def enforce(self, estimated_cost, estimated_tokens=None):
        over_cost = self.cost_budget is not None and estimated_cost > self.cost_budget
        over_token = self.token_budget is not None and estimated_tokens is not None and estimated_tokens > self.token_budget
        return {"allowed": not (over_cost or over_token),
                "over_cost": over_cost, "over_token": over_token,
                "budget": self.cost_budget, "estimated_cost": estimated_cost}

    @staticmethod
    def compress(text, keep_ratio=0.5):
        """极简抽取式压缩：按句子重要性(长度+数字/专有名词密度)保留 keep_ratio 比例。"""
        sentences = re.split(r"(?<=[。！？.!?])", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return text
        def score(s):
            nums = len(re.findall(r"\d", s))
            nouns = len(re.findall(r"[A-Za-z]{3,}", s))
            return len(s) + nums * 3 + nouns * 2
        ranked = sorted(sentences, key=score, reverse=True)
        keep_n = max(1, int(round(len(sentences) * keep_ratio)))
        kept = set(ranked[:keep_n])
        # 维持原文顺序
        out = [s for s in sentences if s in kept]
        return "".join(out)


def _selftest():
    b = Budget(token_budget=2000, cost_budget=0.02, price_per_1k=0.01)
    # 预算内
    est = b.estimate(1000, 500)
    assert abs(est["estimated_cost"] - 0.015) < 1e-9, "成本估算错误: %s" % est
    en = b.enforce(est["estimated_cost"], est["total_tokens"])
    assert en["allowed"] is True, "预算内应放行: %s" % en
    # 超成本拦截
    est2 = b.estimate(3000, 0)
    en2 = b.enforce(est2["estimated_cost"])
    assert en2["allowed"] is False and en2["over_cost"], "超成本应拦截"
    # 超 token 拦截
    en3 = b.enforce(0.005, 5000)
    assert en3["allowed"] is False and en3["over_token"], "超 token 应拦截"
    # 压缩降本
    txt = "项目预算为 120 万元。系统于 2026 年上线。本次会议讨论路线图。后续将评估风险。最终方案需审批。"
    comp = Budget.compress(txt, keep_ratio=0.5)
    assert len(comp) < len(txt), "压缩后应变短"
    assert "120" in comp, "含关键数字的句子应保留"
    print("✅ cost-budget-control selftest 全过 (成本估算+双重拦截+压缩降本)")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        _selftest()
        return
    b = Budget()
    if not args:
        print("用法: --selftest | estimate | enforce | compress")
        return
    cmd = args[0]
    kv = {}
    i = 1
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            kv[a[2:]] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else ""
            i += 2
        else:
            i += 1
    if cmd == "estimate":
        print(json.dumps(b.estimate(int(kv.get("prompt-tokens", 0)), int(kv.get("completion-tokens", 0))), ensure_ascii=False))
    elif cmd == "enforce":
        print(json.dumps(b.enforce(float(kv.get("estimated", 0)), int(kv.get("estimated-tokens", 0) or 0) or None), ensure_ascii=False))
    elif cmd == "compress":
        print(Budget.compress(kv.get("text", ""), float(kv.get("keep-ratio", 0.5))))


if __name__ == "__main__":
    main()
