# Design Ads 设计系统规范 v2

> 完整的设计 token 和组件规范。核心目标：**封面大字冲击 + 内页内容充实 + 标题正文强对比**。

---

## 画布与空间系统

| 参数 | 值 |
|------|-----|
| 画布尺寸 | 1200 x 1800 px |
| 内边距 | 上下 150px，左右 120px |
| **内容区** | **960 x 1500 px**（这是实际可用空间） |
| 背景色 | `#0a0a0f` |

### 空间分配原则

```
┌──────── 1200px ────────────────┐
│120│                            │120│
│   │   ← 960px 内容宽度 →    │   │
│   │                            │   │
│   │   封面布局：               │   │
│   │   ┌─────────────────┐     │   │  1500px
│   │   │                 │     │   │  内容高度
│   │   │   大标题区域     │     │   │
│   │   │   (占35-45%)    │     │   │
│   │   │                 │     │   │
│   │   ├─────────────────┤     │   │
│   │   │   描述/网格/列表 │     │   │
│   │   │   (占30-40%)    │     │   │
│   │   │                 │     │   │
│   │   └─────────────────┘     │   │
│   │          ═╌╌╌╌╌╌╌╌═       │   │
│   │           分隔线          │   │
│150│                            │150│
└──────────────────────────────────┘
```

**铁律：所有可见元素必须在 960x1500px 内容区内完成布局，不能集中在顶部 1/3 区域。**

---

## 字体系统

> **双字体策略：思源宋体标题（权威感+视觉冲击）+ 思源黑体正文（可读性）**

### 字体族定义

```css
/* ====== 标题字体：思源宋体 ====== */
--font-serif: "Source Han Serif SC", "Noto Serif CJK SC",
  "STSong", "SimSun", "Songti SC", serif;

/* ====== 正文字体：思源黑体 ====== */
--font-sans: "Source Han Sans SC", "Noto Sans CJK SC",
  "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
  "Helvetica Neue", Arial, sans-serif;

/* 等宽字体：代码块 */
--font-mono: "Source Code Pro", "SF Mono", "Menlo",
  "Monaco", "Consolas", monospace;
```

### 字号层级表

> **移动端优化说明**：针对移动端观看场景（图片在手机上显示时会被缩小），所有字号在原设计基础上增加约 35-40%。

**封面专用（信息精简，字号拉到最大）：**

| 层级 | 用途 | 字号 | 字重 | 字体 | 占内容区高度比 |
|------|------|------|------|------|---------------|
| **CT1** | 封面主标题第1行 | **160-175px** | **900** | 思源宋体 | ~9% |
| **CT2** | 封面主标题后续行 | **140-155px** | **900** | 思源宋体 | ~8.5% |
| **CB1** | 封面描述文字 | **32-36px** | **400** | 思源黑体 | ~2% |
| **CL** | 封面标签/Badge | **20-22px** | **600** | 思源黑体 | ~1.3% |

**内页专用（内容充实，标题仍要突出）：**

| 层级 | 用途 | 字号 | 字重 | 字体 | 与正文的比 |
|------|------|------|------|------|-----------|
| **IT1** | 内页主标题 | **95-110px** | **900** | 思源宋体 | **3.5:1** |
| **IT2** | 卡片/区块小标题 | **45-52px** | **700** | 思源宋体 | **1.7:1** |
| **IB1** | 正文/描述（统一） | **28-32px** | **400** | 思源黑体 | 基准 |
| **IB2** | 列表项文字 | **26-30px** | **400** | 思源黑体 | 基准 |
| **IB3** | 代码块/Prompt | **25-28px** | **400** | 思源黑体/等宽 | 基准 |
| **IL** | 标签/STEP编号 | **17-20px** | **600** | 思源黑体 | — |

### 对比度速查

```
内页标题 IT1 (100px) ████████████████████████  3.5x
卡片标题 IT2 (48px)  ██████████                  1.6x
正文 IB1    (28px)  █████                       基准
标签 IL    (18px)  ███                          0.65x
```

**标题至少是正文的 3.5 倍，确保一眼区分层级。**

### CSS 工具类

