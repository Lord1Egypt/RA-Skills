---
name: cjl-slides
description: |
  Create stunning HTML presentations in 24 international design styles with strict design rules.
  Export to .pptx for PowerPoint editing.

  ## Design Philosophy
  - Aesthetic-first: each style is a curated visual system, not just colors
  - Font whitelist enforcement: prevents AI-generic typography
  - Container ratio lock (16:9): ensures consistent rendering across devices
  - Zero external dependencies: pure HTML/CSS/JS, works offline

  ## Usage
  1. Activate → Select style by name/number or browse 24 options
  2. Provide content (topic, audience, key points) or upload .pptx for conversion
  3. Review generated HTML slides → request modifications (color/font/layout)
  4. Optionally export .pptx for manual editing in PowerPoint

  ## Precautions
  - Fonts are restricted to a whitelist; custom fonts require adding to the allowed list first
  - Chart.js CDN is used; if blocked, falls back to jsdelivr mirror
  - HTML files must retain their relative structure when shared
  - .pptx export preserves exact colors and fonts but layout uses pptx-native elements

  ## Credits
  Design rules adapted from "专精 HTML 演示文稿的顶级视觉设计师" (24 design styles reference).
  Base HTML structure and tooling inspired by zarazhangrui/frontend-slides.
allowed-tools:
  - Write
  - Read
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
  - WebFetch
origin: https://github.com/0xcjl/cjl-slides | 基于 zarazhangrui/frontend-slides，融合专精 HTML 演示文稿的顶级视觉设计师
---

# HTML Slides

零依赖、纯 HTML 单文件演示文稿，支持 24 种国际设计风格，可转换为 .pptx 格式。

## When to Activate

- 用户请求创建演示文稿/幻灯片/slides/deck
- 用户说"帮我做个 PPT"、"生成演示文稿"、"做一个 pitch deck"
- 用户提供了内容，需要生成视觉精美的 HTML 页面
- 用户提到具体风格名称（Linear、Pitch、Swiss、Cyberpunk 等）

---

## 工作模式

### 模式 A：从零创建

### 模式 B：PPTX 转换

将用户提供的 `.pptx` 文件转换为 HTML slides。

---

## 模式 A 完整流程

### 第一步：问候与风格确认

**问候语：**

> 你好！我可以为你创建精美的 HTML 演示文稿，支持 24 种国际设计风格。
> 请从以下分组中选择你喜欢的风格（可回复编号、名称或 all）。
> 完整风格说明和视觉预览见 STYLE_PREVIEWS.md。

**按场景分组展示（每组不超过 6 种）：**

```
【商业/融资】
1.  Pitch.com — 商务优雅，大量留白与渐变。
2.  Bloomberg Businessweek — 新闻编辑实验风，色块切割，标题极端放大。
3.  Startup VC Pitch — 硅谷路演风，超大指标数字，极度克制信息密度。

【产品/科技】
4.  Linear App — 极简暗色调，精密工程感。
5.  Vercel / Developer Dark — 纯黑开发者极简，精密网格，冷白代码感。
6.  NASA / Scientific — 航天技术文档，海军蓝底，数据可视化优先。
7.  Glassmorphism UI — 磨砂玻璃卡片，渐变光感底层，iOS/visionOS 质感。

【创意/设计】
8.  Framer — 动态感布局，大胆渐变配色。
9.  Figma Community — 活泼彩色，设计师圈子美学。
10. Duotone Editorial — 摄影双色调，Spotify 式媒体感，混合模式叠色。
11. Cyberpunk Neon — 赛博霓虹，纯黑底青粉撞色，发光线条失真感。

【文化/艺术】
12. Swiss Typography — 国际主义，纯排版驱动。
13. Are.na Archive — 文化档案感，颗粒质感纹理。
14. Wabi-Sabi Organic — 侘寂工艺感，陶土色有机形状，刻意不完美。
15. Chinese Ink / 国风 — 水墨笔触，宣纸白配朱红金，东方留白哲学。

【品牌/奢侈】
16. Teenage Engineering — 工业产品手册感，橙色点缀，等宽技术排版。
17. Muji / Japanese Ma — 日式「間」美学，负空间即设计，极度克制。
18. Luxury Fashion House — 高奢品牌语言，超宽字间距，冷峻衬线极简。

【学术/政务】
19. Stripe Press — 编辑排版风，高对比度黑白。
20. Apple Keynote Dark — 深空黑底，产品发布质感。
21. Academic Scholarly — 学术会议风，象牙底多栏密排，严肃衬线体。

【娱乐/复古】
22. Memphis Revival — 80 年代后现代复兴，几何图案，高饱和波普撞色。
23. Brutalist Web — 反设计运动，裸露结构，粗边框刻意未完成感。
24. Y2K Retro Digital — 千禧数字怀旧，铬金属渐变，CRT 扫描线噪点感。
```

