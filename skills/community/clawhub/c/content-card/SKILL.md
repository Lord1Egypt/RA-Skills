---
name: content-card
description: >
  将内容铸成 PNG 视觉卡片。三种模具：-l 长图阅读卡（默认）、-i 信息图、-m 多卡。
  输入文本/URL/文件，输出高品质 PNG。
  Use when: (1) 用户说"做成卡片"/"做成图"/"铸"/"cast",
  (2) 用户说"知识卡片"/"信息图"/"infograph",
  (3) 需要将文章/笔记/分析结果转为可分享的图片,
  (4) 公众号/小红书需要文字密集型配图（数据对比、流程图、知识点总结）。
  NOT for: 照片/插图/AI 艺术图（用 Gemini/Seedream 生图）、
  纯数据图表/柱状图（用代码或 xlsx 生成）。
---

# content-card: 铸

将内容铸成可见的形态。内容进去，PNG 出来。模具决定形状。

## 参数

| 参数 | 模具 | 尺寸 | 说明 |
|------|------|------|------|
| `-l`（默认） | 长图 | 1080 x auto | 单张阅读卡，内容自动撑高 |
| `-i` | 信息图 | 1080 x auto | 数据/结构驱动的自适应视觉布局 |
| `-m` | 多卡 | 1080 x 1440 | 自动切分为多张卡片（小红书/朋友圈适用） |
| `--style` | 风格 | — | `minimal-mono` / `morandi-warm` / `tech-dark` / `paper-craft` / `corporate-clean`，默认：根据气质自动选 |

### 小红书安全区（`-m` 模式必读）

小红书移动端 UI 会遮挡图片以下区域，关键信息必须避开：

```
┌─────────────────────────────┐
│                 [❤️ 📌 💬]  │  ← 右上角 15%：点赞/收藏/评论按钮
│                             │
│      ✓ 安全内容区域          │
│                             │
│  [笔记标题 + 用户头像栏]     │  ← 底部 10%：标题栏遮挡
│                   [@水印]   │  ← 右下角 10%：平台水印
└─────────────────────────────┘
```

在 `-m` 模式生成 HTML 时，确保底部 10% 区域不放置关键文字或数据。

## 获取内容

- URL → `web_fetch` 获取
- 粘贴文本 → 直接使用
- 文件路径 → `read` 获取

## 执行流程

### Step 1: 加载用户偏好

检查 EXTEND.md 配置文件（优先级：项目级 > 用户级）：

| 优先级 | 路径 |
|--------|------|
| 1 | `.content-card/EXTEND.md`（当前工作目录） |
| 2 | `~/.config/content-card/EXTEND.md` |

- 找到：读取并解析，后续步骤中使用配置值作为默认值
- 未找到：静默跳过，使用 SKILL.md 默认值

配置 schema 见 `references/config/preferences-schema.md`。

### Step 2: 理解内容

读取输入内容，提取：
- 核心主题/标题
- 关键信息点（数据、结论、对比、流程）
- 内容气质：思辨/哲学、技术/工程、文学/叙事、科学/研究、商业/产品

### Step 3: 关键词快捷匹配

用户输入中如果包含以下关键词，直接跳过气质推断和布局推荐，使用预设组合：

| 用户关键词 | 布局 | 风格 | 默认比例 | 说明 |
|-----------|------|------|---------|------|
| 高密度信息大图 / high-density | `dense-modules` | `corporate-clean` | portrait | 信息密度优先 |
| 对比图 / vs / 对比 | `binary-comparison` | `minimal-mono` | landscape | 左右分屏对比 |
| 时间线 / timeline / 历程 | `linear-progression` | `morandi-warm` | portrait | 线性时间推进 |
| 流程图 / 步骤 / tutorial | `linear-progression` | `corporate-clean` | portrait | 步骤指引 |
| 数据看板 / dashboard / KPI | `dashboard` | `tech-dark` | landscape | 指标展示 |
| 知识卡片 / 总结卡 | `bento-grid` | `morandi-warm` | portrait | 多主题总览 |
| 对比矩阵 / 功能对比 | `comparison-matrix` | `minimal-mono` | landscape | 多因素对比表 |
| 思维导图 / mindmap | `hub-spoke` | `paper-craft` | landscape | 中心发散 |
| 漏斗 / funnel / 转化 | `funnel` | `corporate-clean` | portrait | 转化漏斗 |
| 冰山 / iceberg / 深层 | `iceberg` | `morandi-warm` | portrait | 表层vs深层 |

匹配规则：
- 匹配到关键词后自动应用预设，跳到 Step 3（生成 HTML）
- 用户仍可通过 `--layout` / `--style` 覆盖预设
- 多个关键词同时命中时，取第一个匹配

### Step 4: 结构化内容（信息图专用）

`-i` 模式在理解内容后，增加一步结构化转换：