> **移动端优化**：以下字号已针对移动端观看场景优化，整体增大约 35-40%。

```html
<style>
:root {
  --font-serif: "Source Han Serif SC", "Noto Serif CJK SC",
    "STSong", "SimSun", "Songti SC", serif;
  --font-sans: "Source Han Sans SC", "Noto Sans CJK SC",
    "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
    "Helvetica Neue", Arial, sans-serif;
}

/* === 封面标题（超大）=== */
.title-cover-main {
  font-family: var(--font-serif);
  font-weight: 900;
  font-size: 165px;
  line-height: 1.12;
}
.title-cover-sub {
  font-family: var(--font-serif);
  font-weight: 900;
  font-size: 145px;
  line-height: 1.14;
}

/* === 内页标题（大但小于封面）=== */
.title-inner-main {
  font-family: var(--font-serif);
  font-weight: 900;
  font-size: 100px;
  line-height: 1.18;
}
.title-inner-block {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 48px;
  line-height: 1.35;
}

/* === 正文（统一用思源黑体）=== */
.text-body {
  font-family: var(--font-sans);
  font-weight: 400;
  font-size: 30px;
  line-height: 1.65;
  color: #9ca3af;
}
.text-label {
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 20px;
  letter-spacing: 2px;
  text-transform: uppercase;
}
.text-code {
  font-family: var(--font-sans); /* 或 var(--font-mono) */
  font-weight: 400;
  font-size: 26px;
  line-height: 1.75;
  color: #d1d5db;
}

/* 渐变文字 */
.gradient-text {
  background: linear-gradient(135deg, var(--accent-start), var(--accent-end));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
```

---

## 配色方案

### 主题色（4 种）

```css
/* 紫色 - 默认科技/AI */
--accent-purple-start: #8b5cf6;  --accent-purple-end: #a78bfa;
--badge-bg-purple: rgba(139, 92, 246, 0.15);
--icon-bg-purple: rgba(139, 92, 246, 0.12);

/* 青色 - 创意/视频 */
--accent-cyan-start: #06b6d4;    --accent-cyan-end: #22d3ee;
--badge-bg-cyan: rgba(6, 182, 212, 0.15);
--icon-bg-cyan: rgba(6, 182, 212, 0.12);

/* 蓝色 - 工具/效率 */
--accent-blue-start: #3b82f6;    --accent-blue-end: #60a5fa;
--badge-bg-blue: rgba(59, 130, 246, 0.15);
--icon-bg-blue: rgba(59, 130, 246, 0.12);

/* 金色 - 教育/课程 */
--accent-gold-start: #f59e0b;    --accent-gold-end: #fbbf24;
--badge-bg-gold: rgba(245, 158, 11, 0.15);
--icon-bg-gold: rgba(245, 158, 11, 0.12);
```

### 中性色

```css
--bg-primary: #0a0a0f;
--bg-card: rgba(255, 255, 255, 0.04);
--text-primary: #ffffff;
--text-secondary: #d1d5db;
--text-muted: #9ca3af;
--text-dim: #6b7280;
--border-default: rgba(255, 255, 255, 0.08);
```

---

## 模板布局详解

### 封面-1: cover-center（居中图标型）

**适用：合集总览、概念介绍**
**特点：极简信息 + 超大字号撑满空间**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配（1680px 内容高）：
├─ 顶部留白:        8-10% (~140-170px)
│  └─ 图标容器:     140x140px
│  └─ 英文标签:     20px, uppercase
│  └─ 间距:         30-36px
├─ 主标题区:        40-48% (~670-810px)  ← 视觉主体
│  └─ 第1行:        160-175px, 思源宋体 900
│  └─ 第2行:        140-155px, 思源宋体 900
│  └─ 第3行(如有):   130-145px, 思源宋体 900
├─ 描述文字:        8-12% (~135-200px)
│  └─ 32-36px, 思源黑体, 居中, max-width 800px
├─ 底部留白:        25-30% → 自然过渡到分隔线
└─ 分隔线:          距底 150px
```

**关键：主标题的字号要让 2-3 行文字占据内容区纵向的 40% 以上。**

### 封面-2: cover-grid（特性网格型）

**适用：多步骤教程、功能清单**
**特点：标题 + 2x2 网格填满中下部空间**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配：
├─ 顶部区 (25%):     Badge + 大标题(135-150px) + 描述(32px)
├─ 网格区 (55-60%):  2x2 网格卡片 ← 充分利用空间
│  └─ 每张卡片:
│      ├─ 图标圆圈:  80x80px
│      ├─ 特性名:    46px, 思源宋体 700
│      └─ STEP编号:  18px, uppercase
│  └─ 卡片间距:      24px
│  └─ 卡片内边距:    36px 32px
└─ 分隔线:           距底 150px
```

