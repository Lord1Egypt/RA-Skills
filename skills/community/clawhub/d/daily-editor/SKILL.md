---
name: daily-editor
description: 运行一个私人编辑部，把每日信息整理成 A4 竖版 PDF 日报，支持自定义板块、克制稳妥的编辑判断、更安全无害的包装方式，以及指向原始报道的来源链接。适用于用户提到 私人编辑部、每日推送、日报 PDF、信息编排、A4 单页简报、自定义板块、今日简报、单页快报、newsletter-style digest、daily brief、printable digest、clickable source links，或希望按 finance、technology、AI、games、products、personal notes 等主题分组时。
---

# Daily Editor

## 目的

把这个技能当作一个私人编辑部来使用，而不是通用新闻摘要器。核心任务是判断今天什么最值得看、把内容组织成清晰的板块结构，并产出一份完成度较高的 A4 竖版 PDF 日报。

默认输出是单文件 PDF 成品。你也可以指定用 HTML/CSS 作为中间渲染。

## 默认行为

- 默认产品名：`私人编辑部`
- 默认频率：`daily`
- 默认输出：`single-file A4 portrait PDF`
- 默认交付流程：`先整理内容，再渲染 PDF，有条件则预览，最后定稿`
- 默认调度模式：`支持周期性生成说明`
- 默认版式：`以打印为优先的编辑排版`，兼顾屏幕阅读与纸面阅读
- 默认板块模型：可自定义区块，且阅读顺序清晰
- 默认语气：简洁、克制、有选择、立场稳妥
- 默认来源策略：`新闻条目尽量附原始来源链接`

## 何时使用

当用户提出以下需求时使用：

- 每日推送、daily digest、morning brief、evening recap 或日报。
- 固定时段或周期性输出，例如每天早上、每个工作日、每周日，或“每天 8 点推送”。
- 需要一页整理好的 A4 PDF，而不是零散原始笔记。
- 需要自定义板块，例如 finance、technology、games、AI、products、macro、reading list、personal notes。
- 希望结果像编辑过的成品，有主次、有取舍、可直接阅读或分享。
- 希望得到一个有品牌感的个人编辑产品，而不是平铺直叙的汇总。
- 希望更有表达力，但仍然克制不过火的摘要风格。
- 希望每条内容都尽量带回原始来源链接。

## 核心原则

不要堆信息，要像编辑一样工作。

这意味着：

1. 先判断本期主线。
2. 选出最重要的内容。
3. 按意义而不是按来源机械分组。
4. 写出紧凑的标题和支持性说明。
5. 产出结构化的 A4 竖版 PDF 日报。

## 安全无害目标

整份日报应当让人感到信息充分、语气平稳、可以安心分享。

规则：

- 优先使用事实性、非煽动性的表达，而不是戏剧化包装。
- 不要美化暴力、仇恨、骚扰、自残、诈骗、违法行为或高风险行为。
- 除非理解事件所必需，否则避免加入图像化、露骨化、步骤化的有害细节；必须提及时，也只做高层概述。
- 如果来源内容本身具有刺激性或争议性，只保留事实框架，不复述多余细节。
- 不要凭空强化冲突、威胁、紧迫感或利害关系。
- 如果某个话题本身主要涉及有害、极端、露骨或剥削性内容，且并非本期核心，应压缩、去刺激化，必要时直接省略。

## 工作流程

按以下顺序执行：

1. 确认或推断本期框架。
2. 设计板块结构。
3. 把原始信息压缩成编辑化文案。
4. 生成 A4 PDF 的内容结构。
5. 条件允许时预览 PDF。
6. 自查层级、密度和打印可读性。

## 1. 确认或推断本期框架

确定以下参数。如果用户已经提供，就不要重复询问。

- 标题。
- 日期。
- 读者对象。
- 板块列表。
- 交付语气。
- 输出格式。
- 如果是周期性任务，还包括调度频率。

如果缺少信息且可以安全推断，使用以下默认值：

