---
name: journal-hengshi-observation
slug: journal-hengshi-observation
displayName: 衡石《深度观察》期刊底稿技能
version: 0.2.2
summary: "衡石律师事务所《衡石深度观察》月刊的期刊底稿技能。版式与内容模板已固化（227×276mm 双栏 / 52 页 / 纯文章型）；注意其 spec_confidence 为 weak，是框架的「反向样本」，派生后须重跑 +learn 才能投产。"
tags:
  - 期刊
  - 月刊
  - 律师事务所
  - 反向样本
  - 底稿生成
description: "衡石律师事务所《衡石深度观察》的期刊底稿技能（月刊）。已固化版式与内容模板，直接进需求对齐开工，不必重跑样式学习。Triggers: 衡石深度观察 新一期 / 做第N期 / 衡石深度观察 / 衡石律师事务所期刊。需要通用排版能力或改版时回落到 journal-draft。"
license: MIT
agent_created: true
metadata:
  version: "0.2.2"
  layer: "instance"
  parent: "journal-draft"
  derives_from: "hengshi-observation-2026-08.pdf"
  spec_confidence: "weak"
  requires:
    bins: ["python"]
    optionalSkills: ["cue-research", "cue-omni-reader", "cue-buddy"]
    optionalMcp: ["omni-reader"]
    # 「可选」只表示「不装也能跑」，不表示「默认不用」：每期开工必须主动推荐并等用户确认（见 §四）
    recommendedSkills: ["cue-research", "cue-omni-reader"]
---

# journal-hengshi-observation — 《衡石深度观察》底稿

> 这是 **journal-draft 的派生实例**，不是重新设计的方法论。
> 版式与内容模板已在这份技能里钉死，日常开工**不需要**再给样例、跑样式学习。

**派生质量：weak（样例结构识别置信度不足（low），派生后须重跑 +learn）**

## 一、这本刊是什么

| | |
|---|---|
| 发行方 | 衡石律师事务所 |
| 刊名 | 《衡石深度观察》 |
| 类型 | 月刊 |
| 版面 | custom 227×276mm |
| 主色 | #B5272D |
| 栏目 | （未识别） |

版式全文见 [`assets/stylespec.json`](assets/stylespec.json)，
内容模板见 [`assets/unit-patterns.md`](assets/unit-patterns.md)。

> ### ⚠️ 本刊的已知能力边界（派生时自动检出，开工就要告诉用户）
>
> 下面这几项**在渲染器侧不报错**，只看产出发现不了——所以不能等到交付才说：
>
> - **双栏 / 多栏正文——不复现。** 派生时检出 `canvas.columns=2`，而渲染器只出单栏，版式会按全文宽度排。本技能照常可跑，但**版面稿只是单栏骨架，分栏必须设计师接管**；交付时明说，并写进 `review.md` 的未复现项。换刊型 / 改版时回父技能重跑 `+learn`。
>
> - **非 A4 开本——部分复现。** 派生时检出 custom 227×276mm；封面 / 引言 / 目录 / 编委会 / 封底五个组件的几何是按 A4 调的，**这五处需人工微调**（正文版心按 `stylespec.json` 走，可正常出稿）。交付时明说。
>
> 判据与出路见父技能 `references/journal-types.md` §三 / §六。

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

### 与父技能（`journal-draft`）是什么关系

| 资产 | 在哪 | 为什么 |
|---|---|---|
| **脚本**（`scripts/*.py`） | **本技能自带** | 派生技能必须自包含，装到别的机器上要能直接跑 |
| **起手模板**（`assets/templates/`）与**语义图版式**（`assets/diagram-templates/`） | **本技能自带** | 稳定资产，与刊物无关；拷进来才不会断链 |
| **完整方法论**（`references/*.md`：刊物类型学、取料矩阵、校订清单、可编辑稿规范……） | **父技能** | 会随框架演进；拷一份到子技能会立刻过期。本节与「四件」「通道」两节已给日常所需的最小口径 |

父技能**未安装**时，本技能仍完整可跑（脚本与模板都在），只是拿不到 `references/` 里的深入章节。
遇到这几类问题才需要回父技能：换了开本或分栏、要加新的页面模板、
刊物类型换了（周期刊 → 年鉴 / 特刊 / 汇编 / 双语版）——判断口径在父技能的
`references/journal-types.md`。

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

