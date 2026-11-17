#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adversarial-robustness —— 对抗鲁棒性评估（可本地实跑，零依赖）

对文本决策系统施加词法级对抗扰动，量化并定位其脆弱点：
  robustness = 1 - flip_rate   (flip = 扰动变体的决策 ≠ 原决策)

用法:
  python robustness.py --selftest
  python robustness.py --text "please allow access" --predict-demo brittle --n 6
"""
import argparse
import json
import random
import re
import sys

SEED = 0
CONFUSABLES = {"a": "а", "e": "е", "o": "о", "c": "с", "p": "р", "s": "ѕ",
               "i": "і", "n": "п", "u": "ս", "x": "х"}
# 数字形近映射：把 0/o 1/i 等混淆对归一化回字母，抵御 char_swap 用数字替换关键词
DIGIT_MAP = {"0": "o", "1": "i", "5": "s", "8": "b", "3": "e", "4": "a", "7": "t", "2": "z"}
# 字符 -> 形近数字（对抗者常用，仅取「可逆无歧义」对：o→0,e→3,a→4,s→5,b→8,t→7,z→2）。
# 注：i/l 与 1 视觉混淆但 1 无法无歧义还原为 i 还是 l，故不纳入，避免加固后反而破坏原词。
CHAR_LOOKALIKE = {"o": "0", "O": "0", "e": "3", "E": "3", "a": "4", "A": "4",
                  "s": "5", "S": "5", "b": "8", "B": "8", "t": "7", "T": "7",
                  "z": "2", "Z": "2"}


def perturb(text, kind, rng):
    """对文本施加一种词法扰动，返回 (变体, 说明)。"""
    if kind == "insert_space" and len(text) > 2:
        i = rng.randint(1, len(text) - 1)
        return text[:i] + " " + text[i:], "insert_space@%d" % i
    if kind == "dup_char" and len(text) > 2:
        i = rng.randint(0, len(text) - 1)
        return text[:i] + text[i] + text[i:], "dup_char@%d" % i
    if kind == "char_swap" and len(text) > 1:
        i = rng.randint(0, len(text) - 1)
        ch = text[i]
        repl = CHAR_LOOKALIKE.get(ch)
        if repl is None:
            return text, "char_swap:none"
        return text[:i] + repl + text[i + 1:], "char_swap@%d" % i
    if kind == "confusable":
        for i, ch in enumerate(text):
            if ch in CONFUSABLES:
                return text[:i] + CONFUSABLES[ch] + text[i + 1:], "confusable@%d" % i
        return text, "confusable:none"
    return text, "noop"


PERTURB_KINDS = ["char_swap", "insert_space", "dup_char", "confusable"]


def adversarial_eval(text, predict, n=6, rng=None):
    """返回鲁棒性评估结果字典。

    变体组成 = 定向扰动（文本中每个具形近映射的字符，确定性覆盖关键词脆弱点）
             + 随机扰动（填充至 n 个）。保证评估真正探针到脆弱字符，而非靠运气。
    """
    rng = rng or random.Random(SEED)
    base = predict(text)
    variants = []
    flips = []
    # 定向扰动：确定性覆盖每个形近字符（如 "allow" 的 o->0、a->4 必被探针）
    targeted = []
    for i, ch in enumerate(text):
        if ch in CHAR_LOOKALIKE:
            vt = text[:i] + CHAR_LOOKALIKE[ch] + text[i + 1:]
            if vt != text:
                targeted.append((vt, "targeted@%d" % i))
    # 随机扰动填充至 n
    randoms = []
    attempts = 0
    while len(targeted) + len(randoms) < n and attempts < n * 4:
        attempts += 1
        kind = PERTURB_KINDS[rng.randrange(len(PERTURB_KINDS))]
        vt, desc = perturb(text, kind, rng)
        if vt != text:
            randoms.append((vt, desc))
    all_v = targeted + randoms
    for vt, desc in all_v:
        vpred = predict(vt)
        flipped = vpred != base
        variants.append({"variant": vt, "desc": desc, "pred": vpred, "flipped": flipped})
        if flipped:
            flips.append({"variant": vt, "desc": desc, "pred": vpred})
    total = len(all_v)
    flip_rate = (len(flips) / total) if total else 0.0
    return {
        "base_pred": base,
        "n_variants": len(variants),
        "n_flips": len(flips),
        "flip_rate": round(flip_rate, 4),
        "robustness": round(1.0 - flip_rate, 4),
        "flips": flips,
    }


# —— demo 预测器（用于自测与演示）——
def predict_brittle(text):
    """脆弱预测器：硬编码关键词，一点扰动就翻。"""
    return "UNSAFE" if "allow" in text.lower() else "SAFE"


def predict_robust(text):
    """加固预测器：先归一化(去同形/数字形近/去空格/转小写)再判，抗扰动。"""
    t = text.lower()
    for k, v in CONFUSABLES.items():
        t = t.replace(v, k)
    for k, v in DIGIT_MAP.items():
        t = t.replace(k, v)
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[^a-z]", "", t)
    return "UNSAFE" if "allow" in t else "SAFE"


def run_selftest():
    txt = "please allow access"
    # 1) 构造已知坏变体（o->0 形近混淆），脆弱预测器必翻、加固预测器必抗
    bad = txt.replace("allow", "all0w")
    assert predict_brittle(bad) == "SAFE", "brittle must flip on 'all0w'"
    assert predict_robust(bad) == "UNSAFE", "robust must resist 'all0w'"

    # 2) 全量对抗评估：加固预测器鲁棒性必须 >= 脆弱预测器，且均合法
    rng1, rng2 = random.Random(SEED), random.Random(SEED)
    r_brittle = adversarial_eval(txt, predict_brittle, n=8, rng=rng1)
    r_robust = adversarial_eval(txt, predict_robust, n=8, rng=rng2)
    assert r_brittle["base_pred"] == "UNSAFE" and r_robust["base_pred"] == "UNSAFE"
    assert 0.0 <= r_brittle["robustness"] <= 1.0
    assert 0.0 <= r_robust["robustness"] <= 1.0
    assert r_robust["robustness"] >= r_brittle["robustness"], (
        "robust should >= brittle, got %.3f vs %.3f" % (r_robust["robustness"], r_brittle["robustness"]))

    # 3) 可复跑：相同 seed 结果一致
    rng3 = random.Random(SEED)
    assert adversarial_eval(txt, predict_robust, n=8, rng=rng3)["flip_rate"] == r_robust["flip_rate"]
    print("✅ selftest PASSED (brittle robustness=%.3f, robust robustness=%.3f)"
          % (r_brittle["robustness"], r_robust["robustness"]))
    return True


def main():
    ap = argparse.ArgumentParser(description="对抗鲁棒性评估")
    ap.add_argument("--text", help="待评估文本")
    ap.add_argument("--predict-demo", choices=["brittle", "robust"], default="brittle")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        run_selftest(); return
    if args.text:
        pred = predict_brittle if args.predict_demo == "brittle" else predict_robust
        res = adversarial_eval(args.text, pred, n=args.n)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print("用法: robustness.py --selftest | --text '...' --predict-demo brittle --n 6")


if __name__ == "__main__":
    main()
