#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_skill.py — 把「做过一期的样例」变成一个独立可安装、可二次改造的场景技能。

框架层 journal-draft 解决「怎么做一本刊」；这个脚本解决「同一本刊怎么做第二期起」。
跑 +spec 时被调用，产出一个自包含目录：

    journal-<slug>/
    ├── SKILL.md                 精简流程；parent 兜底，日常不再跑样式学习
    ├── README.md                **改造指南**：哪些钉死别动、哪些每期必改、怎么换成自家
    ├── scripts/build_draft.py   从父技能拷来（纯标准库），使派生技能离线可用
    ├── scripts/export_editable.py  同份内容导出 draft.docx / draft.md（可编辑稿）
    ├── scripts/import_docx.py   编辑改过的 docx 回填 content.json
    ├── assets/
    │   ├── stylespec.json       钉死的版式（已从 semantic 瘦身后）
    │   ├── unit-patterns.md     钉死的内容原子 + 语料
    │   ├── fixed-pieces.md      页眉 / CTA / 免责 / 名录全文
    │   ├── glossary.md          术语与法规名（高频实体）
    │   └── last-issue.md        上期栏目清单与篇幅，作为新一期的容量基线
    ├── sources.template.md      待填的数据源清单
    └── runbook.template.md      待填的成本与踩坑记录

三条设计原则，都是为了「别人拿去能用」：

1. **自包含**：渲染脚本直接拷进来。派生技能不应依赖父技能当时的安装路径，
   否则一发给别人就断。
2. **瘦身**：semantic 段是一次性的学习中间产物，派生后不再需要，剥离掉，
   spec 体积通常能减半。
3. **诚实标注**：凡是机器推断而没经人工复核的，一律写进 literals
   「machine_draft: true」并在 README 标红。**不把未验证的推断伪装成定稿。**

用法：
    python derive_skill.py --spec ./qiming-regional-sample/stylespec.json \\
        --unit-patterns ./qiming-regional-sample/unit-patterns.md \\
        --out ~/.workbuddy/skills/journal-qiming-regional \\
        --name journal-qiming-regional \\
        --publisher "启明律师事务所" \\
        --title "区域观察" \\
        --alias "启明区域观察"

无 --out 时默认写到 ~/.workbuddy/skills/<name>。

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""

import argparse
import io
import json
import os
import re
import sys

CJK = r"\u4e00-\u9fff"


# --------------------------------------------------------------------------- 读

