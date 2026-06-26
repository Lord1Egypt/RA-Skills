---
name: design-md
description: >
  DESIGN.md 设计与品牌规范技能。当用户需要创建项目设计规范文档、为AI编写品牌规范、让AI生成符合品牌风格的页面时激活。
  触发词：DESIGN.md、设计规范、品牌规范、设计系统、生成设计文档、写DESIGN.md、设计语言。
  用于：创建新项目的 DESIGN.md、更新已有设计规范、让AI按规范生成UI。
version: 1.0.0
---

# DESIGN.md — AI 时代的设计规范技能

> 让 AI 生成的每个页面，都符合你的品牌规范。

---

## 核心概念

**DESIGN.md** 是 Google Stitch 提出的设计规范格式——用纯文本 Markdown 描述完整设计系统，AI 能直接理解和执行。

**为什么是 Markdown？**
- AI 最擅长处理 Markdown
- 比 Figma 文件更好解析
- 比 JSON Design Token 更好读
- 放在项目根目录，AI coding agent 启动即加载

---

## 触发场景

- "帮我写一个 DESIGN.md"
- "为这个项目创建设计规范"
- "按这个规范生成一个页面"
- "更新项目的 DESIGN.md"
- "让我生成的页面风格一致"

---

## DESIGN.md 标准结构（9个模块）

每个 DESIGN.md 必须包含以下内容：

### M1 — Visual Theme & Atmosphere
用自然语言描述产品的"气质"，AI 需要理解整体感觉才能生成风格一致的内容。

```markdown
## M1 — Visual Theme & Atmosphere

DeepFMT 的视觉气质：
- **核心关键词**：专业 / 温暖 / 可信赖 / 轻量
- **情绪版**：医院的专业感，但不像传统医院那么冷；像一位值得信赖的家庭医生
- **设计哲学**：功能清晰，视觉减负；患者不需要在UI里感到压力
- **密度**：中等偏低，内容之间留有充分呼吸空间
- **明暗**：整体偏亮，避免大面积深色带来的压抑感
```

### M2 — Color Palette & Roles
完整颜色系统，每个颜色必须标注：语义名称 / HEX / RGBA / 使用场景。

```markdown
## M2 — Color Palette & Roles

| 角色 | 色值 | 使用场景 |
|------|------|---------|
| Primary | #2D7A4F | 主按钮、导航激活态、关键数据 |
| Primary Light | #3A9460 | Hover态、次级强调 |
| Primary Dark | #1F5E3A | 按下态、深色背景 |
| Accent | #FF8C42 | CTA按钮、重要提示、亮点 |
| Accent Light | #FFA066 | 渐变辅助、hover |
| Background | #F5F9F6 | 全局背景（医疗绿调白）|
| Surface | #FFFFFF | 卡片、输入框、浮层 |
| Text Primary | #1A1A1A | 正文 |
| Text Secondary | #666666 | 说明文字 |
| Text Tertiary | #999999 | 占位符、次要标签 |
| Border | #E8F2EC | 边框、分割线 |
```

### M3 — Typography Rules
字体系统：字体族 / 字重 / 字号 / 行高 / 字间距全套层级。

```markdown
## M3 — Typography Rules

### 字体族（移动端优先）
- 中文：'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif
- 数字/英文：'SF Pro Display', -apple-system, BlinkMacSystemFont
- 等宽：'SF Mono', 'Fira Code', monospace（用于数据展示）

### 字号层级
| 层级 | 字号 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Hero | 28px | 700 | 1.3 | 页面大标题 |
| H1 | 22px | 700 | 1.4 | 模块标题 |
| H2 | 18px | 600 | 1.4 | 卡片标题 |
| Body | 16px | 400 | 1.6 | 正文 |
| Caption | 14px | 400 | 1.5 | 说明文字 |
| XS | 12px | 400 | 1.4 | 标签、角标 |

### 字间距：标题用 -0.5px 负间距压缩感，正文保持标准。
```

### M4 — Component Stylings
所有组件样式，包含各状态（Default / Hover / Active / Disabled / Loading / Error）。

```markdown
## M4 — Component Stylings

### 主按钮
- Default: bg-primary (#2D7A4F), text-white, rounded-btn (8px), py-3 px-6
- Hover: bg-primary-light (#3A9460)
- Active: bg-primary-dark (#1F5E3A), scale(0.98)
- Disabled: opacity-40, cursor-not-allowed
- Loading: 左侧 spinner，文字变为"处理中..."

### 次按钮
- Default: border border-primary text-primary bg-transparent
- Hover: bg-primary/10

### 卡片
- bg-white rounded-card (16px) shadow-sm
- padding: 16px（内容卡片）/ 20px（大卡片）
- 内部分割：border-t border-[#E8F2EC] 或 gap-4

### 输入框
- bg-white rounded-input (12px) border border-[#E8F2EC]
- Focus: border-primary ring-2 ring-primary/20
- Error: border-red-500 ring-2 ring-red-500/20
```