1. 提取标题和核心主张
2. 将内容拆解为独立模块（每个模块 = 一个布局区块）
3. 为每个模块标注：关键概念、核心数据、视觉元素建议
4. **数据保真**：源数据原样保留，不概括不改写。统计数字、引用、专有名词必须逐字保留
5. **凭据剥离**：如果源内容包含 API Key、Token、密码等敏感信息，必须在此步骤剥离

输出到 `temp/content-card/structured-content.md` 文件。好处：
- 换风格/布局时直接复用，不用重新分析
- 用户可在此文件上手动修改后重新生成
- 保留分析过程的可追溯性

如果 `temp/content-card/structured-content.md` 已存在且内容未变，跳过分析直接复用。

### ⚠️ 检查点（Step 2-4 完成后）

内容理解 + 结构化完成后，如果用户未指定风格/配色，简要告知选择的方案再继续：
"内容偏 [气质]，准备用 [风格] + [配色] 做长图，可以吗？"
用户确认或无异议后继续。简单/重复任务可跳过。

### Step 5: 感知内容气质，选择配色

> **气质决定配色方向，风格决定视觉系统。** 气质在这一步确定，风格在 Step 2.5 确定。

| 气质 | 底色方向 | 强调色方向 |
|------|---------|-----------|
| 思辨/哲学 | 暖灰、米白 | 深红、琥珀 |
| 技术/工程 | 冷灰、深蓝灰 | 青色、蓝绿 |
| 文学/叙事 | 暖白、奶油 | 赭石、深橄榄 |
| 科学/研究 | 纯白、浅灰 | 深蓝、靛蓝 |
| 商业/产品 | 浅灰、暖白 | 深橙、深青 |

### Step 6: 选择视觉风格

如果用户指定了 `--style`，使用指定风格。否则根据气质自动推荐：

| 气质 | 默认 Style | 备选 |
|------|-----------|------|
| 思辨/哲学 | `minimal-mono` | `morandi-warm` |
| 技术/工程 | `tech-dark` | `minimal-mono` |
| 文学/叙事 | `morandi-warm` | `paper-craft` |
| 科学/研究 | `minimal-mono` | `corporate-clean` |
| 商业/产品 | `corporate-clean` | `minimal-mono` |

风格定义文件在 `references/styles/<style>.md`，生成 HTML 时读取对应文件中的 CSS 变量。

## 信息图布局库（`-i` 模式可选布局）

信息图有两个维度：**布局**（信息结构）× **内容气质**（已有的配色系统）。

| 布局 | 最佳场景 | 结构描述 |
|------|---------|----------|
| `bento-grid` | 多主题总览、知识合集（默认） | 不等分网格，每块独立主题 |
| `linear-progression` | 时间线、流程、教程步骤 | 从左到右或从上到下的线性推进 |
| `binary-comparison` | A vs B、before/after、优劣对比 | 左右对称分屏 |
| `hierarchical-layers` | 金字塔、优先级层级 | 从上到下的层级堆叠 |
| `hub-spoke` | 中心概念 + 关联要素 | 中心节点向外放射 |
| `funnel` | 转化漏斗、筛选过程 | 从宽到窄的漏斗形 |
| `iceberg` | 表面 vs 深层、显性 vs 隐性 | 水面线分隔，上下两部分 |
| `dashboard` | 指标看板、KPI 展示 | 数字大卡片 + 图表组合 |
| `winding-roadmap` | 旅程、里程碑 | 蜿蜒路径上的节点 |
| `circular-flow` | 循环过程、生态系统 | 首尾相连的环形 |
| `comparison-matrix` | 多因素对比、功能矩阵 | 行列网格，✓/✗ 标记 |
| `dense-modules` | 高密度信息、数据手册 | 紧凑模块化，最大信息密度 |

自动推荐：根据内容结构自动匹配最佳布局。

### 内容类型 → 布局推荐

| 内容类型 | 推荐布局 | 备选 |
|---------|---------|------|
| 时间线/历史 | `linear-progression` | `winding-roadmap` |
| 步骤教程 | `linear-progression` | `funnel` |
| A vs B 对比 | `binary-comparison` | `comparison-matrix` |
| 多因素对比 | `comparison-matrix` | `binary-comparison` |
| 层级/优先级 | `hierarchical-layers` | — |
| 中心概念+扩展 | `hub-spoke` | `bento-grid` |
| 转化/筛选 | `funnel` | `linear-progression` |
| 显性 vs 隐性 | `iceberg` | `hierarchical-layers` |
| 指标/数据 | `dashboard` | `dense-modules` |
| 旅程/路线 | `winding-roadmap` | `linear-progression` |
| 循环过程 | `circular-flow` | `hub-spoke` |
| 多主题总览 | `bento-grid` | `dense-modules` |
| 高密度手册 | `dense-modules` | `bento-grid` |

### 气质 × 布局 兼容矩阵

选定内容气质和布局后，检查此矩阵确保组合合理：