def load_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path):
    if not path or not os.path.exists(path):
        return ""
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def parent_dir():
    """父技能根目录（本脚本位于 parent/scripts/ 下）。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def default_home():
    return os.path.expanduser("~")


# --------------------------------------------------------------------------- 抽

def slim_spec(spec):
    """剥掉 semantic 段——它是学习过程的中间产物，派生后不再需要。

    同时把 meta 里「confidence_note」之类的过程注记也收干净，
    因为派生出去的 spec 是定稿，读它的人不关心上年告警。

    scale_baseline 与 grids 必须保留：前者是篇幅量级门禁的对照值，
    没有它 build_draft --stats 就无法判断这一期是否写够；后者是版心定义，
    spec 缺 grids 时渲染器才会回落到从 page_templates 反推。
    """
    keep_keys = ("meta", "canvas", "palette", "typography", "chrome", "page_templates",
                 "scale_baseline", "grids", "sample_quality")
    out = {}
    for k in keep_keys:
        if k in spec:
            out[k] = spec[k]
    meta = dict(out.get("meta") or {})
    meta.pop("confidence_note", None)
    meta["derived_by"] = "journal-draft/derive_skill.py"
    out["meta"] = meta
    return out


def pick_confidence(sem, has_unit_md):
    """判定派生质量。semantic.tree_confidence 是内容树的可信度，源自样例本身。"""
    tree_conf = (sem.get("section_tree") or {}).get("tree_confidence") or "low"
    if tree_conf == "high" and has_unit_md:
        return "pinned", "样式与 UnitPattern 均已人工定稿"
    if tree_conf == "high":
        return "drafted", "样式可信，但 UnitPattern 缺人工定稿版"
    return "weak", "样例结构识别置信度不足（%s），派生后须重跑 +learn" % tree_conf


def build_fixed_pieces(sem, spec):
    """汇出固定件：页眉、CTA、免责声明、联系方式名录。

    这些是「每期照抄」的东西，恰恰也是最容易在新一期里被写错的
    （比如漏掉免责声明、把上一年的名录照搬）。写死成文件，复用时零思考。
    """
    L = ["# 固定件全文\n",
         "> 每期照抄的部分。**唯一例外**：联系方式与编辑部名单每期必须核对，\n",
         "> 人员流动会让照抄变成事故。\n\n"]

    chrome = spec.get("chrome") or {}
    running = chrome.get("running_head") or []
    L.append("## 一、页眉 / 页脚\n\n")
    if running:
        for r in running[:3]:
            L.append("- 「%s」　%.1fpt　%s　位于 y=%.1fmm\n" % (
                r.get("text"), r.get("size_pt") or 0, r.get("color") or "", r.get("y_mm") or 0))
    else:
        L.append("- 未识别出页眉（样例可能无 running head）\n")
    folio = chrome.get("folio") or {}
    if folio:
        L.append("- 页码：%s 对齐，y=%.1fmm，%.1fpt，%s\n" % (
            folio.get("align") or "?", folio.get("y_mm") or 0,
            folio.get("size_pt") or 0, folio.get("color") or ""))
    L.append("\n")

    fps = sem.get("fixed_pieces") or {}
    page_head_texts = set(r.get("text") for r in (chrome.get("running_head") or []))
    per_unit = fps.get("running_head_candidates") or []
    L.append("\n## 二、每单元固定尾句（CTA）\n\n")
    # 页眉剔除后剩下的「几乎每单元都出现」的短语才是固定尾句。
    # 语义层把它混在 running_head_candidates 里 —— 因为它的重复频次与页眉同一量级。
    actions = [c for c in per_unit
               if c["text"] not in page_head_texts and len(c["text"]) <= 10 and c["count"] >= 10]
    if actions:
        for c in actions:
            L.append("- 「%s」×%d\n" % (c["text"], c["count"]))
        L.append("\n> 每单元结尾必须有，漏掉会显得像没写完。\n")
    else:
        L.append("- 未识别\n")

    # cta_candidates 是「出现 3-14 次」的短句，实测多为实体词或小标题，
    # 不是固定话术。列出来只是给人工复核留线索，不能直接采用。
    low = fps.get("cta_candidates") or []
    L.append("\n## 二点五、待判定候选（勿直接采用）\n\n")
    if low:
        L.append("> 这批出现 3–14 次，实测多为实体词或小标题而非固定话术。\n")
        L.append("> 仅作复核线索，**确认是真尾句才写进上一节**。\n\n")
        for c in low[:10]:
            L.append("- 「%s」×%d\n" % (c["text"], c["count"]))
    else:
        L.append("- 无\n")

    dis = fps.get("disclaimer_candidates") or []
    L.append("\n## 三、免责声明\n\n")
    if dis:
        for d in dis[:3]:
            L.append("- %s\n" % (d.get("text") if isinstance(d, dict) else d))
    else:
        L.append("- ⚠️ **样例里没抽到免责声明**，可能是因为它是图片或在扫描件里。\n")
        L.append("  **发布前必须人工补录**——这类内容漏掉是法律风险，不是排版问题。\n")

    contacts = fps.get("contact_list") or []
    L.append("\n## 四、联系方式 / 分支机构名录\n\n")
    if contacts:
        L.append("共 %d 条：\n\n" % len(contacts))
        for c in contacts:
            L.append("- %s\n" % (c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)))
        L.append("\n> 每期核对增减，不要直接照抄上期。\n")
    else:
        L.append("- 未识别（通常在封底或跨页图里）\n")

    return "".join(L)


def build_glossary(sem):
    """术语表：高频法规名 / 机构名 / 地区名。

    术语统一是内刊最容易掉链子的地方——同一份条例在不同文章里三种简称。
    这里按词频给出候选，让人工圈定「统一写法」。
    """
    terms = sem.get("terms") or {}
    title_map = {
        "statutes_top": "法规 / 文件名",
        "terms_top": "专业术语 / 固定提法",
        "orgs_top": "机构名",
        "regions_top": "地区名",
        "people_top": "人名",
    }
    L = ["# 术语与实体表\n",
         "> 从样例按词频自动提取。**这不是建议写法**，只是候选清单：\n",
         "> 请在「统一写法」列手工定成你刊的标准形式，尤其注意简称是否合规。\n\n"]

    any_group = False
    for key, items in terms.items():
        if not items or not isinstance(items, list):
            continue
        any_group = True
        L.append("## %s\n\n" % title_map.get(key, key))
        L.append("| 样例中的写法 | 出现 | 统一写法 |\n|---|---|---|\n")
        for it in items[:30]:
            if isinstance(it, dict):
                name, n = it.get("name"), it.get("n", "")
            else:
                name, n = it, ""
            L.append("| %s | %s |  |\n" % (name, n))
        L.append("\n")

    if not any_group:
        L.append("（样例里没抽出成规模的高频实体，请手工建立术语表）\n")
    return "".join(L)


def build_last_issue(sem):
    """上期清单：栏目 → 篇目 → 印刷页码 → 篇幅。

    它的价值不是存档，而是**给新一期定容量**：
    上期栏目 02 是 6 篇 2 854–6 848 字，那新一期偏差超过这个区间就要先问。
    """
    L = ["# 上期基线\n",
         "> 两个用途：① 复用结构；② **给新一期定容量**——\n",
         "> 偏离这里记录的数量级时，先问用户是扩刊还是缩刊，别自己决定。\n\n"]

    st = sem.get("section_tree") or {}
    L.append("> 结构识别置信度：**%s**\n\n" % (st.get("tree_confidence") or "low"))

    contents = sem.get("contents") or {}
    parts = contents.get("parts") or []
    entries = contents.get("entries") or []
    if parts or entries:
        L.append("## 一、目录清单\n\n")
        for p in parts:
            pid = p.get("id")
            L.append("### %s %s\n\n" % (pid, p.get("name")))
            got = [e for e in entries if e.get("part_id") == pid]
            if not got:
                L.append("- （样例目录里该栏目下没解析到条目）\n")
            for e in got:
                pg = ("p.%d" % e["page"]) if e.get("page") else "页码未知"
                L.append("- %s　%s\n" % (e.get("title"), pg))
            L.append("\n")

    um = sem.get("unit_metrics") or {}
    L.append("## 二、篇幅基线（字数，含分节）\n\n")
    allu = um.get("all_units") or {}
    if allu:
        L.append("- 全部单元：**%d 篇**，中位 **%d** 字，区间 %d–%d\n" % (
            allu.get("n", 0), allu.get("median", 0), allu.get("min", 0), allu.get("max", 0)))
    per = um or {}
    pp = per.get("per_part") or {}
    if pp:
        L.append("\n| 栏目 | 篇数 | 中位字数 | 区间 |\n|---|---|---|---|\n")
        for name, s in pp.items():
            L.append("| %s | %d | %d | %d–%d |\n" % (
                name, s.get("n", 0), s.get("median", 0), s.get("min", 0), s.get("max", 0)))

    pu = sem.get("paragraph_units") or []
    L.append("\n## 三、段落型单元（不进目录的重复条目）\n\n")
    if not pu:
        L.append("- 无\n")
    for x in pu:
        c = x.get("chars") or {}
        L.append("- **%s** ×%d：中位 %d 字（%d–%d）；切分正则 `%s`\n" % (
            x.get("kind"), x.get("count", 0), c.get("median", 0),
            c.get("min", 0), c.get("max", 0), x.get("split_regex")))
    return "".join(L)


# --------------------------------------------------------------------------- 生成

def render_skill_md(ctx):
    """派生 skill 的主文件。

    刻意写短：子技能不承担方法论，只承担「这本刊是什么 + 每期做什么 + 出事了找谁」。
    方法论在父技能，避免两处维护导致漂移。
    """
    return u"""---