**关键：4 张网格卡片的高度加起来应占内容区的 50% 以上，每张卡片约 280-320px 高。**

### 封面-3: cover-list（列表展示型）

**适用：清单、目录式内容**
**特点：左侧标题 + 右侧大数字装饰 + 列表卡片填充**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配：
├─ 顶部区 (28%):     Badge + 标题(135-150px) + 描述卡片
│  └─ 右侧大数字:    220-280px 半透明装饰字
│  └─ 描述卡片:      左侧彩色竖条 + 文字
├─ 列表区 (47-52%):  2列列表卡片 ← 主要内容区
│  └─ 每张卡片:
│      ├─ 图标:       32px
│      ├─ 文字:       28px, 思源黑体
│      └─ 卡片高度:   自适应, 约 90-110px
│  └─ 卡片间距:      16-20px
└─ 分隔线:            距底 150px
```

### 内页-1: inner-tool（工具详情型）

**适用：单个工具/产品详细介绍**
**特点：内容充实，标题大，描述详细**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配：
├─ 头部区 (22-25%):  Badge + 工具名(95-110px) + 英文名(28px)
├─ 描述卡片区 (25-30%):
│  └─ 左侧竖条卡片:
│      ├─ 功能描述:   2-4句, 30px 思源黑体
│      └─ 详细说明子卡: 图标+文字
├─ 链接卡片区 (12-15%):
│  └─ GitHub 风格卡: 图标 + REPOSITORY + owner/repo
└─ 分隔线:            距底 150px
```

**如果内容更多（如多个功能点），拆成多张图：**
- 第1张：工具名 + 核心功能概述
- 第2张：详细功能列表 + 使用场景
- 第3张（如有）：代码示例 / 高级配置

### 内页-2: inner-prompt（提示词模板型）

**适用：Prompt 模板、AI 指令展示**
**特点：代码块是主角，要给足够空间显示完整文本**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配：
├─ 头部区 (20-23%):  Badge + 标题(95-110px) + 副描述(28px)
├─ Prompt代码区 (32-40%):  ← 最大区块
│  └─ 代码块卡片:
│      ├─ 标签:       PROMPT, 18px uppercase
│      ├─ 内容:       26-28px, 多行完整保留
│      └─ 内边距:     28-32px
├─ 标签卡片区 (15-18%): 2-3个标签按钮
├─ 适用场景区 (12-15%): 场景说明文字
└─ 分隔线:              距底 150px
```

**Prompt 文字较长时优先保证代码块完整显示，可适当压缩其他区域。**

### 内页-3: inner-persona（人设系统型）

**适用：角色设定、System Prompt**
**特点：系统提示词代码块 + 场景列表**
> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```
空间分配：
├─ 头部区 (18-20%):  Badge + 角色名(95-110px) + 英文副标题(28px)
├─ 系统提示词区 (35-42%):  ← 最大区块
│  └─ 代码块:
│      ├─ 标签:       SYSTEM PROMPT, 18px
│      ├─ 内容:       26-28px, 完整保留换行
│      └─ 内边距:     28-32px
├─ 场景列表区 (20-25%): 3-5个场景条目
│  └─ 每条: 图标 + 场景名 + 说明(28px)
└─ 分隔线:              距底 150px
```

---

## 组件规范

### 1. 标签 Badge

> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  height: 50px;
  padding: 14px 26px;
  border-radius: 25px;
  background: var(--badge-bg);
  border: 1px solid var(--badge-border);
  font-family: var(--font-sans);
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent-color);
}
.badge svg { width: 22px; height: 22px; }
```