**用户响应：** 回复编号（`1,4`）、名称（`Pitch, Cyberpunk`）或 `all`。确认后直接进入内容收集。

- 用户描述风格但不指定名称 → 根据描述推荐最接近的风格编号
- 用户回复 `all` → 告知共24种风格，每次最多生成2种，确认批次顺序后开始
- 若用户未指定风格 → 先询问演示用途，按用途推荐最接近的3种风格供选择

---

### 第二步：内容收集

确认风格后，询问：

- 演示用途是什么？
- 有没有现成内容（文字/大纲/文档），还是需要 AI 帮助撰写？
- 需要几页？（默认 5 页标准结构）

**用户无现成内容**：主动询问主题、目标受众、核心卖点，基于信息撰写内容大纲，用户确认后再生成。

**默认 5 页标准结构（用户未指定时）：**
1. 封面 — 标题 + 副标题 + 作者
2. 文字页 — 标题 + 3 段正文
3. 图文分栏 — 图片占位区使用该风格标志性配色
4. 数据页 — 柱状图 + 折线图并排（Chart.js）
5. 结语页 — 一句大型陈述句配视觉锚点

**扩展页面类型参考：** 议程页、引言金句页、团队介绍页、时间轴页、对比页、致谢/问答页。

每批最多输出 2 种风格。

---

### 第三步：生成 HTML

**交付物：** 单个 `.html` 文件（无外部依赖，内联 CSS/JS）。文件命名：`<主题>-<风格名>.html`，例如 `ai-education-Pitch.html`

**生成后自检：** 每张幻灯片有视觉锚点、正文字号≥1.4vw、无居中对齐（封面除外）、CSS变量已定义、Chart.js图例为自定义。

**动画效果：** 可参考 animation-patterns.md，使用 CSS animation 或 transition，不依赖外部库。

**必须遵循的规则：**

#### 字体规则（白名单）

**展示字体（h1/h2）二选一：**
- 衬线组：Playfair Display、Fraunces、DM Serif Display、Cormorant Garamond
- 无衬线组：Syne、Bebas Neue

**正文字体（四选一，均为无衬线）：** DM Sans、Outfit、Figtree、Epilogue

**中文叠加：** 衬线展示字体 → Noto Serif SC；无衬线 → Noto Sans SC

> 禁止使用白名单外任何字体（Inter、Roboto、Arial、Space Grotesk、Plus Jakarta Sans 等一律禁止）

#### 配色规则

每种风格取 3 色，用 CSS 变量管理：
```css
--color-primary: #xxx;
--color-secondary: #xxx;
--color-accent: #xxx;
```

#### 容器比例规则

```css
.slide {
  width: min(100vw, 177.78vh);
  height: min(56.25vw, 100vh);
  overflow: hidden;
}
```

禁止单独使用 `100vw / 56.25vw` 替代以上写法。

#### 美学规则

- 每张幻灯片必须有一个最抢眼的视觉锚点（超大数字、粗体关键词、大色块或图表）
- 标题至少是正文字号的 10 倍，不超过 30 倍
- 正文（p）字号在 `1.4vw` 至 `2.5vw` 之间，禁止被色块遮挡
- 正文必须在 flexbox 或 grid 正常文档流中排列（不得脱离文档流定位）。h1/h2 标题不受此限
- 同一文件内每张幻灯片使用不同布局
- 每张幻灯片视觉重心明显偏向一侧；封面页的标题居中不在此限
- 装饰性色块面积占幻灯片的 30% 以上
- 元素可出血超出幻灯片边缘（`overflow: hidden` 确保容器外内容被裁剪）
- 标题（h1/h2）允许且鼓励压在色块之上
- 创意排版仅用于纯装饰性元素（`opacity < 0.1` 的背景字）；h1/h2 禁止 `transform: rotate`
- 每张幻灯片内所有主要内容（标题+正文+图表）总高度不超过幻灯片容器的 90%

