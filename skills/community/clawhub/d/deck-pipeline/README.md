# Deck Pipeline · CN→EN · McKinsey Polish · Layout Audit

![version](https://img.shields.io/badge/version-0.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![status](https://img.shields.io/badge/status-beta-orange)

> A production-grade Claude Code system for taking decks from raw Chinese draft to McKinsey-polished English — with full audit trail, layout integrity checks, and a swappable PROFILE block for project-specific defaults. Built on a 4-stage pipeline; also runs polish-only on any single-language deck.
>
> 一套生产级 Claude Code 系统，把 deck 从中文原稿做到麦肯锡级英文成稿——全程留痕、排版守护、可替换的项目级 PROFILE 块。基于 4 阶段流水线；也支持纯排版模式，处理任意单语言 deck。

---

## What it does / 做什么

Takes a Chinese deck (and optionally an English draft) and runs it through a 4-stage pipeline. Or, if you give it a single-language deck and ask for layout-only cleanup, skips translation and runs polish stages alone.

Works for any kind of deck — sales, product, research, conference talks, internal reports, whatever.

输入一份中文 deck（可选搭配一版英文草稿），经过 4 阶段流水线。或者，给它一份单语言 deck + 要求"只做排版"，就跳过翻译，只跑排版相关 stage。

| Stage / 阶段 | What happens / 做什么 | Polish-only? |
|---|---|---|
| **1. Sense Pass** | Reverse-engineer design DNA (palette, fonts, size hierarchy) and surface candidate glossary terms.<br>反推设计 DNA（色板、字体、字号梯队），扒出候选术语。 | ✅ runs |
| **2. McKinsey Translation** | CN → EN in McKinsey style from the first pass (top-down, parallel, strong verbs, no filler). Glossary applied inline; unclear terms asked on the spot. Runs **page-by-page** with a checkpoint after each slide.<br>中翻英直接出麦肯锡风格（top-down、平行结构、强动词、去填充词）。术语表 inline 应用；生僻词当场问。**逐页执行**，每页结束 checkpoint 等用户确认。 | ⏭️ skipped |
| **3. Layout Audit** | Font pollution cleanup, overflow estimation, structural-anchor protection, reverse-sync from hand-edits.<br>字体污染清理、溢出估算、结构锚点保护、手动改动反向同步。 | ✅ runs |
| **4. Handoff** | Three or four deliverables + a HANDOFF.md contract for the next session.<br>3–4 件交付物 + 给下一个 session 的 HANDOFF.md 接力契约。 | ✅ runs |

You do **not** need any external skill installed. The generic deck-globalization engine (3-phase visual audit / semantic alignment / page-by-page execution) is bundled inside.

**不需要**安装任何外部 skill。通用 deck 全球化引擎（3 阶段：视觉审计 / 语义对齐 / 逐页执行）已内置。

---

## Install / 安装

```bash
git clone https://github.com/<your-org>/deck-pipeline ~/.claude/skills/deck-pipeline
pip3 install python-pptx openpyxl pymupdf pyyaml
```

The skill is loaded automatically by Claude Code on next start.

下次 Claude Code 启动时会自动加载本 skill。

---

## Modes / 模式

| Mode / 模式 | Trigger / 触发 | Stages run / 跑哪些 stage |
|---|---|---|
| **Full pipeline / 完整流水线** | CN deck (± EN draft) provided, translation requested<br>提供 CN deck（± EN 草稿），要翻译 | 1 → 2 → 3 → 4 |
| **Polish-only / 纯排版** | Single-language deck, "just polish / format only / skip translation"<br>单语言 deck，说"只做排版 / 跳过翻译 / format only" | 1 → 3 → 4 |
| **Reverse-sync only / 反向同步** | User hand-edited PPT after Excel was generated<br>用户在 Excel 生成后手动改了 PPT | 3.5 sub-routine |

---

## Outputs / 输出

**Full pipeline / 完整流水线**（4 件）：

| File / 文件 | Content / 内容 |
|---|---|
| `xxx-en-polished-[date].pptx` | English deck after McKinsey-style translation + glossary lock.<br>麦肯锡风格翻译 + 术语锁定后的英文 deck。 |
| `xxx-final-[date].pptx` | Above + font/layout normalization, overflow fixes.<br>在前者基础上做完字体/布局规范化、溢出修复。 |
| `xxx-bilingual-diff-[date].xlsx` | Row-by-row comparison: `page / kind / cn / en_original / en_optimized / notes`. Red-bold rows = key corrections.<br>逐行对照表，红粗 = 关键修正。 |
| `HANDOFF.md` | Session contract: goal · tools · completed · unresolved · cautions · principles · constraints.<br>session 契约。 |

**Polish-only / 纯排版**（3 件）：

| File / 文件 | Content / 内容 |
|---|---|
| `xxx-final-[date].pptx` | After font/layout normalization, overflow fixes.<br>字体/布局规范化、溢出修复后。 |
| `xxx-layout-changes-[date].xlsx` | What was changed.<br>改了什么。 |
| `HANDOFF.md` | Same as above.<br>同上。 |

---

## Architecture / 架构

Three layers, in order of stability / 三层，按稳定性排序：

### L1 Tokens（stable, project-defined / 稳定，项目级定义）
- **Palette / 色板** — ink, primary brand, soft fill, page background
- **Font whitelist / 字体白名单** — title face (e.g. serif) + body face (e.g. sans-serif)
- **Unit conversion / 单位换算** — 百万=M · 亿=100M · 十亿=1B · 百亿=10B · 千亿=100B · 万亿=1T
- **Glossary / 术语表**（见下）

### L2 Constants（operational defaults / 操作默认值）
- **Size ladder / 字号梯队** — 22 / 14 / 10 / 8 / 6 / 4 pt
- **Floors / 地板** — body ≥ 7pt · caption ≥ 6pt · source ≥ 4pt
- **Compression step / 压缩步进** — `-0.1pt` discrete only / 仅 -0.1pt 离散迭代，不一刀切
- **Line-spacing fallback / 行距备选档** — 1.25 → 1.15 before sub-floor compression
- **Quote style / 引号风格** — McKinsey single quotes `'…'`
- **Footer format / 页脚格式** — `Confidential · For Intended Recipients Only · {month} {year}` (middle dot, not em-dash)

### L3 Sensed（run-time, per-deck / 运行时，按 deck 推算）
- **Font-name suffix audit / 字体名后缀审计** — `font.name` must not contain `Bold` / `Regular` / `Italic` / `Light` suffixes; split into `name` + boolean attribute
- **Structural-anchor detection / 结构锚点检测** — shapes consistent across ≥3 pages (footers, callout bands, watermarks) → per-page protection list
- **Late-stage glossary re-scan / 末段术语复扫** — catches hand-edit regressions
- **Glossary wavering detection / 术语摇摆检测** — same source term getting multiple translations across the deck

---

## Style baseline + extensible references / 风格基线 + 可扩展引用

**McKinsey is the default baseline.** Title-as-takeaway, lead-with-so-what, parallel structure, strong action verbs, filler removal, sentence-case by default.

**麦肯锡是默认基线**：标题即结论、so-what 前置、平行结构、强动词、去填充词、默认小写。

**On top of McKinsey, you can upload additional reference samples** — any PDF or .pptx whose writing style you want to emulate (a colleague's well-written report, an industry whitepaper, your own prior work, etc.). The skill distills each via `scripts/style_distill.py` and layers its rules on top of the McKinsey base.

**在麦肯锡之上，可以上传其他参考样本**——任何你想模仿其文风的 PDF 或 pptx（同事写得好的报告、行业白皮书、自己之前的作品等）。skill 用 `scripts/style_distill.py` 抽每份样本的风格指纹，在麦肯锡基线之上叠加。

Distillation extracts / 蒸馏出来的内容：
- Cadence: avg sentence/paragraph length, p90 length / 节奏：句长、段长、p90
- Vocab: signature phrases, top action verbs, filler-word patterns / 词汇：标志短语、高频动词、填充词模式
- Structure: bullet pattern, parallel-structure score / 结构：bullet 模式、平行度
- Tone: first-person ratio, hedge ratio, certainty ratio / 调性：第一人称比例、保守语 / 笃定语比例

Add references in PROFILE / 在 PROFILE 加 references：

```yaml
style_references:
  - path: "/path/to/sample.pdf"
    weight: 0.7   # 0.0–1.0; how strongly to bias toward this sample
```

Conflicts between references → most recent entry wins; user asked at first conflict.

References 冲突 → 最新一条优先；首次冲突时问用户。

---

## Page-by-page execution / 逐页执行

Stage 2 is **not** all-at-once. After overall confirmation, the skill iterates slides 1 → N. For each slide:

Stage 2 **不是**一次性全跑。整体确认后逐页跑：

1. Apply edits to that slide's paragraphs / 应用该页的 edits
2. Append rows to the Excel immediately / 立刻把该页的对照行追加到 Excel
3. Print "P{n} done — N changes applied. Continue?" / 打印 "P{n} 完成，N 处改动，继续？"
4. Wait for user confirmation before moving to P{n+1} / 等用户确认再进下一页

You can interject "back to P{n-1}", "stop here", or "redo P{n}" between pages.

页间可以说"回到 P{n-1}"、"停在这里"、"P{n} 重做"。

Why / 为什么：
- Mid-stream review and steering / 中途可审查、可调整
- Bad assumptions don't propagate silently / 错误假设不会静默扩散
- Excel grows incrementally → survives interruption / Excel 增量增长，中断也能续上
- Token-efficient: only current slide in active scratchpad / 省 token：当前页才在活跃上下文

---

## Glossary categories / 术语表分类（extensible / 可扩展）

```
Locked            → user-confirmed, never re-asked / 用户确认过，不再问
Pending           → asked but not yet confirmed / 问过但未拍板，跨 session 接力
Rejected rewrites → user vetoed; never propose again / 被驳回过，永久回避
Session-added     → added mid-session; promoted to Locked at handoff / 本次新加，handoff 时升 Locked
Per-row override  → "ignore glossary for this row" / 单行豁免
```

Replace the example entries in `SKILL.md` `PROFILE.glossary.locked` with your project's terms (proper nouns, brand names, product names, industry phrases, etc.).

把 `SKILL.md` 中 `PROFILE.glossary.locked` 的示例条目替换成你项目的术语（专有名词、品牌名、产品名、行业说法等）。

---

## Magnitude trap / 量级陷阱

The Chinese 亿 is **100 million**, NOT "billion". / 中文「亿」= 1 亿 = 100M，**不是** "billion"。

| CN | EN |
|---|---|
| 一百万 / 百万 | 1 million |
| 一千万 / 千万 | 10 million |
| 一亿 / 1亿 | 100 million |
| 十亿 | 1 billion |
| 百亿 | 10 billion |
| 千亿 | 100 billion |
| 万亿 | 1 trillion |

Append your currency suffix (`$`, `RMB`, `€`, etc.) in PROFILE per project.

---

## Interaction model / 交互模型

The skill is **bidirectional** — it stops and asks at specific checkpoints rather than guessing.

本 skill **双向交互**——在特定检查点停下来问，不瞎猜。

You will be asked when / 以下情况会问你：

1. A source term has no glossary entry and Claude is unsure<br>遇到未收录术语且拿不准
2. A McKinsey rewrite candidate looks ambiguous (only when unsure — not every line)<br>麦肯锡改写候选有歧义（仅在拿不准时问，不是每行都问）
3. A shape's font hits the floor and overflow remains<br>某 shape 字号撞地板但仍溢出
4. A companion file (`.pptx` / `.xlsx`) is open in another app (lock file present)<br>配套文件被其他 app 打开（lock 文件存在）
5. The overflow estimator reports > 10 HIGH-risk shapes (defer to user-side rendering)<br>估算器报 > 10 个 HIGH 风险 shape（让用户外部渲染复核）

You will **not** be asked twice for the same thing in one session — once confirmed, it enters Locked.

同一件事**不会问两次**——确认过的进 Locked。

---

## Operational rules / 操作规则

### File-write discipline / 文件写入纪律
- Overwrite the original by default / 默认覆盖原文件
- Scan for `~$xxx` lock file before writing / 写前扫 `~$xxx` lock 文件
- If lock exists → **stop and ask user to save + close first** / 存在 → **停 + 让用户先保存并关闭**

### Excel companion guard-rails / Excel 配套文件三护栏
1. **Pre-write check / 写前校验** — verify header has all 6 columns / 校验 header 6 列齐全
2. **Post-write readback / 写后回读** — immediately reload and confirm columns survived / 立即重读，确认列数没丢
3. **Reverse sync / 反向同步** — bidirectional diff (ordinal first, fuzzy fallback) updates Excel from a hand-edited PPT / 双向 diff（先 ordinal，再 fuzzy 兜底），把 PPT 的修改同步回 Excel

### Font compression discipline / 压字号纪律
- Detect per-page protection list (structural anchors + user-specified) / 先取 per-page 保护列表（结构锚点 + 用户指定）
- Iterate `-0.1pt` until no overflow / 按 -0.1pt 迭代到无溢出
- If floor is hit / 撞地板：
  1. Geometric widening (eat margin) / 横向扩框（吃 margin）
  2. Line-spacing 1.25 → 1.15 / 行距压缩
  3. Still overflowing → **escalate to user** / 仍溢出 → **上报用户**，列出问题 shape

### CN-alignment configuration / CN 对齐配置
Configure `PROFILE.cn_en_slide_offset` (or pass `--cn-offset <yaml>` to `excel_sync.py`) for decks where CN and EN have been restructured.

如果 CN/EN 两版有结构性差异，配置 `PROFILE.cn_en_slide_offset`（或给 `excel_sync.py` 传 `--cn-offset <yaml>`）。

Default is 1:1 alignment.

默认 1:1 对齐。

---

## Overflow estimator / 溢出估算器

Static analyzer flagging shapes whose text likely overflows. Three severity bands:

静态分析，三档严重度：

- **HIGH** — `ratio > 1.5`（very likely real / 极可能为真）
- **MED** — `ratio 1.15 – 1.5`（might be real / 可能为真）
- **LOW** — `ratio 1.0 – 1.15`（probably fine / 大概率没事）

Only HIGH is surfaced by default. / 默认只报 HIGH。

### Accuracy details
- Honors `auto_size`（NONE / SHAPE_TO_FIT_TEXT / TEXT_TO_FIT_SHAPE）
- Reads actual margins (no defaults)
- Line-height multiplier `1.15`
- Per-character width by class (narrow / wide / digit / upper / space)
- Greedy word-wrap simulation

### When the estimator is still wrong / 估算器仍可能错

Static analysis cannot render. If > 10 HIGH-risk shapes are reported:

静态分析不能渲染。HIGH > 10 个时：

> "Render the deck to PDF or PNGs externally (Keynote `File → Export`, or PowerPoint `Save as PDF`) and tell me which page numbers look problematic. I'll fix those targeted pages."
>
> 「请用 Keynote 导出或 PPT 另存 PDF，告诉我哪几页有问题，我针对性修。」

By design — dumping 30+ rendered pages into a single session causes context overload.

这是刻意设计——把 30+ 渲染页一次性灌进 session 会过载。

---

## Known limitations / 已知限制

1. Overflow estimator is a **hint, not a verdict** — final visual check requires external rendering.<br>溢出估算器是 hint 不是判决，最终视觉确认需外部渲染。
2. `python-pptx` cannot render slides.<br>`python-pptx` 不能渲染。
3. CN auto-alignment can drift on heavily restructured pages — configure overrides for known cases.<br>CN 自动对齐对重排页可能漂移，已知情况配 overrides。
4. The skill assumes the CN source is semantic ground truth — typos in CN propagate.<br>把 CN 当语义基线，CN 自带的错也会传过去。
5. File-lock collisions silently corrupt output. Always close before letting the skill write.<br>文件锁冲突会静默破坏输出，让 skill 写之前一定要关。

---

## License / 许可

MIT. See `LICENSE`. / MIT 协议，见 `LICENSE`。

## Contributing / 贡献

See `CONTRIBUTING.md`. / 见 `CONTRIBUTING.md`。

## Credits / 致谢

Generic deck-globalization engine derived from upstream **DeckGlobalizer v2.1.1** by tinadu-ai (<https://clawhub.ai/tinadu-ai/deckglobalizer>). Original three-phase architecture (Visual Audit / Semantic Alignment / Page-by-Page Execution) credited and retained.

通用 deck 全球化引擎来自上游 **DeckGlobalizer v2.1.1**（作者 tinadu-ai，<https://clawhub.ai/tinadu-ai/deckglobalizer>）。原三阶段架构（视觉审计 / 语义对齐 / 逐页执行）credit 保留。