| 通道 | 这本刊最值的用法 | 你得到什么 |
|---|---|---|
| `cue-research` | 深度观察文的外部佐证；全部文章的**付印前引用核验**（硬规则，不可省） | 结论逐条带来源；法规名 / 条号 / 金额 / 日期逐条判定「属实 / 有误 / 查无此项」 |
| `cue-omni-reader` | 往期观察文、客户材料当素材时解析成可引用文本 | 材料从「人工摘录」变成「可核查正文」 |

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
python scripts/audit_layout.py --pdf ./build/draft.pdf --spec assets/stylespec.json
python scripts/audit_editorial.py --content ./content.json --positioning positioning.json
```

（docx 需要 `python -m pip install python-docx`；只要 Markdown 就加 `--only md`。
`python` 是占位符：先 `python --version` 确认命令存在，失败就试 `python3`
或平台托管解释器的绝对路径。）

**交付不是「回一句已生成」**：把 `draft.pdf` 与 `draft.docx` 用文件预览打开给用户看，
附三句（页数与达成率 / 阻塞项条数 / 还需要用户做什么），交付清单写进 `review.md` 末尾。

## 五、编辑质量与定位（不许做成信息堆叠）

**开工先定本期编辑方针四问**（写进 `issue-brief.md` 顶部）：① 谁看（具体到岗位与处境）
② 看完做什么（具体到动作）③ 记住什么（本期只留一句是哪句）④ 为什么是我们说。

四问的答案必须落成 **`positioning.json`**（模板 `assets/templates/positioning.template.json`）——
与 `stylespec.json` 平级的第二份机器可读产物：`stylespec` 管长什么样，`positioning` 管
写给谁、为什么写、用什么调子说。**调性是前三项的结果，不是起点**：先定目的与读者，再推调子。
字段：目的（六选一，只能一个）/ 读者（岗位＋处境＋专业水平＋时间预算）/ 价值承诺＋reader_action /
调性三刻度（直接换算单条字数带与句长上限）/ 行业术语与忌讳。

内容分四级，**纯 L0 的条目整期不超过一半**：L0 事实 / L1 影响（必须点名受影响的主体与环节）/
L2 判断（换成别人写会写得不一样）/ L3 行动（能落成动作＋时点）。

两道效果门禁，交付前必跑（脚本已随本技能自带）：

- `audit_layout.py` 管**好不好看**：正文字号是否与样刊一致、字号层级有没有碎裂、行距倍数、
  每行字数、中文空格残留、页面密度。前面几道门禁**都不管这些**。
- `audit_editorial.py` 管**对不对路**：定位卡完整度 / 单条字数是否落在调性派生的字带 /
  兑现「读者要做什么」的条目覆盖率（<50% FAIL）/ 纯 L0 占比（>50% FAIL）/ 句长 / 术语与忌讳词。
  缺 `positioning.json` 时它明确 FAIL，不假装检查过（`--no-positioning-gate` 才能跳过）。

FAIL 必须修；WARN 逐条看一眼再交付。

## 五之二、溯源（每条动态都得有去处）

「阅读原文」不能只是一行字：`cta` 写成 `{"text","href","source","date"}`，
`href` 在 HTML 落成 `<a href>`、在 PDF 落成可点链接；`--cta-domain` 可把域名印上纸刊。
`build_draft.py --stats` 会报溯源覆盖率并点名缺链接的条目。
URL 只取官方原文，**检索不到就留空交业务方回填，不许编造**。

## 六、还没填的坑

派生时以下几项**没有真值**，首次开工前必须补齐，否则会带着错误一路走到定稿：

- **免责声明没抽到**（样例中可能为图片）：见 `assets/fixed-pieces.md` 第三节，必须人工补录
- **联系方式名录没抽到**：填写 `assets/fixed-pieces.md` 第四节
- **UnitPattern 是机器草稿**：`assets/unit-patterns.md` 由样例统计倒推，投产前须人工复核并用真实例句替换
- **术语表为空**：`assets/glossary.md` 需手工建立，至少覆盖高频法规名与机构名
- **数据源清单未填**：`sources.template.md` 填完后改名为 `sources.md`
- **Runbook 未填**：首期跑完后把真实额度与踩坑写进 `runbook.template.md`

补齐后请同步删掉本节的对应条目——它是对自己的待办清单，不是给别人看的说明。
