# -*- coding: utf-8 -*-
"""loop_kit.py — loop 命令实现体:渲染评审闭环执行清单生成器(0.16.0)。

把渲染评审轮(showcase 打磨 + 配方 v1-v7 两轮实证的回路)编码为宿主可逐步执行的检查单:
机械预检 → 渲染截图(三条 IAB 铁律)→ qc 对账 → 五镜自审 → 定点修复(patch)→ 复验 → 停止条件。
清单内命令按实参生成(页面/色板/下限真实填入),复制即跑;闸门绿≠完成,五镜过才可宣称完成
(用户铁律 2026-10-21)。被 palette_forge.py 的 cmd_loop 调用。纯 stdlib。
"""

FIVE_LENSES = (
    ("视线顺序", "第一眼落点=本屏主角?动线 Z/F 且不跳脱;主角被装饰抢走=不过。"),
    ("密度", "信息密度够吗?空留白必须有出处(十字/竖注/水印/真实内容),不许空留白。"),
    ("构图", "跨度序列/不对称比成立?装饰剂量(强调≤10%、一屏一主角)被超了吗?"),
    ("对比可读", "最小字、最弱对比处念得出来吗?念不出=不过,给修复值再改。"),
    ("减法", "删掉任何一件,页面更好吗?对象·依据·状态·主动作四类不删,其余敢删。"),
)


def emit(page, palette, floor=12, bg=None, out=None):
    """→ 检查单 markdown 文本。palette=hex 列表。"""
    pal = ",".join(palette)
    bg_arg = (" --bg " + bg) if bg else ""
    md = f"""# 渲染评审闭环清单 — {page}

> 每轮迭代照单执行;**修复后必须复验**。四闸绿+五镜过才可宣称完成;清单由 aesthete loop 生成,命令已按实参填好,复制即跑(skill 根目录执行)。

## 0 机械预检(先于渲染)
- [ ] `python3 scripts/palette_forge.py audit {page} --palette {pal} --floor {floor}`
  P0 存在或 P1≥2 = FAIL:先修再渲染(机械类可用 patch --apply 直修)。
- [ ] `python3 scripts/lint_page.py {page} --palette {pal}` —— 色板漂移/字号/渐变静态闸。

## 1 渲染截图(三条铁律)
1. 整视口截图(建议 1280×1400);⛔clip 范围大于视口与 ⛔fullPage 长页都会触发 900px 平铺伪影——**逐屏滚动、分屏截**。
2. goto 后立即 capture 必挂:重开标签页或等 4 秒再截。
3. 多标签页按 URL 匹配选 tab;⛔tabs.list()[0] 盲选(会截到旧页)。
4. headless/无头截图先强制显形再截:含 .reveal(入场动画 opacity:0)的页面会拍到未显形区块,
   误判成空洞;100svh/60vh 区块随视口拉伸——推荐真实视口 1280×1400 逐屏。
4. **全量滚屏目审**:逐屏直到页底。首屏目审发现不了折叠线以下的 bug(引文幕塌窄条教训)。

## 2 渲染对账(至少首屏一张)
- [ ] `python3 scripts/palette_forge.py qc <首屏>.png --palette {pal}{bg_arg}`
  大底真伪/板外入侵带面积份额;FAIL 即回阶段 0,修完重截。

## 3 五镜自审(每屏过一遍,严格、不含水分)
"""
    for i, (name, q) in enumerate(FIVE_LENSES, 1):
        md += f"{i}. **{name}** —— {q}\n"
    md += f"""
## 4 定点修复
- [ ] `python3 scripts/palette_forge.py patch {page} --palette {pal} --floor {floor} --apply`
  机械类(脏色大底/字号下限/中文负字距/对比对)生成字面替换对,自动备份 .bak 后直修并复检;
  不可机械类按 audit 的 fix 字段手工改——每处颜色修改必须回答"它编码什么"。

## 5 复验与停止条件(全满足才停)
- [ ] audit:0 P0 且 P1<2
- [ ] qc:PASS(渲染实况=声明)
- [ ] lint:exit 0
- [ ] 五镜:无未修复问题
- 仍不过 → 回阶段 1 下一轮;**最多 5 轮**——5 轮仍不过 = 换配方或换板,不要死磕细节。
"""
    if out:
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
    return md