name: {name}
slug: {slug}
displayName: {displayName}
version: 0.1.0
summary: "{publisher}《{title}》{kind}的期刊底稿技能。版式与内容模板已固化，直接进需求对齐开工，不必重跑样式学习。"
tags:
  - 企业期刊
  - {kind}
  - 底稿生成
description: "{publisher}《{title}》的期刊底稿技能（{kind}）。已固化版式与内容模板，直接进需求对齐开工，不必重跑样式学习。Triggers: {title} 新一期 / 做第N期 / {alias} / {publisher}期刊。需要通用排版能力或改版时回落到 journal-draft。"
license: MIT
agent_created: true
metadata:
  version: "0.1.0"
  layer: "instance"
  parent: "journal-draft"
  derives_from: "{derives_from}"
  spec_confidence: "{confidence}"
  requires:
    bins: ["python", "python3"]
    optionalSkills: ["cue-research", "cue-omni-reader", "cue-buddy"]
    optionalMcp: ["omni-reader"]
    # 「可选」只表示「不装也能跑」，不表示「默认不用」：每期开工必须主动推荐并等用户确认（见 §四）
    recommendedSkills: ["cue-research", "cue-omni-reader"]
---

# {name} — 《{title}》底稿

> 这是 **journal-draft 的派生实例**，不是重新设计的方法论。
> 版式与内容模板已在这份技能里钉死，日常开工**不需要**再给样例、跑样式学习。

**派生质量：{confidence}（{confidence_note}）**

## 一、这本刊是什么

| | |
|---|---|
| 发行方 | {publisher} |
| 刊名 | 《{title}》 |
| 类型 | {kind} |
| 版面 | {canvas} |
| 主色 | {primary} |
| 栏目 | {sections} |

版式全文见 [`assets/stylespec.json`](assets/stylespec.json)，
内容模板见 [`assets/unit-patterns.md`](assets/unit-patterns.md)。
{boundary}

## 二、每期固定动作

1. **可直接复用的**（无需询问）：栏目结构、固定件全文（见 `fixed-pieces.md`）、版式参数、页面模板映射。
2. **必须核对的**：联系方式与人员名单（[`assets/fixed-pieces.md`](assets/fixed-pieces.md) 第四节）——人员流动会让照抄变成事故。
3. **每期重取的**：期号、年月、当期话题、封面图、新的第三方引用。

## 三、容量约束（超出就要先问）

上期基线在 [`assets/last-issue.md`](assets/last-issue.md)。
**篇数或中位字数偏离基线超过约三成时，先确认是扩刊 / 缩刊 / 合刊，不要自行决定。**

## 四、开工路径

```
+brief   对齐本期需求 —— 唯一必须的一轮确认；把「有无素材库 / 材料能否上传 / Cue 与 Omni
         该不该用（逐条给判定与成本）」一并问掉，见 §四「Cue / Omni 通道」
+gather  按 sources.md 取料；缺的外部佐证走 Cue（参照 runbook.md 里的额度经验）
+draft   写稿 → build_draft.py 出 HTML、export_pdf.py 出 PDF、export_editable.py 出 docx/md
+art     配图 —— 语义图（流程 / 框架 / 分工 / 路径）走 gen_diagram.py 矢量绘制；只有封面题花这类氛围图才用文生图
+check   crosscheck.py + check_freshness.py + qa-checklist → 交付
```

**开工时建 `progress.md` 台账**，每完成一个阶段记一行「状态 / 产出文件 / 已确认项」。
中断后接手先读它，**用户答过的问题不再重问**——子技能场景通常只该问 1–2 批，
问到第三批就说明 `+brief` 没问到位。台账模板见 [`assets/templates/progress.template.md`](assets/templates/progress.template.md)，
起手模板一整套都在 [`assets/templates/`](assets/templates/)（已随本技能打包，不依赖父技能安装位置）。

### 与本技能的父技能（`journal-draft`）是什么关系

| 资产 | 在哪 | 为什么 |
|---|---|---|
| **脚本**（`scripts/*.py`） | **本技能自带** | 派生技能必须自包含，装到别的机器上要能直接跑 |
| **起手模板**（`assets/templates/`）与**语义图版式**（`assets/diagram-templates/`） | **本技能自带** | 它们是稳定资产，与刊物无关；拷进来才不会断链 |
| **完整方法论**（`references/*.md`：类型学、取料矩阵、校订清单、可编辑稿规范……） | **父技能** | 会随框架演进；拷一份到子技能会立刻过期。本节与「四件」「通道」两节已给日常所需的最小口径 |

父技能**未安装**时，本技能仍然完整可跑（脚本与模板都在），只是拿不到 `references/` 里的
深入章节。遇到这几类问题再回父技能：换了开本或分栏、要加新的页面模板、
刊物类型换了（周期刊 → 年鉴 / 特刊 / 汇编）、要做双语版——它们的判断口径在
父技能 `references/journal-types.md`。

日常**不要**跑 `+learn`：样式已钉死。只有两种情况回到父技能 `journal-draft`：
① 用户带了新版样例或要求改版；② 要做这份技能从未做过的页面类型。