### 2. 特性网格卡片（封面-2）

> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```css
.feature-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 20px;
  padding: 44px 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 让卡片在网格中均匀分布 */
  text-align: center;
  min-height: 280px; /* 保证卡片有足够高度 */
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--icon-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 26px;
}
.feature-icon svg { width: 38px; height: 38px; }

.feature-title {
  font-family: var(--font-serif);
  font-size: 46px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 14px;
}

.feature-step {
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 500;
  color: var(--text-dim);
  letter-spacing: 2px;
  text-transform: uppercase;
}
```

### 3. 列表卡片（封面-3 / 内页通用）

> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```css
.list-card {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: 26px 30px;
  display: flex;
  align-items: center;
  gap: 18px;
}
.list-card svg { width: 32px; height: 32px; flex-shrink: 0; }
.list-card span {
  font-family: var(--font-sans);
  font-size: 28px;
  color: var(--text-secondary);
}
```

### 4. 内容详情卡片（内页）

> **移动端优化**：字号已增大 35-40% 以适配移动端观看

```css
.content-card {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 20px;
  padding: 38px 42px;
}
.content-card-accent {
  border-left: 4px solid var(--accent-color);
}

.code-block {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 32px 38px;
  font-family: var(--font-sans);
  font-size: 26px;
  line-height: 1.75;
  color: var(--text-secondary);
}
.code-block-label {
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-dim);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 18px;
}
```

### 5. 底部分隔线

```css
.divider {
  position: absolute;
  bottom: 150px;
  left: 120px;
  right: 120px;
  height: 1px;
  background: repeating-linear-gradient(
    to right,
    rgba(255, 255, 255, 0.1) 0,
    rgba(255, 255, 255, 0.1) 6px,
    transparent 6px,
    transparent 12px
  );
}
```

---

## SVG 图标库

```html
<!-- 星星/火花 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>

<!-- 笔/编辑 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.83 0 114 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>

<!-- 搜索 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>

<!-- 播放/视频 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18"/><path d="M10 8l6 4-6 4V8z"/></svg>

<!-- 发送/分享 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>

<!-- 层叠/堆栈 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>

<!-- 调色板 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="13.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="10.5" r="2.5"/><circle cx="8.5" cy="7.5" r="2.5"/><circle cx="6.5" cy="12.5" r="2.5"/><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/></svg>

<!-- 电影胶片 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18"/><path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 17h5M17 7h5"/></svg>

<!-- 日历 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>

<!-- 书本 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>

<!-- 组织结构 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="12" r="3"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="9" y1="12" x2="6" y2="12"/><line x1="15" y1="12" x2="18" y2="12"/></svg>

<!-- 用户/人设 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>

<!-- GitHub -->
<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>

<!-- 终端/命令行 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>

<!-- 数据库 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>

<!-- 文件/文档 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>

<!-- 消息/评论 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>

<!-- 目标/靶心 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
```

---

## HTML 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1200">
  <style>
    :root {
      --font-serif: "Source Han Serif SC", "Noto Serif CJK SC",
        "STSong", "SimSun", "Songti SC", serif;
      --font-sans: "Source Han Sans SC", "Noto Sans CJK SC",
        "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
        "Helvetica Neue", Arial, sans-serif;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 1800px;
      background: #0a0a0f;
      font-family: var(--font-sans);
      overflow: hidden;
      position: relative;
      color: #ffffff;
      padding: 150px 120px;
    }
    /* ... 具体模板样式 ... */
  </style>
</head>
<body>
  <!-- 内容区 960x1500px，充分利用 -->
</body>
</html>
```

**注意事项：**
- `body` 设置 `padding: 60px` 后自然形成 1080x1680px 内容区
- 所有内容在这个区域内排版
- 标题必须用 `var(--font-serif)` + 900 weight
- 正文统一用 `var(--font-sans)` + 20-22px
- 依赖系统已安装的「思源宋体」和「思源黑体」