### M5 — Layout Principles
间距体系与网格原则。

```markdown
## M5 — Layout Principles

### 间距系统（4px基准）
| Token | 值 | 用途 |
|-------|-----|------|
| space-xs | 4px | 图标与文字间距 |
| space-sm | 8px | 紧凑元素间距 |
| space-md | 12px | 标准元素间距 |
| space-lg | 16px | 区块内间距 |
| space-xl | 24px | 区块间间距 |
| space-2xl | 32px | 大区块间距 |

### 页面布局
- 最大内容宽度：max-w-lg (448px)，居中
- 左右安全边距：px-4（16px）
- 页面顶部：pt-4
- 页面底部：pb-[68px]（底部导航高度）

### 栅格：单列布局为主，偶尔2列（卡片并排）。
```

### M6 — Depth & Elevation
阴影层级系统。

```markdown
## M6 — Depth & Elevation

| Level | 样式 | 用途 |
|-------|------|------|
| L0 | 无阴影 | 默认状态 |
| L1 | shadow-sm | 卡片默认态 |
| L2 | shadow-md | 浮层、弹窗背景 |
| L3 | shadow-lg | Modal、浮出菜单 |
| L4 | shadow-xl | 强层级弹窗 |

### 医疗场景特殊性
- 避免过度阴影（医疗用户不需要"重量感"）
- 阴影 opacity 不超过 0.1，避免压抑
- 优先用 border 代替阴影来区分层级
```

### M7 — Do's and Don'ts
设计禁区与正确示范。

```markdown
## M7 — Do's and Don'ts

### ✅ 正确做法
- 用 Primary 绿做主操作按钮
- 重要数据（如评分、日期）用 Accent 橙高亮
- 卡片内使用 rounded-card (16px)
- 列表项之间用 border 分割，不用分隔线

### ❌ 错误做法
- 不要用蓝色作为主色调（与医疗信任感冲突）
- 不要用深色背景（患者需要明亮、轻松的氛围）
- 不要用太小的字体（14px以下正文需避免）
- 不要在大面积使用渐变背景
- 不要用纯黑文字（#000000），用 #1A1A1A 减少压迫感
```

### M8 — Responsive Behavior
响应式行为与移动端特殊处理。

```markdown
## M8 — Responsive Behavior

### 移动端优先
- 设计基于375px宽度的iPhone
- 触控热区最小44×44px
- 底部固定导航高度60px，内容区 pb-[68px]

### 断点（必要时）
- sm: 640px（平板横屏）
- lg: 1024px（桌面端）

### 文字截断
- 单行截断：truncate，max-w-xs
- 两行截断：line-clamp-2
```

### M9 — Agent Prompt Guide
给 AI coding agent 的快速参考与提示模板。

```markdown
## M9 — Agent Prompt Guide

### 快速颜色参考
- Primary: #2D7A4F
- Accent: #FF8C42
- Background: #F5F9F6
- Surface: #FFFFFF
- Text: #1A1A1A / #666666 / #999999

### AI 生成提示模板
"请按以下规范生成页面：
- 颜色：Primary #2D7A4F，Accent #FF8C42，Background #F5F9F6
- 字体：正文16px，行高1.6
- 圆角：卡片16px，按钮8px，输入框12px
- 间距：16px区块间距，底部导航占68px
- 阴影：卡片用 shadow-sm
- 不要：深色背景、蓝色主色调、过度阴影"

### Tailwind 速查
- 主按钮：bg-primary text-white rounded-btn px-6 py-3
- 卡片：bg-white rounded-card shadow-sm p-4
- 输入框：bg-white rounded-input border border-[#E8F2EC]
```

---

## 执行流程

### 场景1：创建新项目 DESIGN.md

1. 询问用户：产品定位、目标用户、品牌关键词
2. 提取已有设计资源（Tailwind配置、颜色变量、品牌资料）
3. 按 M1-M9 框架撰写完整 DESIGN.md
4. 保存到 `DESIGN.md`（项目根目录）
5. 给用户一个 AI 使用示例

### 场景2：更新已有 DESIGN.md

1. 读取现有 DESIGN.md
2. 确认要修改的模块
3. 增量更新对应章节
4. 标注版本号

### 场景3：按 DESIGN.md 生成页面

1. 读取项目根目录的 DESIGN.md
2. 确认页面需求
3. 生成页面代码，在生成时严格遵循 M1-M9 规范
4. 自检：颜色是否正确、字号层级是否符合、圆角是否匹配

---

## 参考资源

详细案例参考：
- VoltAgent/awesome-design-md：https://github.com/VoltAgent/awesome-design-md
- Google Stitch DESIGN.md 官方格式：https://stitch.withgoogle.com/docs/design-md/overview/
- 模板文件：`references/design-md-template.md`