| 气质 \ 布局 | bento-grid | linear | binary-comp | hierarchical | hub-spoke | funnel | iceberg | dashboard | roadmap | circular | comp-matrix | dense-mod |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 思辨/哲学 | ✓ | ✓ | ✓✓ | ✓✓ | ✓✓ | ✗ | ✓✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| 技术/工程 | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ |
| 文学/叙事 | ✓ | ✓✓ | ✓ | ✗ | ✓ | ✗ | ✓✓ | ✗ | ✓✓ | ✓ | ✗ | ✗ |
| 科学/研究 | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ |
| 商业/产品 | ✓✓ | ✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✗ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ |

> ✓✓ 强推荐 | ✓ 可用 | ✗ 不推荐（气质与布局形式冲突，效果差）
>
> 核心逻辑：思辨/文学偏深度叙事，避免数据密集型布局；技术/科学/商业偏结构化，避免纯叙事型布局。

**兼容检查**：选定气质+布局后查此矩阵。有 ✗ 则提示调整或换备选布局。

### 内容信号 → 气质+布局自动推荐

根据输入内容的关键词信号，自动推荐气质和布局组合：

| 内容信号 | 气质 | 推荐布局 | 备选 |
|---------|------|---------|------|
| AI、架构、系统、代码、框架 | 技术/工程 | `bento-grid` | `hub-spoke` |
| 对比、vs、选型、优劣 | 技术/工程 | `binary-comparison` | `comparison-matrix` |
| 产品、增长、转化、商业模式 | 商业/产品 | `funnel` | `dashboard` |
| KPI、指标、数据、ROI | 商业/产品 | `dashboard` | `dense-modules` |
| 哲学、思辨、本质、悖论 | 思辨/哲学 | `iceberg` | `hierarchical-layers` |
| 故事、经历、旅程、成长 | 文学/叙事 | `winding-roadmap` | `linear-progression` |
| 实验、论文、研究、假设 | 科学/研究 | `linear-progression` | `comparison-matrix` |
| 教程、步骤、流程、操作 | 技术/工程 | `linear-progression` | `bento-grid` |
| 生态、循环、闭环、飞轮 | 商业/产品 | `circular-flow` | `hub-spoke` |
| 层级、金字塔、优先级 | 思辨/哲学 | `hierarchical-layers` | `hub-spoke` |

**混合信号时**：取第一个匹配的推荐，气质由主导信号决定。

### Step 7: 生成 HTML

**文件安全**：生成新文件前，如果目标路径已存在同名文件，自动重命名为 `{name}-backup-{YYYYMMDD-HHMMSS}.{ext}`。适用于：
- HTML 中间文件
- 最终 PNG 输出
- structured-content.md

示例：`report.png` 已存在 → 重命名为 `report-backup-20260420-225400.png` → 再生成新的 `report.png`

根据选择的模具，读取对应模板文件：
- `-l`：`assets/long_template.html`
- `-i`：`assets/infograph_template.html`
- `-m`：`assets/poster_template.html`

**注入风格变量**：读取 `references/styles/<style>.md` 中的 CSS 变量定义，将其注入到 HTML 的 `:root` 选择器中。风格变量覆盖模板默认值，实现布局 × 风格的自由组合。

将内容填充到模板的 `{{VARIABLE}}` 占位符中。

### Step 8: 品味检查

生成 HTML 后、截图前，Read `references/taste.md`，逐项过品味准则自检清单。

### Step 9: 截图

```bash
node ~/.openclaw/skills/content-card/scripts/capture.js <html文件路径> <输出png路径> <宽度> <高度> [fullpage]
```

默认宽度 1080，长图和信息图用 `fullpage` 模式（高度自适应）。

依赖：Playwright。如未安装：
```bash
cd ~/.openclaw/skills/content-card && npm install playwright && npx playwright install chromium
```

### Step 10: 交付

- 输出路径：`~/Downloads/{标题}.png`
- 报告文件路径

## 品味准则

Read `references/taste.md` — 所有模具的视觉质量底线。

核心原则：**反 AI 生成痕迹**。
- 禁 Inter 字体（用 Noto Serif SC / Geist / Satoshi）
- 禁纯黑 #000（用 #1a1a1a）
- 禁三等分卡片
- 禁居中 Hero
- 禁 AI 文案腔（赋能/无缝/释放）
- 禁假数据（99.99%）
- 最多 1 个强调色，饱和度 < 80%
- 阴影必须染色，不用灰色默认

## 使用场景示例

```
# 公众号知识卡片
/content-card -l 将这段 Agent 架构分析做成长图

# 小红书多卡
/content-card -m 把这个对比表做成多张卡片

# 数据信息图
/content-card -i 将这份项目分析报告做成信息图
```

## 设计品味准则

通用品味准则见 `~/.openclaw/workspace/references/design-taste.md`，覆盖品牌协议、反 AI slop、品味锚点、事实验证。本 skill 遵守该文件的所有规则。涉及具体品牌时必须走品牌资产协议 5 步流程。