### 编辑质量：不许把底稿做成信息堆叠

**开工先定本期编辑方针四问**（写进 `issue-brief.md` 顶部）：① 谁看（具体到岗位与处境）
② 看完做什么（具体到动作）③ 记住什么（本期只留一句是哪句）④ 为什么是我们说。

内容分四级，**纯 L0 的条目整期不超过一半**：

| 级 | 是什么 | 判据 |
|---|---|---|
| L0 事实 | 时间 / 主体 / 文号 / 金额 | 可核查、有出处 |
| L1 影响 | 对谁、在哪件事上、改变了什么 | 必须点名**受影响的主体与具体环节**；「具有重要意义」＝零信息 |
| L2 判断 | 为什么这样定、边界在哪、容易踩哪条线 | 换成别人写会写得不一样 |
| L3 行动 | 读者接下来做什么、什么时点前 | 能落成**动作 + 时点**；「建议持续关注」不是行动 |

- 快讯/动态：每条至少一句 L1；
- 深度文章：L0 打底 + 至少 3 处 L2 + 结尾一段 L3 + **至少一处反直觉提醒**
  （写不出这一处，就不算深度文章，退回动态条目）；
- **遮掉机构名还看得出是谁写的吗**——看不出就是搬运，补 L2；
- 篇幅不够去补素材与证据，**不许把每条从 180 字灌到 400 字**。

### 定位：先定「写给谁、为什么写」，再定调子

四问的答案必须落成 **`positioning.json`** —— 与 `stylespec.json` 平级的**第二份机器可读产物**
（`stylespec` 管长什么样，`positioning` 管写给谁、为什么写、用什么调子说）。
模板已随本技能打包在 `assets/templates/positioning.template.json`，可离线填。

| 段 | 内容 |
|---|---|
| `purpose` | 六选一主目的（A 品牌心智 / B 获客转化 / C 客户留存 / D 合规传达 / E 员工凝聚 / F 投资者关系），**只能一个** |
| `audience` | 岗位＋处境＋专业水平(1–5)＋**时间预算(分钟)** |
| `value_promise` | 一句话承诺 + `reader_action`（动词短语，读者读完要做的动作） |
| `tone` | 权威・密度・立场 三刻度 1–5，**直接换算单条字数带与句长上限** |
| `industry_rules` | 术语密度上限、行业忌讳词、必标出处 |

**调性是前三项的结果，不是起点**——先定目的与读者，再推调子；反过来挑一个
「看着舒服」的调子，等于没定位。同一件事写给外部客户 / 员工 / 投资者 / 公众，
切哪一段、要他做什么、写多少字全都不同（四种写法对照见父技能
`references/audience-value.md` §三）。

交付前跑：

```bash
python <本技能>/scripts/audit_editorial.py --content content.json --positioning positioning.json
```

管的是**「对不对路」**：定位卡完整度 / 单条字数是否落在字带 / 兑现 `reader_action` 的条目
覆盖率（<50% FAIL）/ 纯 L0 占比（>50% FAIL）/ 句长中位 / 术语密度与忌讳词。
缺定位卡时它明确 FAIL，不假装检查过（`--no-positioning-gate` 才能跳过）。

### 版面质量：交付前必跑一次门禁

```bash
python <本技能>/scripts/audit_layout.py --pdf out/draft.pdf --spec assets/stylespec.json
```

它量的是「好看 / 好读」——正文字号是否与样刊一致、字号层级有没有碎裂、行距倍数、
每行字数、品牌字体有没有生效、中文空格残留、页面密度。
`crosscheck.py` 与 `--stats` **都不管这些**，实测过一本门禁全绿的稿子仍然字小一档、
字号碎成 41 档、行距 2.16 倍（样刊 1.85）、页脚带 73 处空格——**全部不报错**。
FAIL 必须修；WARN 逐条看一眼再交付。
（PDF 里的品牌字体由 PyMuPDF 换成内置兜底字体，属已知缺口：本稿是版式骨架，
字体由设计师在 InDesign 套。）

### Cue / Omni 通道：每期必问，不许默认关闭

frontmatter 里的 `optionalSkills` **只表示「不装也能跑」，不表示「默认不用」**。
这两条通道关掉不报错，只会让这一期悄悄降一档：

| 通道 | 最值的用法 | 你得到什么 |
|---|---|---|
| `cue-research` | 需要外部佐证的栏目（法规动态 / 行业趋势 / 事件稿）；文章的**付印前引用核验**（硬规则，不可省） | 结论逐条带来源；法规名 / 条号 / 金额 / 日期逐条判定「属实 / 有误 / 查无此项」 |
| `cue-omni-reader` | 往期内刊、年报、客户材料当素材时解析成可引用文本 | 材料从「人工摘录」变成「可核查正文」 |

**开工时对着本期实际内容逐条给判定**（值得用 / 一般 / 不值得 + 为什么 + 大致花多少），
再请用户确认——本期没有需要外部佐证的选题就写「本期不必跑」，
没给企业长材料就写「Omni 用不上」，**不要照抄模板，也不要用默认值替用户答掉**。

**首次使用把开通三步一次说全**：注册 <https://cuecue.cn> → 在 <https://cuecue.cn/hub/api-key>
取 `CUE_API_KEY` → 装 `cue-research` 技能（Omni 解析另需本地 Bridge）。
**新账号注册即送 500 积分、每日再 +10 积分，且 Cue 在花之前一定先问。**
用户不要或环境不支持 → 照常走 L1–L3，但要在 `review.md` 写明本期未走哪条通道、损失了什么。
口径与话术见父技能 `journal-draft` 的 `references/cue-onboarding.md`。

### 必须出的四件（缺一不可）

