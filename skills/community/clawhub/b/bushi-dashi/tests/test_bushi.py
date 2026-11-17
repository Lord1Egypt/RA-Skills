#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bushi.py 单测 —— 覆盖钱筮法概率、卦象编码、断卦七法、签级边界、卦图对齐、学卦数据、卦册落盘
用法：python tests/test_bushi.py
"""
import os
import random
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import bushi  # noqa: E402

FAILS = 0
CHECKS = 0


def ok(cond, msg):
    global FAILS, CHECKS
    CHECKS += 1
    if cond:
        print("  ok  %s" % msg)
    else:
        FAILS += 1
        print("  ❌  %s" % msg)


def main():
    rng = random.Random(20261031)

    print("== 1. 钱筮法概率分布（N=100000）==")
    dist = {6: 0, 7: 0, 8: 0, 9: 0}
    N = 100000
    for _ in range(N):
        dist[bushi.cast_once(rng)] += 1
    expect = {6: 0.125, 7: 0.375, 8: 0.375, 9: 0.125}
    for k, e in expect.items():
        p = dist[k] / N
        ok(abs(p - e) < 0.005, "爻值 %d 概率 %.4f ≈ %.3f" % (k, p, e))
    ok(bushi.LINE_NAMES[6] == "老阴" and bushi.LINE_NAMES[9] == "老阳", "爻名映射正确")
    ok(len(bushi.cast_hexagram(rng)) == 6, "cast_hexagram 返回 6 爻")

    print("== 2. 卦象编码 ==")
    lines = [9, 8, 7, 6, 7, 8]
    ok(bushi.primary_bits(lines) == 21, "本卦 bits=21（0b010101）")
    ok(bushi.changed_bits(lines) == 28, "之卦 bits=28（初九变阴、六四变阳）")
    ok(bushi.changing_positions(lines) == [1, 4], "变爻位 [1,4]")
    ok(bushi.primary_bits([7] * 6) == 63, "六阳=乾 bits=63")
    ok(bushi.primary_bits([8] * 6) == 0, "六阴=坤 bits=0")
    ok(bushi.is_yang(7) and bushi.is_yang(9) and not bushi.is_yang(6) and not bushi.is_yang(8), "阴阳判定")
    ok(bushi.hex_name(63) == "乾为天" and bushi.hex_name(0) == "坤为地", "卦名查库")
    ok(len(bushi.hexagrams()) == 64, "卦库 64 卦")
    ok(bushi.yao_text(63, 0) == "潜龙勿用。", "乾初九爻辞")
    ok(bushi.hex_of(63).get("yong", "") == "见群龙无首，吉。", "乾有用辞（见群龙无首，吉。）")
    ok(bushi.hex_of(0).get("yong", "") == "利永贞。", "坤有用辞（利永贞。）")

    print("== 3. 断卦七法逐档（遵主人参照图）==")
    v = bushi.verdict([7] * 6)
    ok(len(v) == 1 and v[0]["pos"] == -1 and v[0]["bits"] == 63 and v[0]["role"] == "主", "0 变→本卦卦辞单选")
    v = bushi.verdict([9, 7, 7, 7, 7, 7])
    ok(len(v) == 1 and v[0]["pos"] == 0 and v[0]["bits"] == 63, "1 变→本卦变爻爻辞（单辞，照图）")
    v = bushi.verdict([9, 9, 7, 7, 7, 7])
    ok(v[0]["pos"] == 1 and v[1]["pos"] == 0, "2 变→主=上变爻、副=下变爻")
    l3 = [9, 9, 9, 7, 7, 7]
    v = bushi.verdict(l3)
    ok(v[0]["pos"] == -1 and v[0]["bits"] == 63 and v[1]["pos"] == -1
       and v[1]["bits"] == bushi.changed_bits(l3), "3 变→本卦辞主、之卦辞副")
    v = bushi.verdict([9, 9, 9, 9, 7, 7])
    ok(v[0]["pos"] == 4 and v[1]["pos"] == 5 and v[0]["bits"] == 63, "4 变→本卦两不变爻、下爻为主（与参照图同）")
    l5 = [9, 9, 9, 9, 9, 7]
    v = bushi.verdict(l5)
    cb5 = bushi.changed_bits(l5)
    ok(len(v) == 1 and v[0]["pos"] == 5 and v[0]["bits"] == cb5, "5 变→之卦不变爻爻辞（单辞，照图）")
    v = bushi.verdict([9] * 6)
    ok(len(v) == 1 and v[0]["pos"] == -1 and v[0]["bits"] == 0, "6 变乾→之卦（坤）卦辞，不设用九特例")
    v = bushi.verdict([6] * 6)
    ok(len(v) == 1 and v[0]["pos"] == -1 and v[0]["bits"] == 63, "6 变坤→之卦（乾）卦辞")
    l6 = [9, 6, 9, 6, 9, 6]
    v = bushi.verdict(l6)
    ok(len(v) == 1 and v[0]["pos"] == -1 and v[0]["bits"] == bushi.changed_bits(l6), "6 变非乾坤→之卦卦辞")

    print("== 4. 签级边界 ==")
    ok(bushi.tier_of(70.0) == "shangshang" and bushi.tier_of(69.9) == "shang", "70 分界上上/上")
    ok(bushi.tier_of(30.0) == "shang" and bushi.tier_of(29.9) == "zhong", "30 分界上/中")
    ok(bushi.tier_of(-29.9) == "zhong" and bushi.tier_of(-30.0) == "xia", "-30 分界中/下（-30 归下，遵游戏版）")
    ok(bushi.tier_of(-69.9) == "xia" and bushi.tier_of(-70.0) == "xiaxia", "-70 分界下/下下（-70 归下下）")
    ok(bushi.tier([7] * 6) == "shangshang", "六少阳（乾·0 变）→ 上上签")
    ok(bushi.TIER_LABEL["zhong"] == "中签", "签级中文")
    ok(bushi.score([7] * 6) == 90.0, "乾 0 变 score=90（ji 独断）")
    ok(abs(bushi.score([9] * 6)) <= 90.0, "坤 6 变 score 在 [-90,90]")

    print("== 4b. 卦图 ==")
    dg = bushi.build_diagram([8, 8, 7, 8, 8, 9])
    ok("艮为山" in dg and "地山谦" in dg, "卦图含本卦与之卦名")
    ok("Ｘ" in dg and "上九" in dg, "动爻标记 Ｘ 与爻题在图（老阴老阳同记，遵参照图）")
    ok(dg.count(bushi.YANG_BAR) + dg.count(bushi.YIN_BAR) == 12, "本卦、之卦各六爻")
    ok(bushi.CHANGE_MARK[6] == bushi.CHANGE_MARK[9] == "Ｘ", "老阴老阳同记 Ｘ（遵参照图）")
    # 对齐：爻画之前的对齐区（爻题+标记）每行同宽，且不含歧义宽度字符
    pres = [r.split(bushi.YANG_BAR if bushi.YANG_BAR in r else bushi.YIN_BAR)[0]
            for r in dg.split("\n")
            if (bushi.YANG_BAR in r or bushi.YIN_BAR in r)]
    widths = {bushi._dw(p) for p in pres}
    ok(len(widths) == 1, "各行爻画同列起画（对齐区 %s 列）" % sorted(widths))
    amb = [c for p in pres for c in p if unicodedata.east_asian_width(c) == "A"]
    ok(amb == [], "对齐区无歧义宽度字符（粗线 ▄ 恒在行尾，不参与对齐）")
    ok(bushi._dw(bushi.CHANGE_MARK[9]) == bushi._dw(bushi.CHANGE_MARK[6]) == 2
       and bushi._dw("  ") == 2, "变爻标记与静爻占位同为 2 列")
    dg0 = bushi.build_diagram([7] * 6)
    ok("之卦" not in dg0 and "无（六爻安静）" in dg0, "无变爻只画本卦")
    ok(dg0.count(bushi.YANG_BAR) == 6, "六阳爻全实")

    print("== 4c. 掷报换算（遵参照图四种情况）==")
    ok(bushi.TOSS_MAP == {"3阴": 6, "2阴1阳": 7, "1阴2阳": 8, "3阳": 9},
       "四种情况映射：三阴=6 / 二阴一阳=7 / 一阴二阳=8 / 三阳=9")
    ok(bushi.parse_toss("3阴") == 6 and bushi.parse_toss("三阴") == 6, "三阴=6 老阴")
    ok(bushi.parse_toss("3阳") == 9 and bushi.parse_toss("三阳") == 9, "三阳=9 老阳")
    ok(bushi.parse_toss("1阴2阳") == 8 and bushi.parse_toss("一阴二阳") == 8, "一阴二阳=8 少阴")
    ok(bushi.parse_toss("2阴1阳") == 7 and bushi.parse_toss("二阴一阳") == 7
       and bushi.parse_toss("两阴一阳") == 7, "二阴一阳=7 少阳")
    ok(bushi.parse_toss("2阴,1阳") == 7 and bushi.parse_toss("1阳2阴") == 7, "宽松写法（逗号/倒序）")
    ok(bushi.parse_toss("4阴") is None and bushi.parse_toss("乱写") is None, "非法报法返回 None")

    print("== 5. 学卦数据 ==")
    d = bushi.study_data(63)
    ok(bool(d) and len(d.get("sections", [])) == 12, "乾卦四源 12 节入库")
    gua = [s for s in d["sections"] if s["key"] == "gua"]
    srcs = [b["src"] for b in gua[0]["blocks"]]
    ok(srcs == ["jing", "zhengyi", "benyi", "yizhuan"], "卦辞节四源齐全")
    ok(len(bushi.study_data(8)) == 0, "需卦(bits=8)未入库→空（诚实占位）")

    print("== 6. 卦册（隔离临时文件）==")
    tmp = bushi.CODEX_PATH
    bushi.CODEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_codex_tmp.json")
    if os.path.exists(bushi.CODEX_PATH):
        os.remove(bushi.CODEX_PATH)
    c = bushi.load_codex()
    ok(c["visits"] == 0 and c["casts"] == [], "新册为空")
    c["casts"].append({"bits": 63, "hand": True})
    c["codex"].append(63)
    c["visits"] = 1
    bushi.save_codex(c)
    c2 = bushi.load_codex()
    ok(c2["visits"] == 1 and 63 in c2["codex"] and len(c2["casts"]) == 1, "落盘重读一致")
    os.remove(bushi.CODEX_PATH)
    bushi.CODEX_PATH = tmp

    print("")
    if FAILS == 0:
        print("BUSHI ALL PASSED (%d checks)" % CHECKS)
        sys.exit(0)
    print("BUSHI FAILED: %d/%d" % (FAILS, CHECKS))
    sys.exit(1)


if __name__ == "__main__":
    main()