#### 图表规则

- 图表库：Chart.js（cdnjs CDN，优先使用 v4 稳定版）
  - CDN 失效时使用 jsdelivr 镜像：`https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
  - 若所有 CDN 均失效，在 HTML 注释中标注图表数据，提示用户手动插入
- **禁止使用 Chart.js 默认图例**，必须用自定义 HTML 图例替代
- 自定义图例：用 `<div>` + CSS 实现，不得使用 Chart.js 默认图例选项
- 图表外层容器必须同时满足：明确的 vw 高度 + `overflow: hidden` + `position: relative`
- canvas 元素必须用内联 style 设置高度（`style="height: 18vw; width: 100%"`），禁止用全局 CSS 或 Chart.js 默认设置
- 图表配色必须匹配该风格配色方案

#### 导航规则

- 仅支持键盘左右箭头切换幻灯片
- **禁止在幻灯片上显示任何导航按钮、箭头或提示文字**
- 触摸设备：支持左右滑动切换幻灯片（touch 事件）

#### 代码质量规则

所有引号、尖括号、符号保持原始字符；严禁 HTML 实体转义。每个 HTML 文件以 markdown 代码块标记 ` ```html ` 开头，第一行注释写 `<!-- 风格 N：[名称] -->`。代码块外不添加任何解释文字。

#### 内容约束

生成的幻灯片内容不得包含违法信息、虚假广告、侵犯版权的内容。

---

### 第四步：询问 PPTX 格式

HTML slides 输出完毕后，询问：

> 是否需要 .pptx 格式文件（便于在 PowerPoint 中调整）？

- **是**：用户确认需要 PPTX → 若用户未指定保存路径，使用 `<html文件名>.pptx` 作为默认路径
  → 运行 `python3 ~/.claude/skills/cjl-slides/scripts/html-to-pptx.py <html文件路径> <输出路径>`
  → 若 python-pptx 未安装，提示用户先运行：`pip3 install python-pptx`
  → 若文件保存失败（权限问题），提示用户指定其他保存路径
  → 告知保存位置（绝对路径）
- **否**：直接进入下一步
- 用户未明确回答时，默认为否

---

### 第五步：等待修改指令

每次最多输出 2 种风格。输出完毕后等待用户修改指令。

> 是否继续生成下一批，或需要对已生成的文件进行修改？

**支持以下修改指令（准确识别意图）：**

| 用户指令 | 响应动作 |
|---------|---------|
| "换配色" | 仅修改 --color-primary/secondary/accent，重新输出完整文件 |
| "换字体" | 仅替换字体（白名单内） |
| "重做第 N 张"（N为数字） | 仅重新设计该幻灯片的 HTML 结构 |
| "换风格" | 返回 STYLE_PREVIEWS.md，重新确认选择，从内容收集开始 |
| "加一页" | 在当前批次文件中插入新幻灯片，保持风格一致 |
| "减少一页" | 从当前批次文件中删除指定幻灯片 |
| "改成竖版" / "换布局" | 重新设计该幻灯片的 grid/flexbox 布局 |
| "调字号" / "字大一点" | 按比例调整 h1/h2/p 的 font-size |
| "加图表" / "加数据页" | 按当前风格添加 Chart.js 数据页 |
| "翻译成英文" | 将中文文本替换为英文，保持排版结构 |
| 无法识别 | 询问用户具体想改什么，可提供选项"换配色/换字体/换布局/其他" |