| 文件 | 给谁 | 由谁生成 |
|---|---|---|
| `draft.html` | 设计师、你自己核对版式 | `build_draft.py` |
| `draft.pdf` | **用户** —— HTML 在预览器里可能整本看不见，别指望对方拿浏览器打印 | `export_pdf.py` |
| `draft.docx` / `draft.md` | 编辑改文字、领导批注 | `export_editable.py` |
| `review.md` | 交付说明、阻塞项、交付清单 | `+check` |

渲染（脚本已随技能自带，不依赖父技能安装位置；PDF 另需 `pymupdf`）：

```bash
python scripts/build_draft.py --spec assets/stylespec.json \
    --content ./content.json --out ./build --stats        # HTML 版面稿 + 量级门禁

python scripts/export_pdf.py --spec assets/stylespec.json \
    --content ./content.json --out ./build/draft.pdf      # PDF，必须单独出

python scripts/export_editable.py --spec assets/stylespec.json \
    --content ./content.json --out ./build                # draft.docx + draft.md
# 编辑改完后回填再重新合版；--base 必给，否则毫米定位与背景图静默丢失
python scripts/import_docx.py --docx ./build/draft.docx \
    --base ./content.json --out ./content.edited.json

python scripts/crosscheck.py --content ./content.json \
    --html ./build/draft.html --md ./build/draft.md --pdf ./build/draft.pdf
python scripts/check_freshness.py --content ./content.json --issue-date <付印日>
```

（docx 需要 `python -m pip install python-docx`；只要 Markdown 就加 `--only md`。
`python` 是占位符：先 `python --version` 确认命令存在，失败就试 `python3`
或平台托管解释器的绝对路径。）

**交付不是「回一句已生成」**：把 `draft.pdf` 与 `draft.docx` 用文件预览打开给用户看，
附三句（页数与达成率 / 阻塞项条数 / 还需要用户做什么），交付清单写进 `review.md` 末尾。

## 五、还没填的坑

派生时以下几项**没有真值**，首次开工前必须补齐，否则会带着错误一路走到定稿：

{open_items}

补齐后请同步删掉本节的对应条目——它是对自己的待办清单，不是给别人看的说明。
""".format(**ctx)


def render_readme(ctx):
    """改造指南。这是公开发布时真正给用户看的东西：怎么把样例换成自家。"""
    return u"""# 把这份样例技能改成你自己的

> 这份技能是 journal-draft 的一个**成品样例**，可以三类用法：
> ① 直接拿去做《{title}》的下一期；② 照着结构改成你公司的刊；
> ③ 只当参考——看一本真实刊物的版式与内容模板被抽成了什么样。
>
> 改造成自己之前，建议先完整跑一遍，知道每个文件在什么时候被用到。

## 一、先分清三类文件

| 类别 | 文件 | 改造时要不要动 |
|---|---|---|
| **已钉死** | `assets/stylespec.json`、`assets/unit-patterns.md` | **不要手改**。它们是这台机器的参数；要改请用父技能 `journal-draft` 重新 `+learn` 一遍样例 |
| **待填清单** | `sources.template.md`、`runbook.template.md` | **必须填**。填上后把 `.template` 后缀去掉 |
| **每期变** | `assets/last-issue.md`、`SKILL.md` 的期次信息 | 每期更新，尤其 `last-issue.md`——它是新一期的容量基线 |

## 二、换成自家的最小改动

1. **换名字**：改 `SKILL.md` 的 frontmatter（`name` / `description` / Triggers）。
   `description` 里必须带上你刊的真实叫法和别名，否则触发不到。
2. **换版式**：**不要手改 stylespec.json**。拿你家的一期刊物当样例，
   用父技能跑一遍 `+learn`，产出替换掉 `assets/stylespec.json`。手改几十个字段必然漏。
3. **换内容模板**：重写 `assets/unit-patterns.md`。这是最值得花时间的一份——
   版式可以错一点，**内容模板错了整本刊都是错的**。每条至少要包含：slot 清单、
   字数硬指标、固定件要求、3 条真实例句。
4. **换固定件**：`assets/fixed-pieces.md` 填免责声明全文与名录。
   免责声明漏掉是法律风险，不是排版问题。
5. **填数据源**：`sources.template.md` 列官网栏目、公众号、监管机构原文站点。
6. **术语表**：`assets/glossary.md` 的「统一写法」列手工填——同一份条例在
   不同文章里出现三种简称，是内刊最常见的硬伤。

## 三、判断改好了没有

拿一期的真实素材跑一遍，然后看两个数字：

- **被打断几次**：确认提问应当在一轮内完成（父技能规定 ≤5 个问题且必带默认值）。
  超过一轮说明 `+brief` 没问到位，回到 `sources.md` 和固定件清单找原因。
- **直接可用比例**：产出的底稿里，多少比例的内容可以不改就进设计。
  低于一半通常是 UnitPattern 写得不够具体——回去补例句和字数硬指标。

## 四、什么时候别派生

- 只做过一期、还没拿到内部反馈
- 刊物本身在改版中
- 只是想看看效果

派生是承诺：一旦钉死，后续就照它执行。**样式定了再派生。**

## 五、派生过程

由父技能 `journal-draft` 的 `scripts/derive_skill.py` 生成：

```bash
python ~/.workbuddy/skills/journal-draft/scripts/derive_skill.py \\
    --spec ./stylespec.json --unit-patterns ./unit-patterns.md \\
    --out ~/.workbuddy/skills/<你的技能名> \\
    --name <你的技能名> --publisher "<发行方>" --title "<刊名>"
```

**机器粗加工 ≠ 定稿。** 生成的 `spec_confidence` 若为 `drafted` 或 `weak`，
`unit-patterns.md` 是由样例统计倒推的草稿，**投产前必须人工复核并定稿**。
""".format(**ctx)


def render_sources(ctx):
    return u"""# 数据源清单 — 《{title}》

