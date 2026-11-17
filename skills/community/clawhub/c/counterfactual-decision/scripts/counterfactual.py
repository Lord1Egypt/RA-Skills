#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""counterfactual-decision —— 反事实决策（可计算的 What-if 对照）。

给定决策模型(加权线性评分 + 阈值)与干预，计算：
  factual           : 基线状态上的事实评估
  counterfactual   : 施加干预后的反事实评估
  flip / margin    : 决策是否翻转 / 边际贡献
  contributions     : 每个被干预变量的单独贡献
零依赖、可本地实跑；--selftest 自带夹具断言全链路通过。
"""
import sys, argparse, json


def evaluate(model, state):
    score = sum(model["weights"].get(k, 0.0) * v for k, v in state.items())
    return {"score": round(score, 4), "decision": score >= model["threshold"]}


def counterfactual(model, state, interven):
    cf_state = dict(state)
    cf_state.update(interven)
    return cf_state


def contributions(model, state, interven):
    """每个被干预变量的单独贡献 = w · Δv。"""
    out = {}
    for k, nv in interven.items():
        w = model["weights"].get(k, 0.0)
        dv = nv - state.get(k, 0.0)
        out[k] = round(w * dv, 4)
    return out


def conclude(model, state, interven):
    factual = evaluate(model, state)
    cf_state = counterfactual(model, state, interven)
    cf = evaluate(model, cf_state)
    return {
        "factual": factual,
        "counterfactual": cf,
        "flip": factual["decision"] != cf["decision"],
        "margin": round(cf["score"] - factual["score"], 4),
        "contributions": contributions(model, state, interven),
    }


def selftest():
    print("🧪 selftest: 构造加权决策夹具 ...")
    model = {"weights": {"a": 1.0, "b": 1.0}, "threshold": 1.5}
    state = {"a": 1.0, "b": 0.0}          # 事实 score=1.0 < 1.5 -> False
    interven = {"a": 2.0}                    # 干预 a: 1->2
    res = conclude(model, state, interven)
    # 断言1：事实决策为 False
    assert res["factual"]["decision"] is False, f"事实应 False，实际 {res['factual']}"
    assert res["factual"]["score"] == 1.0, f"事实 score 应 1.0，实际 {res['factual']['score']}"
    # 断言2：反事实 score=2.0 -> True（翻转）
    assert res["counterfactual"]["score"] == 2.0, f"反事实 score 应 2.0，实际 {res['counterfactual']['score']}"
    assert res["counterfactual"]["decision"] is True, "反事实应翻转成 True"
    assert res["flip"] is True, "应标记 flip=True"
    # 断言3：边际贡献 = 1.0，变量 a 单独贡献 = 1.0
    assert res["margin"] == 1.0, f"margin 应 1.0，实际 {res['margin']}"
    assert res["contributions"]["a"] == 1.0, f"a 贡献应 1.0，实际 {res['contributions']}"
    print(f"  ✓ 事实评估正确（score={res['factual']['score']}, 决策={res['factual']['decision']}）")
    print(f"  ✓ 反事实对照正确（score={res['counterfactual']['score']}, 翻转={res['flip']}）")
    print(f"  ✓ 边际贡献/变量贡献正确（margin={res['margin']}, a={res['contributions']['a']}）")
    print("✅ selftest 全链路 PASS")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--state")
    ap.add_argument("--intervene")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.model and args.state and args.intervene):
        print("用法: --model m.json --state s.json --intervene '{\"a\":2}' [--selftest]")
        return None
    model = json.load(open(args.model, encoding="utf-8"))
    state = json.load(open(args.state, encoding="utf-8"))
    interven = json.loads(args.intervene)
    print(json.dumps(conclude(model, state, interven), ensure_ascii=False, indent=2))
    return None


if __name__ == "__main__":
    main()