**批量生成（all）**：共24种风格，每次最多2种，按场景分组顺序分批生成：
批次1: 商业(1-3) → 批次2: 产品(4-7) → 批次3: 创意(8-11) → 批次4: 文化(12-15) → 批次5: 品牌(16-18) → 批次6: 学术(19-21) → 批次7: 娱乐(22-24)
每批完成后询问"是否继续下一批"。预计生成时间：24种约需12批次。

**中断处理**：若用户在任何步骤中断对话，重新激活时从最近未完成步骤继续，无需从头开始。

**文件路径告知**：生成完成后告知用户 HTML 文件的绝对路径，方便后续查找。

---

## 模式 B：PPTX 转换

当用户提供 `.pptx` 文件时：

1. 确认 PPTX 文件路径（支持拖拽路径或 Browse）
   - 文件损坏时（python-pptx 解析失败），提示用户检查文件完整性，询问是否尝试其他文件
   - 文件路径含中文或空格时：先检查 python-pptx 是否能正确解析，若失败提示用户重命名文件
2. 调用 `scripts/extract-pptx.py` 提取内容：
   - 输出 JSON 文件（extracted-slides.json）
   - 包含每页标题、正文、图片路径、备注
   - 用户确认 JSON 内容 → 生成 HTML → 再进入下一步
3. 按提取结果生成 HTML，设计风格以用户选定风格为准
4. 正常进入模式 A 第三步
   - 视频/音频：extract-pptx.py 暂不支持提取，生成 HTML 时用占位符替代，标注"[此处有视频]"
   - 转换多页 PPTX 时，确认需要转换全部页面还是指定范围
   - PPT 页数超过 20 页时：询问用户是否需要筛选重点页面，或按章节分段生成多个 HTML 文件

模式 B 转换完成后，用户可以像模式 A 一样请求修改（换配色/换字体/换布局等）。

---

## 多语言支持

可生成中英双语幻灯片，中英文内容分页或分栏排版。

---

## 在线部署

生成后可询问用户是否需要部署到 Vercel（运行 `~/.claude/skills/cjl-slides/scripts/deploy.sh`）。

---

## 24 种风格配色参考

| # | 风格 | 主色 | 配色 | 点缀 |
|---|------|-----|-----|-----|
| 1 | Pitch.com | #000000 | #FFFFFF | #635BFF |
| 2 | Bloomberg | #E42311 | #000000 | #FFE500 |
| 3 | Startup VC | #000000 | #1A1A1A | #00D4AA |
| 4 | Linear | #0F0F0F | #1A1A2E | #5E5AD4 |
| 5 | Vercel | #000000 | #111111 | #FFFFFF |
| 6 | NASA | #0B3D91 | #000000 | #E0E0E0 |
| 7 | Glassmorphism | #FFFFFF | #E0E5EC | #6366F1 |
| 8 | Framer | #000000 | #1A1A1A | #D4BBFF |
| 9 | Figma | #1A1A1A | #A259FF | #0D99FF |
| 10 | Duotone | #FA7268 | #7B61FF | #FEFEFE |
| 11 | Cyberpunk | #0D0D0D | #00F0FF | #FF2D6A |
| 12 | Swiss | #FFFFFF | #000000 | #FF0000 |
| 13 | Are.na | #1A1A1A | #CCCCCC | #8C5E3C |
| 14 | Wabi-Sabi | #F5F0EB | #C4A77D | #8B6F5C |
| 15 | 国风 | #F8F5F0 | #1A1A1A | #C41E3A |
| 16 | Teenage | #FF5800 | #000000 | #FFFFFF |
| 17 | Muji | #F5F5F0 | #1A1A1A | #CCCCCC |
| 18 | Luxury | #000000 | #F5F5F5 | #C9A96E |
| 19 | Stripe Press | #FFFFFF | #000000 | #6772E5 |
| 20 | Apple Keynote | #000000 | #1D1D1F | #F5F5F7 |
| 21 | Academic | #FFFEF0 | #1A1A1A | #8B0000 |
| 22 | Memphis | #FF6B6B | #4ECDC4 | #FFE66D |
| 23 | Brutalist | #FFFFFF | #000000 | #FF0000 |
| 24 | Y2K | #C0C0C0 | #0A0A0A | #FF00FF |

> 实际生成时可根据语义适当调整配色，但需保持风格辨识度。