> 派生时自动 drafted，**没有真值**。首次开工前填完，并把本文件改名为 `sources.md`。
> 填得越具体，后续每期省下的沟通越多。

## 一、企业官方源（自己说了算的部分，优先用）

| 用途 | 入口 | 更新频率 | 备注 |
|---|---|---|---|
| 官网新闻 / 公告 | | | |
| 微信公众号 | | | 公众号正文往往需要登录态，取不到时直接向业务方要原文 |
| 年报 / 季报 | | | |
| 分支机构动态 | | | |

## 二、权威原文（引用不能出错的部分）

| 监管机构 | 原文站点 | 覆盖地区 |
|---|---|---|
| | | |

> 引用外部文件时**必须**落到原文 URL + 发布主体 + 发布日期。
> 二手来源是偏误的来源：引错监管机构名称或生效日期，比不引更糟。

## 三、Cue 深度研究（官方源没有的才用）

| 话题类型 | 走的技能 / 搭子 | template_id | 上期额度 |
|---|---|---|---|
| | | | |

先用 `cue_api.py list` 查有没有现成搭子，再决定要不要做新的。
固化判据见父技能 `references/cue-buddy-map.md`。

## 四、明确不用的源

| 源 | 为什么不用的原因 |
|---|---|
| | |
""".format(**ctx)


def render_runbook(ctx):
    return u"""# Runbook — 《{title}》

> 每期跑完更新一次。它的价值是让第 N 期不必重踩第 N-1 期的坑，
> 也为下一期给出可信的成本预期。

## 进度

| 期次 | 日期 | 篇数 | 总字数 | Cue 花费 | 返工轮次 |
|---|---|---|---|---|---|
| {first_issue} | | | | | |

## 额度经验（填进去，下次照着报成本）

| 环节 | 单位成本 | 备注 |
|---|---|---|
| 样例解析（omni-reader，text 档） | 约 0.07 credits / 页 | 91 页样例实测 6.432 |
| Cue 搭子跑一次 | 视搭子而定 | 见 sources.md 第三节 |
| 配图出图（agent 内置多模态能力） | 无额外配置、无 key | 产出可能带角落水印，印刷前重出或裁切 |

## 踩坑记录

> 只写「下次还会踩」的坑。一次性失误不必记录。

| 现象 | 根因 | 应对 |
|---|---|---|
| | | |

## 用户的偏好决策

> 记录用户反复选择默认值的那些问题。下次直接按默认值走，不必再问。