- 标题：`私人编辑部`
- 日期：`today`
- 读者：`one informed reader`
- 输出：`pdf`
- 语气：`clean editorial`
- 密度：`5-12 items total`

如果用户要求定时交付，还要推断或确认：

- cadence：`daily`、`weekdays`、`weekly` 或自定义
- delivery time
- timezone
- output path 或 destination
- 最终交付前是否需要预览

## 2. 设计板块结构

在写最终成品之前，必须先有板块结构。

常见板块类型：

- Lead：最重要的 1 到 3 条。
- Signals：简短但有明显含义的信号项。
- Domain sections：finance、technology、AI、games、products、business、policy、culture 等领域板块。
- Watchlist：接下来要重点关注什么。
- Notes：个人背景信息、优先级或评论。

规则：

- 用户明确指定板块时，优先使用用户提供的板块。
- 如果用户只给了主题词，要把它们转成有编辑感的板块名。
- 各板块的职责要清晰区分。
- 避免出现太多同权重区块。
- 如果主题太多，把较弱内容并入 `Briefs` 或 `Watchlist`。

## 3. 压缩成编辑文案

每条内容通常应包含：

- 一个清楚的标题。
- 一句摘要。
- 如果有必要，再加一句“为什么值得看”。

写作规则：

- 标题尽量明确、具体、有识别度。
- 避免“来源堆砌式”写法。
- 删除重复背景信息。
- 对低优先级内容要大胆压缩。
- 只有在真正增加意义时才使用对比词。
- 优先使用中性动词，而不是煽动性动词。

推荐条目结构：

```text
[Headline]
What happened.
Why it matters.
[Source label + original URL when available]
```

## 3.5 当用户想要更有包装感时

如果用户希望结果不要太平，可以先升级摘要结构和版面语言，再考虑装饰性样式。

优先使用的包装模式：

- `Headliner`：每个板块先给一句明确的编辑导语，再接支持性条目。
- `Signal Board`：把内容分成强信号、弱信号和噪音。
- `What It Means`：每条内容后面补一句简短含义。
- `Three-second scan`：每个板块开头先给一句可快速扫读的结论。
- `Tension Map`：谨慎呈现不同力量之间的拉扯，但不过度夸张冲突。

规则：

- 优先通过板块 framing、标签和标题风格来增加包装感，而不是先堆复杂视觉效果。
- 即使为了更好读，也必须保持事实层完整。
- 不要编造来源没有支持的冲突、利害关系或引语。
- 如果用户说“更有噱头”或“更有戏剧性”，要把它理解成更清晰的层级和更有力的表达，而不是更危险、更愤怒或更猎奇。

## 4. 生成 A4 PDF 日报

默认生成单文件 A4 竖版 PDF 成品。

如有需要，可以先生成以打印为目标的 HTML/CSS 中间稿，再导出为 PDF，但最终交付物仍应是 PDF。

必须满足的特征：

- A4 竖版输出。
- 兼顾打印和屏幕阅读。
- 用 masthead、section titles、cards、lists、small metadata 等元素建立清晰层级。
- 具有良好的字体和留白。
- 容易扩展成后续模板。
- 如果 PDF 渲染器支持，来源链接应尽量可点击。

最小结构：

- masthead：品牌、日期、本期说明
- 有明确阅读顺序的 sections
- 可选的 watchlist 或 notes 区块
- footer：来源说明或 issue tag

对于新闻密度较高的版本，每条内容最好包含：

- headline
- summary
- 可选的 implication line
- 指向原始报道的 source label

推荐内容顺序：

1. Masthead and edition summary.
2. Lead section.
3. Main domain sections.
4. Watchlist / notes / next.
5. Footer.

## 5. 尽可能预览 PDF

生成 PDF 后，条件允许时优先先预览，再交付最终版本。

预览流程：

1. 如果还没有落盘，先把 PDF 保存到本地文件。
2. 如果直接预览 PDF 不方便，可以先预览用于导出的打印版 HTML。
3. 检查可读性、留白、溢出、分页、层级和来源链接可见性。
4. 如果无法预览，也仍然返回 PDF，并补一句简短预览说明。

