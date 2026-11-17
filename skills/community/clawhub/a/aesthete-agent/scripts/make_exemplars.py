# -*- coding: utf-8 -*-
"""make_exemplars.py — 范例库构建器(0.16.0):五配方 → references/exemplars/*.html。

范例=配方产物的静态快照(渲染评审轮 v1-v7 与四闸验证过的同一代码路径),头部注释承载
检索元数据。⭐每例异板异品牌(0.16 评审定案):范例是 agent 的少样学习输入,同板同母题
会把产出拖向同一张脸——板随配方气质走,母题随品牌走。配方或注入说明更新后重跑即再生成。
用法:python3 scripts/make_exemplars.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import layout_recipes  # noqa: E402
import scaffold_kit  # noqa: E402

OUT = os.path.join(HERE, "..", "references", "exemplars")

# (文件名, recipe, kind, register, techniques, 色板, 品牌, 品牌EN, 一句定位)
# 板全部取自库内已验证板族:Deep Pine/野莓 Atelier/靛蓝工程/晨柔——异板防趋同。
SPEC = [
    ("edit-split-light.html", "EDIT-SPLIT", "landing", "light",
     "R2,R5,R9,菜单卡,KPI阶梯",
     ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"], "夜松工作室", "NIGHTPINE", "深松木作·三代手作"),
    ("blueprint-dark.html", "BLUEPRINT", "tech-landing", "dark",
     "R2,网格底纹,bento,亮区定价",
     ["1E293B", "3B82F6", "93C5FD", "DBEAFE", "0F172A"], "界外工具", "OUTBOUND", "给严肃场景的工程台"),
    ("swiss-poster-light.html", "SWISS-POSTER", "poster", "light",
     "R2,R4,巨字,3+9交替,幽灵序号",
     ["EA526F", "E76B74", "D7AF70", "937D64", "585B56"], "野莓甜室", "WILDBERRY", "法式甜品·每周小批"),
    ("editorial-mag-light.html", "EDITORIAL-MAG", "editorial", "light",
     "R1,R6,R9,出血,窄文,三联",
     ["EA526F", "D7AF70", "937D64", "585B56", "F3E7D4"], "晨柔手帖", "MORNPASTEL", "器物与生活·月刊"),
    ("dark-four-act-dark.html", "DARK-FOUR-ACT", "narrative", "dark",
     "R1,R2,R3,R4,明暗旅程,颗粒",
     ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"], "夜松工作室", "NIGHTPINE", "深松木作·三代手作"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn, recipe, kind, register, tech, pal, brand, brand_en, use_when in SPEC:
        tokens = scaffold_kit.derive({"hexes": pal}, brand, brand_en, use_when)
        html = layout_recipes.build_recipe(tokens, recipe)
        meta = ("<!-- exemplar\nkind: %s\nregister: %s\nrecipe: %s\ntechniques: %s\n"
                "palette: %s\nvalidated: 四闸 PASS(0P0/0P1/0P2)+渲染评审 v1-v7\n"
                "regen: python3 scripts/make_exemplars.py(勿手改本文件)\n-->\n" % (
                    kind, register, recipe, tech, ",".join(pal)))
        body = html.replace("<!-- layout-recipe:", "<!-- recipe-source:")
        with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
            f.write(meta + body)
        print("exemplar:", fn, "[%s/%s]" % (brand, ",".join(pal[:2]) + "…"))
    print("OK: %d exemplars -> %s" % (len(SPEC), os.path.abspath(OUT)))


if __name__ == "__main__":
    main()