| 问题 | 用户的默认选择 |
|---|---|
| | |
""".format(**ctx)


def open_items(spec, sem, has_unit_md):
    """派生时确实缺真值的项——写进 SKILL.md 第五节，作为自检清单。"""
    items = []
    fps = sem.get("fixed_pieces") or {}
    if not fps.get("disclaimer_candidates"):
        items.append("- **免责声明没抽到**（样例中可能为图片）：见 `assets/fixed-pieces.md` 第三节，必须人工补录")
    if not fps.get("contact_list"):
        items.append("- **联系方式名录没抽到**：填写 `assets/fixed-pieces.md` 第四节")
    if not has_unit_md:
        items.append("- **UnitPattern 是机器草稿**：`assets/unit-patterns.md` 由样例统计倒推，"
                     "投产前须人工复核并用真实例句替换")
    gl = sem.get("terms") or {}
    if not (gl.get("statutes_top") or gl.get("orgs_top")):
        items.append("- **术语表为空**：`assets/glossary.md` 需手工建立，至少覆盖高频法规名与机构名")
    items.append("- **数据源清单未填**：`sources.template.md` 填完后改名为 `sources.md`")
    items.append("- **Runbook 未填**：首期跑完后把真实额度与踩坑写进 `runbook.template.md`")
    return "\n".join(items)


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="从样例派生出一份独立可用的场景技能")
    ap.add_argument("--spec", required=True, help="定稿的 stylespec.json（含 semantic 段）")
    ap.add_argument("--unit-patterns", help="人工定稿的 unit-patterns.md；缺失则自动倒推草稿")
    ap.add_argument("--out", help="输出目录，默认 ~/.workbuddy/skills/<name>")
    ap.add_argument("--name", required=True, help="技能名，如 journal-qiming-regional")
    ap.add_argument("--slug", default="",
                    help="发布用 slug（SkillHub 要求 kebab-case 且全网唯一）；默认取 --name，"
                         "非 kebab-case 时自动规范化，被占用可在此加 handle 前后缀")
    ap.add_argument("--publisher", required=True, help="发行方全称")
    ap.add_argument("--title", required=True, help="刊名（不用带书名号《》，带也会自动去掉）")
    ap.add_argument("--kind", default="客户通讯", help="期刊类型，如 双月刊 / 内刊 / 年报")
    ap.add_argument("--alias", default="", help="别名或简称，多个用 / 分隔")
    ap.add_argument("--first-issue", default="第 1 期（派生基线）", help="上期期次标识")
    ap.add_argument("--force", action="store_true", help="目标目录已存在时覆盖")
    args = ap.parse_args()

    spec_raw = load_json(args.spec)
    sem = spec_raw.get("semantic") or {}
    if not sem:
        # 允许单独传 semantic.json
        cand = os.path.join(os.path.dirname(args.spec), "semantic.json")
        if os.path.exists(cand):
            sem = load_json(cand)

    out = args.out or os.path.join(default_home(), ".workbuddy", "skills", args.name)
    if os.path.exists(out) and not args.force:
        print("[ERROR] 目标已存在：%s（加 --force 覆盖）" % out, file=sys.stderr)
        return 2

    unit_md = load_text(args.unit_patterns).strip()
    has_unit_md = bool(unit_md)
    if not has_unit_md:
        unit_md = auto_unit_patterns(sem)

    confidence, conf_note = pick_confidence(sem, has_unit_md)

    canvas = spec_raw.get("canvas") or {}
    size = canvas.get("size_mm") or []
    canvas_txt = "%s %s" % (canvas.get("standard_size") or "自定义",
                            "×".join("%g" % x for x in size) + "mm" if size else "")
    palette = (spec_raw.get("palette") or {}).get("roles") or {}
    st = sem.get("section_tree") or {}
    parts = st.get("parts") or {}
    sections = "、".join("%s %s" % (k, v.get("name")) for k, v in sorted(parts.items())) or "（未识别）"

    # --- 发布用标识：slug / displayName -------------------------------------
    # 子技能常常要独立发布到技能市场，而平台的硬校验只认 slug / version / displayName
    # 三个字段。以前这三项要用户事后手改 SKILL.md，漏一个就发不上去。
    title_clean = re.sub(r"^[《【\s]+|[》】\s]+$", "", args.title.strip())
    raw_slug = (args.slug or args.name).strip()
    slug = re.sub(r"[^a-z0-9]+", "-", raw_slug.lower()).strip("-")
    if len(slug) < 2:
        slug = "journal-" + (slug or "instance")
    if slug != raw_slug:
        print("  [NOTE] slug 已规范化为 %r（原 %r）；如需固定请显式传 --slug"
              % (slug, raw_slug))

    ctx = {
        "name": args.name,
        "slug": slug,
        "displayName": "%s《%s》期刊底稿技能" % (args.publisher, title_clean),
        "publisher": args.publisher,
        "title": title_clean,
        "kind": args.kind,
        "alias": args.alias or title_clean,
        "canvas": canvas_txt or "（见 stylespec.json）",
        "primary": palette.get("primary") or "（见 stylespec.json）",
        "sections": sections,
        "confidence": confidence,
        "confidence_note": conf_note,
        "derives_from": spec_raw.get("meta", {}).get("source_file") or "样例期刊 PDF",
        "first_issue": args.first_issue,
    }
    ctx["open_items"] = open_items(spec_raw, sem, has_unit_md)

    # 边界告警：渲染器只出单栏，五个组件的几何按 A4 调。派生前不把这两条写进
    # 子技能，子技能就会带着「能复现」的错觉投产——实测衡石双栏刊（227×276mm，
    # 2×94.8mm）派生后照常按单栏全宽渲染：脚本零报错、unknown=0、三件套齐全、
    # 页数与达成率全对，**版式全错**，只有量正文栏宽才能发现（父技能硬规则 24）。
    boundary = []
    raw_cols = canvas.get("columns")
    try:
        cols = int(raw_cols) if raw_cols is not None else 1
    except (TypeError, ValueError):
        cols = 1
    if cols >= 2:
        boundary.append(
            "**双栏 / 多栏正文——不复现。** 派生时检出 `canvas.columns=%d`，"
            "而渲染器只出单栏，版式会按全文宽度排。本技能照常可跑，但"
            "**版面稿只是单栏骨架，分栏必须设计师接管**；交付时明说，"
            "并写进 `review.md` 的未复现项。换刊型 / 改版时回父技能重跑 `+learn`。" % cols)
    w, h = (list(size) + [0, 0])[:2] if size else (0, 0)
    is_a4 = ("A4" in (canvas.get("standard_size") or "").upper()
             or (abs(w - 210) < 2 and abs(h - 297) < 2))
    if (w or h) and not is_a4:
        boundary.append(
            "**非 A4 开本——部分复现。** 派生时检出 %s；封面 / 引言 / 目录 / 编委会 / "
            "封底五个组件的几何是按 A4 调的，**这五处需人工微调**（正文版心按 "
            "`stylespec.json` 走，可正常出稿）。交付时明说。" % (canvas_txt or "非 A4"))
    ctx["boundary"] = (
        "\n\n> ### ⚠️ 本刊的已知能力边界（派生时自动检出，开工就要告诉用户）\n>\n"
        "> 下面这几项**在渲染器侧不报错**，只看产出发现不了——所以不能等到交付才说：\n>\n"
        + "".join("> - %s\n>\n" % b for b in boundary)
        + "> 判据与出路见父技能 `references/journal-types.md` §三 / §六。"
    ) if boundary else ""

    if not unit_md.startswith("#"):
        unit_md = "# UnitPattern — %s\n\n%s" % (args.title, unit_md)
    if confidence != "pinned":
        unit_md += ("\n\n---\n\n> ⚠️ **本文件为机器草稿（`spec_confidence: %s`）**："
                    "由样例统计倒推而成，未经人工定稿。\n> 投产前必须逐条复核，"
                    "并用样例里的真实例句替换占位语料。\n" % confidence)

    write_tree(out, {
        "SKILL.md": render_skill_md(ctx),
        "README.md": render_readme(ctx),
        "assets/stylespec.json": json.dumps(slim_spec(spec_raw), ensure_ascii=False, indent=2),
        "assets/unit-patterns.md": unit_md,
        "assets/fixed-pieces.md": build_fixed_pieces(sem, spec_raw),
        "assets/glossary.md": build_glossary(sem),
        "assets/last-issue.md": build_last_issue(sem),
        "sources.template.md": render_sources(ctx),
        "runbook.template.md": render_runbook(ctx),
    })

    # 渲染脚本拷进来：派生技能应当自包含，不能依赖父技能的安装位置
    # build_draft.py 只依赖标准库；export_editable.py 的 md 分支也是，
    # 只有 docx 分支需要 python-docx（缺失时脚本会自己报错说明）
    dst_dir = os.path.join(out, "scripts")
    os.makedirs(dst_dir, exist_ok=True)
    copied = 0
    missed = []
    # 动态取父技能全部脚本，只排除派生器自身。
    # 曾硬编码三个旧名字，导致后加的 export_pdf / check_freshness / crosscheck /
    # plan_images / adopt_images 全部漏拷——派生技能交不出三件套、没有时效门禁。
    src_dir = os.path.join(parent_dir(), "scripts")
    names = sorted(n for n in os.listdir(src_dir)
                   if n.endswith(".py") and n != "derive_skill.py") if os.path.isdir(src_dir) else []
    for name in names:
        src_path = os.path.join(src_dir, name)
        if os.path.exists(src_path):
            with io.open(src_path, "r", encoding="utf-8") as f:
                body = f.read()
            with io.open(os.path.join(dst_dir, name), "w", encoding="utf-8") as f:
                f.write(body)
            copied += 1
        else:
            missed.append(name)
            print("  [WARN] 父技能缺少 scripts/%s，未拷贝" % name)
    if not names:
        print("  [WARN] 未在 %s 找到任何脚本，派生技能无法独立运行" % src_dir)
    else:
        print("  scripts: %s" % "、".join(names))
    if missed:
        print("  [WARN] 缺失脚本：%s" % "、".join(missed))

    # 稳定资产一并打包：起手模板与语义图版式。
    # 实测断链（2026-09-18）：生成的 SKILL.md 里写着「台账模板见父技能
    # assets/templates/progress.template.md」——可子技能被设计成自包含
    # （脚本都拷了），模板却指向父技能；装到没装父技能的机器上，第一节就 404。
    # 判据：**子技能文档里凡是引到 `assets/` 的路径，都必须是它自己的 `assets/`**。
    # references/ 不拷：那是会演进的方法论，拷一份会立刻过期（见 SKILL.md 新增的
    # 「与父技能是什么关系」一节，那节已把日常所需的最小口径写进正文）。
    for pkg in ("assets/templates", "assets/diagram-templates"):
        src_pkg = os.path.join(parent_dir(), pkg)
        if not os.path.isdir(src_pkg):
            print("  [WARN] 父技能缺少 %s，未打包" % pkg)
            continue
        n = 0
        for name in sorted(os.listdir(src_pkg)):
            sp = os.path.join(src_pkg, name)
            if not os.path.isfile(sp):
                continue
            with io.open(sp, "r", encoding="utf-8") as f:
                body = f.read()
            dst = os.path.join(out, pkg, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with io.open(dst, "w", encoding="utf-8") as f:
                f.write(body)
            n += 1
        print("  %s: %d 个文件" % (pkg, n))

    spec_in = len(json.dumps(spec_raw, ensure_ascii=False))
    spec_out = len(json.dumps(slim_spec(spec_raw), ensure_ascii=False))
    print("OK -> %s" % out)
    print("  confidence=%s (%s)" % (confidence, conf_note))
    print("  unit-patterns=%s" % ("pinned" if has_unit_md else "machine draft"))
    print("  stylespec %d -> %d chars (剥离 semantic，省 %.0f%%)" % (
        spec_in, spec_out, 100.0 * (spec_in - spec_out) / max(1, spec_in)))
    print("  scripts copied=%d" % copied)
    if boundary:
        print("  [WARN] 检出 %d 项能力边界，已写入 SKILL.md（开工时必须告知用户）：" % len(boundary))
        if cols >= 2:
            print("         · 双栏正文（canvas.columns=%d）→ 渲染器只出单栏，分栏需设计师接管" % cols)
        if (w or h) and not is_a4:
            print("         · 非 A4 开本（%s）→ 封面/引言/目录/编委会/封底几何需人工微调" % (canvas_txt or "?"))
    if confidence != "pinned":
        print("  [WARN] 投产前需完成 SKILL.md 第五节的待办")
    return 0


def auto_unit_patterns(sem):
    """没有人工定稿时，从 semantic 统计倒推一份草稿。

    这份草稿的价值在于「给出可讨论的起点」，而非可投产的模板——
    必须在 UNIT 文件的显眼处把这一点说清楚。
    """
    L = ["> ⚠️ 由 `derive_skill.py` 从样例统计自动倒推，**请以人工定稿替换**。\n",
         "> 没有单元定稿的生产是批量制造错稿。\n\n"]

    st = sem.get("section_tree") or {}
    um = sem.get("unit_metrics") or {}
    pp = um.get("per_part") or {}
    for pid, part in sorted((st.get("parts") or {}).items()):
        name = part.get("name")
        s = pp.get(name) or {}
        L.append("## 栏目 %s %s\n\n" % (pid, name))
        L.append("- 上期 %d 篇，中位 %d 字，区间 %d–%d\n" % (
            s.get("n", 0), s.get("median", 0), s.get("min", 0), s.get("max", 0)))
        units = part.get("units") or []
        if units:
            L.append("- 角色分布：%s\n" % ", ".join(
                "%s×%d" % (r, len([u for u in units if u.get("role") == r]))
                for r in sorted(set(u.get("role", "?") for u in units))))
            L.append("- 待补 slot：此处需人工按样例逐条写出 slot 清单与字数硬指标\n")
        L.append("\n")

    for x in sem.get("paragraph_units") or []:
        c = x.get("chars") or {}
        L.append("## 段落型单元 %s\n\n" % x.get("kind"))
        L.append("- 上期 %d 条，中位 %d 字（%d–%d）\n" % (
            x.get("count", 0), c.get("median", 0), c.get("min", 0), c.get("max", 0)))
        L.append("- 切分正则：`%s`\n" % x.get("split_regex"))
        L.append("- 样例：%s\n\n" % (x.get("samples") or [""])[0][:120])
    return "".join(L)


def write_tree(root, files):
    for rel, body in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with io.open(p, "w", encoding="utf-8") as f:
            f.write(body)
        print("  + %s (%d chars)" % (rel, len(body)))


if __name__ == "__main__":
    sys.exit(main())