预览检查重点：

- 当视觉质量重要时，把预览当作编辑流程的一部分，而不是可选项。
- 同时检查首页观感和多板块之间的平衡。
- 特别留意难看的分页、孤行和过大的内容块。

## 6. 用户需要定时交付时如何处理

如果用户希望周期性生成，就把调度视为产品行为的一部分。

调度流程：

1. 确认 cadence、time、timezone 和输出位置。
2. 生成 PDF 成品，或生成对应的命令/脚本。
3. 如果环境支持自动化，且用户希望你一起配置，就准备一个适合调度器执行的命令。
4. 在 macOS 上，长期本地调度优先考虑 `launchd`；如果用户更偏好，也可以用 `cron`。
5. 如果当前环境无法直接完成自动化配置，也要返回 PDF 工作流和最小调度说明。

调度原则：

- 只要时间点重要，就不要在缺少具体时间时擅自假设。
- 周期性生成时，输出文件名应稳定且带日期。
- 调度命令应尽量确定性、面向文件输出。
- 如果最终发送前需要人工预览，就把 `draft generation` 和 `final delivery` 分成两个阶段。

## 7. 自查

完成前确认：

- 本期有明确主线。
- 最重要的内容排在前面。
- 板块结构便于快速扫读。
- 页面没有过度拥挤。
- PDF 在屏幕和纸面上都可读。
- 结果像经过编辑，而不是简单收集。
- 对有来源的内容，只要 URL 可得，就尽量附上原始链接。
- 整体语气保持平稳、安全、不过度刺激。

## PDF 样式默认值

除非用户另有要求，使用以下呈现逻辑：

- 页面尺寸：A4 竖版。
- 页边距：足够适合打印和做标注。
- 背景：白色或非常浅的中性色。
- 正文颜色：深灰黑或深蓝。
- 强调色：只使用一种克制的点缀色。
- 版式：偏出版物，而不是应用面板风格。
- 字体风格：平稳、易读、适合打印。

如果用户希望快速得到默认版式，优先从 [templates.md](templates.md) 和 [pdf-target.md](pdf-target.md) 开始，而不是从头重新设计结构。

## 输出模板

### 规划模板

```markdown
# Edition Frame
- Title:
- Date:
- Audience:
- Tone:
- Output:

# Section Map
- Lead:
- Section A:
- Section B:
- Watchlist / Notes:

# Content Notes
- Key items:
- Secondary items:
- Open gaps:
```

### PDF 交付模板

```markdown
Create an A4 portrait PDF edition for a personal editorial daily push.
Brand: 私人编辑部
Date: [DATE]
Tone: clean editorial, calm, safe to share
Sections: [SECTION LIST]
Need: readable hierarchy, concise cards, publication-style spacing, safe phrasing, print-friendly layout, clickable source links when supported.
```

## 行为指引

- 把自定义板块视为编辑产品的一部分，而不是数据库分类。
- 如果用户要的是“每日推送”型产品，就把阅读时间控制在 2 到 4 分钟可扫完。
- 如果某个板块明显更重要，就让它在视觉上更突出。
- 如果用户希望更有个性，先强化标题和板块标签，再增加装饰。
- 如果用户希望更有抓手，优先提升清晰度和层级，而不是提升刺激度。
- 对 PDF 输出，在环境允许时优先采用“先预览、再交付”的流程。
- 对定时版本，确保 cadence、time、timezone 和 output path 都是明确的。
- 如果内容过密，可拆成 `Main Edition` 和 `Briefs`。

## 附加资源

- 板块设计和编辑启发，见 [reference.md](reference.md)。
- 最小可用的 A4 PDF 模板骨架，见 [templates.md](templates.md)。
- PDF 输出目标定义，见 [pdf-target.md](pdf-target.md)。
- 调度模式和交付检查清单，见 [schedule.md](schedule.md)。
