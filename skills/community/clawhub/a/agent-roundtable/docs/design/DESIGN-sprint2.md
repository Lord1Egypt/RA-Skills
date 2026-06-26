# agent-roundtable v2 Sprint 2 设计规范

> **设计师**：像素姐 🎨 | **日期**：2026-05-26
> **分支**：feature/v2-ux-improvements
> **关联 PRD**：docs/product/PRD-sprint2.md

---

## 1. 概述与设计原则

### 1.1 设计目标

Sprint 2 为 agent-roundtable WebViewer 带来两项核心体验升级：

1. **发布自动化状态看板**：tag push 后，PyPI / ClawHub / GitHub Pages 三渠道发布状态一目了然
2. **讨论回放模式**：讨论结束后可逐段回看 AI 讨论过程，像看录像一样回溯推理链

### 1.2 设计原则（延续 Sprint 1）

| 原则 | Sprint 2 延伸 |
|------|--------------|
| **渐进呈现** | 回放时信息按原始节奏逐步重现，不一次性剧透结论 |
| **角色可辨** | 回放模式下 Agent 色彩、头像、徽章保持一致 |
| **焦点明确** | 正在播放的发言最突出，已播放的自然弱化 |
| **流畅过渡** | 播放/暂停/跳转全有动画衔接，进度条拖拽顺滑 |
| **移动友好** | 回放控制栏触控友好，≥44px 触摸目标 |

### 1.3 设计语言沿用

延续 Sprint 1 的 `theme.css` 设计体系：
- **色彩**：Dark Slate 底色（`#0F172A`）+ 角色色标识
- **圆角**：小 6px / 中 10px / 大 16px
- **字体**：系统字体栈（PingFang SC + SF Pro）
- **动效**：`cubic-bezier(0.4, 0, 0.2, 1)` 缓动曲线
- **间距**：4px 网格基准

### 1.4 新增设计令牌

Sprint 2 新增以下 CSS 变量，复用 Sprint 1 已有体系：

```css
:root {
  /* 回放模式专用色 */
  --rt-replay-bg: #0D1525;           /* 比实时模式底色更深一级 */
  --rt-replay-accent: #6366F1;       /* 回放强调色（靛蓝） */
  --rt-replay-accent-glow: rgba(99, 102, 241, 0.2);
  --rt-replay-progress-track: rgba(255, 255, 255, 0.08);
  --rt-replay-progress-fill: #6366F1;

  /* 发布状态色 */
  --rt-release-success: #22C55E;
  --rt-release-pending: #F59E0B;
  --rt-release-failed: #EF4444;
  --rt-release-idle: #64748B;

  /* 控制栏 */
  --rt-control-bg: rgba(15, 23, 42, 0.92);
  --rt-control-border: rgba(255, 255, 255, 0.08);
  --rt-control-height: 72px;
}
```

---


## 2. 发布状态看板

### 2.1 看板概述

发布状态看板是一个轻量级的发布追踪 UI，嵌入 WebViewer 或作为独立页面。当开发者推送 `v*` tag 后，可在此查看三渠道（PyPI / ClawHub / GitHub Pages）的发布进度。

> **设计定位**：这不是一个独立的管理后台，而是 WebViewer 顶栏的一个入口（⚙️ 发布状态），点击展开看板面板。

### 2.2 入口与触发

```
┌─────────────────────────────────────────────────────┐
│ [TOP BAR]  🟢 LIVE  主题标题  👥  ⏱  📦 v0.2.0 发布中  │
└─────────────────────────────────────────────────────┘
                            ↑
                    点击展开发布看板
```

| 属性 | 值 | 说明 |
|------|------|------|
| 入口位置 | 顶栏右侧，分享按钮左侧 | 仅当有进行中/最近发布时显示 |
| 入口图标 | 📦 | 后接版本号 + 状态摘要 |
| 入口文字色 | 发布中 `var(--rt-release-pending)` / 成功 `var(--rt-release-success)` / 失败 `var(--rt-release-failed)` | 状态驱动 |
| 入口字号 | 13px | 低调不抢主视觉 |
| 展开方式 | 点击后向下展开面板（`slideDown 300ms`） | 再次点击收起 |

### 2.3 看板面板结构

```
┌─────────────────────────────────────────────────────────┐
│  📦 Release v0.2.0                        2 分钟前 触发 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ✓ 版本一致性检查                    通过  0:03   │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ ✓ 构建 sdist + wheel                通过  0:12   │   │
│  ├─────────────────────────────────────────────────┤   │
│  │                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ 🐍 PyPI  │  │ 🦀 Claw  │  │ 📄 Pages │       │   │
│  │  │  ✅ 完成  │  │  🔄 进行中│  │  ⏳ 等待  │       │   │
│  │  │  0:25    │  │  ...     │  │          │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘       │   │
│  │                                                   │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ ⏳ 创建 GitHub Release              等待中       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  📜 历史发布                                            │
│  v0.1.0  ✅ 全部成功   3 天前                           │
│  v0.1.1  ⚠️ Pages 失败  1 天前（已修复）                │
└─────────────────────────────────────────────────────────┘
```

### 2.4 状态指示器

每个渠道/步骤使用统一的四态指示器：

| 状态 | 图标 | 颜色 | 动画 |
|------|------|------|------|
| **等待中** | `⏳` | `var(--rt-release-idle)` #64748B | 无 |
| **进行中** | `🔄` | `var(--rt-release-pending)` #F59E0B | 旋转 `spin 1s linear infinite` |
| **成功** | `✅` | `var(--rt-release-success)` #22C55E | 弹入 `bounceIn 300ms` |
| **失败** | `❌` | `var(--rt-release-failed)` #EF4444 | 震动 `shake 400ms` |

**CSS**：
```css
.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
}

.status-indicator[data-status="pending"]  { color: var(--rt-release-idle); }
.status-indicator[data-status="running"]  { color: var(--rt-release-pending); }
.status-indicator[data-status="success"]  { color: var(--rt-release-success); }
.status-indicator[data-status="failed"]   { color: var(--rt-release-failed); }

.status-indicator[data-status="running"] .status-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

@keyframes bounceIn {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25%      { transform: translateX(-3px); }
  75%      { transform: translateX(3px); }
}
```

### 2.5 渠道卡片

三个渠道并排显示（桌面端），移动端改为纵向堆叠。

| 属性 | 值 |
|------|------|
| 背景 | `var(--rt-bg-card)` #1E293B |
| 边框 | 1px solid `var(--rt-border)` #334155 |
| 圆角 | `var(--rt-radius-md)` 10px |
| 内边距 | 16px |
| 最小宽度 | 140px |
| 间距 | 12px |
| 布局 | Flexbox，`justify-content: center`，`gap: 12px` |

**渠道卡片结构**：
```html
<div class="channel-card" data-channel="pypi" data-status="success">
  <div class="channel-icon">🐍</div>
  <div class="channel-name">PyPI</div>
  <div class="channel-status">
    <span class="status-icon">✅</span>
    <span class="status-text">完成</span>
  </div>
  <div class="channel-time">0:25</div>
</div>
```

| 渠道 | 图标 | 说明 |
|------|------|------|
| PyPI | 🐍 | Python 包索引 |
| ClawHub | 🦀 | ClawHub 生态 |
| GitHub Pages | 📄 | 文档站点 |

### 2.6 进度总览条

看板顶部标题下方显示一条整体进度条，反映全链路完成度。

```
████████████████░░░░░░░░░░░░░  5/7 步骤完成
```

| 属性 | 值 |
|------|------|
| 高度 | 3px |
| 圆角 | 999px |
| 背景轨道 | `var(--rt-replay-progress-track)` |
| 填充色 | `var(--rt-release-success)`（全成功时）/ `var(--rt-release-pending)`（进行中）/ `var(--rt-release-failed)`（有失败） |
| 过渡动画 | `width 0.6s ease-out` |
| 位置 | 标题栏下方，内容区上方 |

### 2.7 历史发布列表

面板底部展示最近 5 条发布记录，按时间倒序。

| 属性 | 值 |
|------|------|
| 每行高度 | 40px |
| 版本号 | 14px `font-weight: 600`，`var(--rt-text-primary)` |
| 状态标签 | 胶囊形，12px，颜色同状态指示器 |
| 时间 | 13px，`var(--rt-text-muted)` |
| 分割线 | `1px solid var(--rt-border)` |

**状态标签**：
- ✅ 全部成功 — 绿底
- ⚠️ 部分失败 — 黄底
- ❌ 发布失败 — 红底

### 2.8 失败回滚入口

当某渠道发布失败时，卡片底部出现「回滚」操作按钮：

| 属性 | 值 |
|------|------|
| 按钮文字 | `回滚此版本` |
| 样式 | 红色描边按钮（`border: 1px solid #EF4444`，文字 `#EF4444`） |
| 点击行为 | 弹出确认对话框，显示回滚步骤（参考 PRD §11.2 Runbook） |
| 确认对话框 | Modal，暗色底，红边框警告样式 |

---


## 3. 讨论回放播放器

### 3.1 回放入口

讨论状态为 `concluded` 时，WebViewer 页面显示「回放讨论」入口。

**入口位置**：讨论结束后，在最终总结卡片下方出现。

```
┌─────────────────────────────────────────────────────┐
│  ┌─ 🎯 讨论总结（Sprint 1 已有）──────────────────┐ │
│  │  💡 结论：采用 FastAPI 重写核心模块...          │ │
│  │  ■ 全部共识 (3)  ■ 全部分歧 (1)                │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
│  ┌─────────────────────────────────────────────────┐│
│  │         🎬 回放讨论全过程                        ││
│  │         36 段发言 · 3 轮讨论 · 05:40            ││
│  │         [Alice] [Bob] [Carol]                   ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

| 属性 | 值 |
|------|------|
| 背景 | `var(--rt-replay-accent-glow)` rgba(99,102,241,0.08) |
| 边框 | 1.5px dashed `var(--rt-replay-accent)` #6366F1 |
| 圆角 | `var(--rt-radius-lg)` 16px |
| 内边距 | 24px |
| 图标 | 🎬，32px |
| 标题 | 18px，`font-weight: 600`，`var(--rt-text-primary)` |
| 元信息 | 13px，`var(--rt-text-muted)`，`36 段发言 · 3 轮讨论 · 05:40` |
| Agent 头像行 | 小头像 24×24px 水平排列，间距 -8px（重叠效果） |
| 悬浮态 | 边框变为实线，背景加深 `rgba(99,102,241,0.14)`，`box-shadow: 0 0 20px var(--rt-replay-accent-glow)` |
| 点击行为 | 进入回放模式，页面切换到回放视图 |

**CSS**：
```css
.replay-entry {
  background: rgba(99, 102, 241, 0.08);
  border: 1.5px dashed var(--rt-replay-accent);
  border-radius: var(--rt-radius-lg);
  padding: 24px;
  margin-top: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.replay-entry:hover {
  border-style: solid;
  background: rgba(99, 102, 241, 0.14);
  box-shadow: 0 0 20px var(--rt-replay-accent-glow);
}

.replay-entry-icon { font-size: 32px; margin-bottom: 8px; }
.replay-entry-title { font-size: 18px; font-weight: 600; color: var(--rt-text-primary); }
.replay-entry-meta { font-size: 13px; color: var(--rt-text-muted); margin-top: 4px; }
```

### 3.2 回放模式整体布局

进入回放模式后，页面布局变为专用的回放视图：

```
┌─────────────────────────────────────────────────────┐
│ [TOP BAR]  ◀ 返回   🎬 回放 — FastAPI vs Flask    1x ▾│
├─────────────────────────────────────────────────────┤
│                                                     │
│  [timeline-strip] 第 1 轮 · · · 第 2 轮 · · · 第 3 轮 │
│                                                     │
│  ┌─ Alice (蓝边) ─────────────────────────────────┐ │
│  │ 🤖 Alice (GPT-4o)                    10:23    │ │
│  │ 我认为 FastAPI 的性能优势在 IO 密集场景下...    │ │
│  └────────────────────────────────────────────────┘ │
│  ┌─ Bob (紫边) ───────────────────────────────────┐ │
│  │ 🧠 Bob (Claude)                      10:24    │ │
│  │ 同意 Alice 的观点。但需要注意 FastAPI 的...     │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
│  ┏━━ 第 1 轮 观点总结 ━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃ ✅ FastAPI 性能优势明确  ⚠️ 迁移成本需评估    ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                     │
│  ┌─ Carol (绿边) ─────────────────────────────────┐ │
│  │ 💻 Carol (GPT-4o)                      10:25  │ │
│  │ 从工程角度，我认为应该先从 API 层开始...     ▊ │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐│
│  │  ▶  ━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━  12/36 段  ││
│  │  01:23 / 05:40    第 1 轮 / 共 3 轮    [1x ▾]  ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

**与实时模式的差异**：

| 维度 | 实时模式 | 回放模式 |
|------|---------|---------|
| 底色 | `#0F172A` | `--rt-replay-bg` #0D1525（更深） |
| 顶栏 | LIVE 徽章 + 元信息 | 返回按钮 + 回放标题 + 速度选择 |
| 气泡边框 | 角色色实线 | 角色色半透明（`opacity: 0.6`） |
| 打字光标 | 标准闪烁 | 播放中闪烁，暂停时静止 |
| 新增元素 | 无 | 时间轴条 + 底部控制栏 |
| 自动滚动 | 持续 | 仅播放时 |

### 3.3 时间轴条（Timeline Strip）

顶栏下方的紧凑时间轴，展示讨论的轮次结构和当前播放位置。

```
┌──────────────────────────────────────────────────────┐
│  ◉ 第 1 轮    ● ● ● ●    ◉ 第 2 轮    ● ● ●    ◉ 第 3 轮  │
│                    ↑ 当前位置                         │
└──────────────────────────────────────────────────────┘
```

| 属性 | 值 |
|------|------|
| 高度 | 32px |
| 背景 | `rgba(255,255,255,0.03)` |
| 轮次节点 | 圆形 10px，`var(--rt-replay-accent)` 填充 |
| 发言节点 | 小圆点 5px，`var(--rt-border)` #334155 |
| 已播放发言 | `var(--rt-replay-accent)` 填充 |
| 当前发言 | 放大到 7px + 辉光 `box-shadow: 0 0 8px var(--rt-replay-accent-glow)` |
| 连接线 | 1px `var(--rt-border)` 水平线连接各节点 |
| 交互 | 点击发言节点跳转到对应位置 |

**CSS**：
```css
.timeline-strip {
  display: flex;
  align-items: center;
  height: 32px;
  padding: 0 16px;
  background: rgba(255, 255, 255, 0.03);
  overflow-x: auto;
  gap: 0;
  -webkit-overflow-scrolling: touch;
}

.timeline-node {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--rt-border);
  transition: all 0.3s ease;
  cursor: pointer;
  flex-shrink: 0;
}

.timeline-node.round-marker {
  width: 10px;
  height: 10px;
  background: var(--rt-replay-accent);
}

.timeline-node.played {
  background: var(--rt-replay-accent);
}

.timeline-node.current {
  width: 7px;
  height: 7px;
  background: var(--rt-replay-accent);
  box-shadow: 0 0 8px var(--rt-replay-accent-glow);
}

.timeline-connector {
  flex: 1;
  min-width: 12px;
  height: 1px;
  background: var(--rt-border);
}
```

---


### 3.4 回放控制栏（Control Bar）

固定在页面底部的播放控制栏，类似视频播放器。

```
┌─────────────────────────────────────────────────────────┐
│  ▶  ━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━  12/36 段  │
│  01:23 / 05:40          第 1 轮 / 共 3 轮         1x ▾  │
└─────────────────────────────────────────────────────────┘
```

#### 3.4.1 控制栏整体

| 属性 | 值 |
|------|------|
| 定位 | `fixed`，`bottom: 0` |
| z-index | 200 |
| 背景 | `var(--rt-control-bg)` rgba(15,23,42,0.92) + `backdrop-filter: blur(16px)` |
| 顶部边框 | 1px solid `var(--rt-control-border)` |
| 高度 | `var(--rt-control-height)` 72px（双行布局） |
| 内边距 | 12px 20px |
| 阴影 | `0 -4px 20px rgba(0,0,0,0.3)` |

**CSS**：
```css
.replay-control-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--rt-control-height);
  background: var(--rt-control-bg);
  backdrop-filter: blur(16px);
  border-top: 1px solid var(--rt-control-border);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.3);
  padding: 12px 20px;
  z-index: 200;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
```

#### 3.4.2 进度条（第一行）

进度条占据控制栏第一行，可拖拽跳转。

| 属性 | 值 |
|------|------|
| 轨道高度 | 4px（悬浮/拖拽时扩展到 6px） |
| 轨道圆角 | 999px |
| 轨道背景 | `var(--rt-replay-progress-track)` rgba(255,255,255,0.08) |
| 已播放填充 | `var(--rt-replay-accent)` #6366F1 |
| 缓冲指示 | `rgba(255,255,255,0.12)`，在已播放后面 |
| 拖拽手柄 | 圆形 12px，`var(--rt-replay-accent)` 填充 + 白色边框 |
| 手柄悬浮态 | 放大到 16px + 辉光 |
| 段落标记 | 小竖线 2px 高，表示每段发言的起始位置，`rgba(255,255,255,0.15)` |
| 进度文字 | 右侧 `12/36 段`，12px，`var(--rt-text-muted)` |

**交互行为**：
- 拖拽时进度条高度扩展到 6px，手柄放大
- 拖拽中实时预览缩略信息（段落摘要 tooltip）
- 松手后跳转到目标位置，清除已有气泡并从目标位置重新播放
- 段落标记悬浮时显示 `第 N 段 · Agent 名称` tooltip

**CSS**：
```css
.replay-progress-track {
  width: 100%;
  height: 4px;
  background: var(--rt-replay-progress-track);
  border-radius: 999px;
  position: relative;
  cursor: pointer;
  transition: height 0.2s ease;
}

.replay-progress-track:hover,
.replay-progress-track.dragging {
  height: 6px;
}

.replay-progress-fill {
  height: 100%;
  background: var(--rt-replay-accent);
  border-radius: 999px;
  transition: width 0.1s linear;
}

.replay-progress-handle {
  position: absolute;
  top: 50%;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--rt-replay-accent);
  border: 2px solid #fff;
  transform: translate(-50%, -50%);
  transition: width 0.2s, height 0.2s;
  box-shadow: 0 0 0 0 transparent;
}

.replay-progress-track:hover .replay-progress-handle {
  width: 16px;
  height: 16px;
  box-shadow: 0 0 10px var(--rt-replay-accent-glow);
}

.replay-segment-marker {
  position: absolute;
  top: 0;
  width: 2px;
  height: 100%;
  background: rgba(255, 255, 255, 0.15);
  pointer-events: none;
}
```

#### 3.4.3 控制按钮（第二行）

第二行左侧为播放控制，中间为进度信息，右侧为速度选择。

| 元素 | 属性 | 值 |
|------|------|------|
| 播放/暂停按钮 | 尺寸 | 36×36px |
| | 圆角 | 50%（圆形） |
| | 背景 | `var(--rt-replay-accent)` |
| | 图标色 | 白色，18px |
| | 悬浮态 | `brightness(1.1)` + `box-shadow: 0 0 12px var(--rt-replay-accent-glow)` |
| 进度文字 | 字号 | 13px |
| | 颜色 | `var(--rt-text-muted)` |
| | 格式 | `01:23 / 05:40` |
| 轮次信息 | 字号 | 12px |
| | 颜色 | `var(--rt-text-muted)` |
| | 格式 | `第 N 轮 / 共 M 轮` |
| 速度选择 | 样式 | 下拉菜单或 Segmented control |
| | 选项 | `1x` `2x` `4x` |
| | 当前值 | `var(--rt-replay-accent)` 背景 + 白色文字 |
| | 字号 | 12px |

**布局 CSS**：
```css
.replay-controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.replay-play-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--rt-replay-accent);
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.replay-play-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 12px var(--rt-replay-accent-glow);
}

.replay-time-info {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: var(--rt-text-muted);
}

.replay-speed-selector {
  display: inline-flex;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.replay-speed-btn {
  padding: 4px 10px;
  font-size: 12px;
  color: var(--rt-text-muted);
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.replay-speed-btn.active {
  background: var(--rt-replay-accent);
  color: #fff;
}
```

### 3.5 回放气泡样式

回放模式下的发言气泡与实时模式有微妙但明确的视觉区分。

#### 3.5.1 气泡状态

| 状态 | 视觉表现 | 说明 |
|------|---------|------|
| **未播放** | 不显示 | 气泡尚未出现在 DOM 中 |
| **正在播放** | 左侧角色色边框 + 辉光 + 打字光标 | 与实时模式一致，沉浸感 |
| **已播放** | 左侧边框 `opacity: 0.35`，正文 `opacity: 0.85` | 视觉降权，引导焦点到当前发言 |
| **暂停中** | 光标静止（不闪烁），其余保持 | 明确提示「暂停」状态 |

#### 3.5.2 回放气泡 vs 实时气泡

| 属性 | 实时气泡 | 回放气泡 |
|------|---------|---------|
| 左侧边框 | 3px solid `{agent-color}` | 3px solid `{agent-color}`（同） |
| 正在发言辉光 | `box-shadow: -4px 0 16px {color}25` | 同实时（一致的沉浸感） |
| 已播放态边框 | N/A | `opacity: 0.35`，过渡 0.5s |
| 已播放态正文 | N/A | `opacity: 0.85`，过渡 0.5s |
| 时间戳 | 显示 | 显示 + 淡化（回放模式时间不是重点） |
| 完成标记 ✓ | 200ms 延迟出现 | 即时出现（无需等待感） |
| 气泡入场 | `fadeSlideIn 300ms` | 同实时（保持一致性） |

**CSS**：
```css
/* 回放模式 · 已播放态 */
.replay-mode .speech-card[data-replay-state="played"] {
  transition: all 0.5s ease-out;
}

.replay-mode .speech-card[data-replay-state="played"] .speech-border {
  opacity: 0.35;
}

.replay-mode .speech-card[data-replay-state="played"] .speech-text {
  opacity: 0.85;
}

/* 回放模式 · 暂停时光标静止 */
.replay-mode.paused .typing-cursor {
  animation: none;
  opacity: 1;
}
```

#### 3.5.3 回放中的观点卡片

回放模式下的轮次总结/最终总结卡片沿用 Sprint 1 规范，但增加回放特有样式：

| 属性 | 值 |
|------|------|
| 入场动画 | 与实时模式一致（`fadeSlideIn`） |
| 边框 | 沿用 Sprint 1 的品牌靛蓝边框 |
| 回放特有 | 卡片右上角显示轮次时间戳（`10:25`，12px，`var(--rt-text-muted)`） |
| 已播放态 | 整卡 `opacity: 0.8` |

---


## 4. 讨论列表页

### 4.1 列表概述

讨论列表页是回放功能的入口之一，展示所有历史讨论，用户可以选择任意一场进行回放。

**入口位置**：WebViewer 顶栏左侧增加「📜 讨论列表」导航（或底部 Tab 切换）。

### 4.2 页面布局

```
┌─────────────────────────────────────────────────────┐
│  📜 历史讨论                           [搜索] [筛选] │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                     │
│  ┌─────────────────────────────────────────────────┐│
│  │ 🎬 FastAPI vs Flask 技术选型                    ││
│  │                                                 ││
│  │  🤖 🧠 💻  Alice · Bob · Carol                 ││
│  │                                                 ││
│  │  3 轮讨论  ·  36 段发言  ·  05:40              ││
│  │  2026-05-26 14:30                               ││
│  │                                                 ││
│  │  📊 收敛度 ████████████████░░░░  78%           ││
│  │                                                 ││
│  │                           [🎬 回放]  [📋 总结]  ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
│  ┌─────────────────────────────────────────────────┐│
│  │ 🎬 AI Agent 协作模式探讨                        ││
│  │                                                 ││
│  │  🤖 🧠  Dave · Eve                              ││
│  │                                                 ││
│  │  2 轮讨论  ·  18 段发言  ·  03:20              ││
│  │  2026-05-25 10:00                               ││
│  │                                                 ││
│  │  📊 收敛度 ██████████████████████  92%          ││
│  │                                                 ││
│  │                           [🎬 回放]  [📋 总结]  ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
│  ┌─────────────────────────────────────────────────┐│
│  │ 🟢 多模态 AI 的未来方向              进行中     ││
│  │                                                 ││
│  │  🤖 🧠 💻 📊  Alice · Bob · Carol · Dave      ││
│  │                                                 ││
│  │  第 2 轮进行中  ·  已发言 12 段                 ││
│  │  2026-05-26 16:00                               ││
│  │                                                 ││
│  │                           [👁 实时观看]          ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.3 讨论卡片规格

| 属性 | 值 |
|------|------|
| 背景 | `var(--rt-bg-card)` #1E293B |
| 边框 | 1px solid `var(--rt-border)` #334155 |
| 圆角 | `var(--rt-radius-lg)` 16px |
| 内边距 | 20px |
| 卡片间距 | 12px |
| 最大宽度 | 720px（与内容区一致） |

#### 卡片元素

| 元素 | 属性 | 说明 |
|------|------|------|
| 讨论标题 | 16px `font-weight: 600`，`var(--rt-text-primary)` | 最多 2 行，超出省略 |
| Agent 头像行 | 小头像 24×24px，重叠排列 `-8px margin` | 展示参与者 |
| Agent 名称 | 13px，`var(--rt-text-muted)` | `Alice · Bob · Carol` |
| 元信息 | 13px，`var(--rt-text-muted)` | `3 轮讨论 · 36 段发言 · 05:40` |
| 时间戳 | 13px，`var(--rt-text-muted)` | `2026-05-26 14:30` |
| 收敛度条 | 沿用 Sprint 1 的收敛度进度条规范 | `78%` |
| 操作按钮 | 右下角，13px 按钮 | 回放 / 总结 / 实时观看 |

#### 讨论状态

| 状态 | 图标 | 标签色 | 操作按钮 |
|------|------|--------|---------|
| **concluded** | 🎬 | 无标签 | `[🎬 回放]` + `[📋 总结]` |
| **active** | 🟢 | 绿色标签「进行中」 | `[👁 实时观看]` |
| **failed** | ❌ | 红色标签「已中断」 | `[📋 查看已有]` |

### 4.4 搜索与筛选

列表页顶部提供轻量级搜索和筛选：

| 功能 | 实现 | 说明 |
|------|------|------|
| 搜索 | 文本输入框，placeholder「搜索讨论主题...」 | 前端模糊匹配 |
| 状态筛选 | Segmented control：`全部` `已完成` `进行中` | 默认「全部」 |
| 排序 | 下拉：`最新优先` `最长优先` `收敛度最高` | 默认「最新优先」 |

| 属性 | 值 |
|------|------|
| 搜索框 | 圆角 10px，`var(--rt-bg-card)` 底色，`var(--rt-border)` 边框 |
| 搜索图标 | 🔍，14px，`var(--rt-text-muted)` |
| 筛选器间距 | 8px，与搜索框同行排列 |

### 4.5 空状态

当没有历史讨论时，显示空状态：

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                  🎭                                  │
│          还没有历史讨论                              │
│                                                     │
│     开始一场圆桌讨论，结束后这里会显示回放入口       │
│                                                     │
│              [🚀 开始讨论]                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| 属性 | 值 |
|------|------|
| 图标 | 🎭，48px |
| 标题 | 16px，`var(--rt-text-muted)` |
| 说明 | 14px，`var(--rt-text-muted)` |
| CTA 按钮 | 品牌色填充按钮 |

---

## 5. 回放进度指示器

### 5.1 进度信息层级

回放模式中，进度信息分布在三个位置，形成从概览到细节的三级信息层级：

| 层级 | 位置 | 信息 | 字号 |
|------|------|------|------|
| **L1 总览** | 顶栏右侧 | 当前段数 / 总段数 `12/36 段` | 13px |
| **L2 时间轴** | 顶栏下方 | 轮次结构 + 当前播放位置 | 见 §3.3 |
| **L3 控制栏** | 底部固定 | 时间 + 轮次 + 速度 | 12-13px |

### 5.2 段数指示

```
12 / 36 段
```

| 属性 | 值 |
|------|------|
| 当前段数 | `var(--rt-replay-accent)`，`font-weight: 600` |
| 分隔符 | `/`，`var(--rt-text-muted)` |
| 总段数 | `var(--rt-text-muted)` |
| 后缀 | `段`，`var(--rt-text-muted)` |
| 更新时机 | 每播放完一段后更新 |
| 过渡动画 | 数字变化时微弹效果 `scale(1.05)` → `scale(1)`，200ms |

### 5.3 轮次指示

```
第 1 轮 / 共 3 轮
```

| 属性 | 值 |
|------|------|
| 格式 | `第 N 轮 / 共 M 轮` |
| 当前轮次 | `var(--rt-text-primary)`，`font-weight: 500` |
| 总轮次 | `var(--rt-text-muted)` |
| 轮次切换 | 进入新轮次时，文字短暂高亮为 `var(--rt-replay-accent)`，500ms 后恢复 |

### 5.4 时间显示

```
01:23 / 05:40
```

| 属性 | 值 |
|------|------|
| 格式 | `MM:SS / MM:SS` |
| 当前时间 | `var(--rt-text-primary)` |
| 总时长 | `var(--rt-text-muted)` |
| 计算方式 | 基于已播放的 token 时间戳差值 |
| 更新频率 | 每秒更新一次 |

---


## 6. 移动端适配与响应式

### 6.1 回放模式响应式断点

延续 Sprint 1 的断点体系，Sprint 2 回放模式在移动端做以下调整：

| 断点 | 调整 |
|------|------|
| `≤768px`（手机） | 控制栏高度缩减为 60px；进度条触摸区域扩大（上下各 +8px padding）；速度选择器改为下拉菜单；时间轴条隐藏，仅保留轮次文字；讨论列表卡片内边距 16px |
| `≤480px`（小手机） | 控制栏改为单行布局（播放按钮 + 进度条 + 速度）；时间/轮次信息合并为一行；讨论列表卡片全宽 |
| `prefers-reduced-motion: reduce` | 回放时无逐字动画，直接显示完整段落；进度条无过渡动画 |

### 6.2 控制栏移动端布局

**桌面端（>768px）**：双行，进度条 + 控制按钮
**手机端（≤768px）**：进度条全宽 + 单行控制按钮

```
手机端控制栏：
┌──────────────────────────────────────┐
│  ━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━   │  ← 进度条（触摸友好）
│  ▶  01:23/05:40  1/3轮        1x ▾  │  ← 单行控制
└──────────────────────────────────────┘
```

| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 控制栏高度 | 72px | 60px |
| 进度条触摸区 | 4px 轨道 | 上下各 +8px padding（总触摸高度 20px） |
| 播放按钮 | 36×36px | 32×32px |
| 速度选择器 | Segmented control | 下拉菜单（点击展开） |
| 时间信息 | 独立行 | 与播放按钮同行 |

**移动端 CSS**：
```css
@media (max-width: 768px) {
  .replay-control-bar {
    height: 60px;
    padding: 8px 16px;
  }

  .replay-progress-track {
    padding: 8px 0;
    margin: -8px 0;
  }

  .replay-controls-row {
    gap: 8px;
  }

  .replay-play-btn {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .replay-speed-selector {
    position: relative;
  }

  .replay-speed-dropdown {
    position: absolute;
    bottom: 100%;
    right: 0;
    background: var(--rt-control-bg);
    border: 1px solid var(--rt-border);
    border-radius: 8px;
    padding: 4px;
    margin-bottom: 8px;
    display: none;
  }

  .replay-speed-dropdown.open {
    display: block;
  }

  .timeline-strip {
    display: none; /* 移动端隐藏时间轴条 */
  }
}
```

### 6.3 讨论列表移动端

| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 卡片间距 | 12px | 8px |
| 内边距 | 20px | 16px |
| 操作按钮 | 卡片右下角 | 卡片底部全宽 |
| 搜索+筛选 | 同行排列 | 搜索框全宽，筛选器换行 |

### 6.4 触摸手势

| 手势 | 区域 | 行为 |
|------|------|------|
| 点击 | 气泡区域 | 无特殊行为（沿用默认） |
| 左滑 | 讨论列表卡片 | 露出「回放」快捷操作 |
| 点击+长按 | 进度条 | 显示段落预览 tooltip |
| 拖拽 | 进度条手柄 | 跳转到目标位置 |

### 6.5 页面底部留白

回放模式下，由于控制栏 fixed 定位，内容区底部需要额外留白：

| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 底部留白 | `calc(var(--rt-control-height) + 20px)` = 92px | `calc(60px + 16px)` = 76px |

---

## 7. 断点续播与本地状态

### 7.1 本地存储策略

回放进度通过 `localStorage` 持久化，支持断点续播。

**存储 Key 设计**：
```
Key: rt-replay-{discussion_id}
Value: JSON {
  "speechIndex": 12,        // 当前播放到第几段
  "timestamp": 1779761742,  // 存储时间
  "speed": 1                // 播放速度
}
```

### 7.2 恢复流程

用户再次打开回放页面时：

```
页面加载
  │
  ▼
检查 localStorage 有无 rt-replay-{id}
  │
  ├─ 有 → 显示「继续从上次位置播放？」提示条
  │       ┌─────────────────────────────────────────┐
  │       │  ⏸ 上次播放到第 12/36 段 (01:23)       │
  │       │     [继续播放]  [从头开始]  [✕]         │
  │       └─────────────────────────────────────────┘
  │
  └─ 无 → 从头开始播放
```

| 属性 | 值 |
|------|------|
| 提示条背景 | `var(--rt-replay-accent-glow)` rgba(99,102,241,0.12) |
| 提示条边框 | 1px solid `var(--rt-replay-accent)` |
| 提示条位置 | 内容区顶部，sticky |
| 自动消失 | 10 秒后自动消失（默认从头开始） |
| 「继续播放」 | 品牌色填充按钮 |
| 「从头开始」 | 文字按钮，`var(--rt-text-muted)` |

---


## 8. 组件清单与交付物

### 8.1 Sprint 2 新增组件

| # | 组件 | 优先级 | 所属功能 | 状态 |
|---|------|--------|---------|------|
| 1 | 回放入口卡片（`.replay-entry`） | P1 | 讨论回放 | 待开发 |
| 2 | 时间轴条（`.timeline-strip`） | P1 | 讨论回放 | 待开发 |
| 3 | 回放控制栏（`.replay-control-bar`） | P1 | 讨论回放 | 待开发 |
| 4 | 进度条（`.replay-progress-track`） | P1 | 讨论回放 | 待开发 |
| 5 | 播放/暂停按钮（`.replay-play-btn`） | P1 | 讨论回放 | 待开发 |
| 6 | 速度选择器（`.replay-speed-selector`） | P1 | 讨论回放 | 待开发 |
| 7 | 段数/轮次指示器 | P1 | 讨论回放 | 待开发 |
| 8 | 续播提示条 | P1 | 讨论回放 | 待开发 |
| 9 | 讨论列表卡片（`.discussion-card`） | P1 | 讨论回放 | 待开发 |
| 10 | 讨论列表搜索/筛选 | P1 | 讨论回放 | 待开发 |
| 11 | 发布状态看板面板 | P0 | 发布自动化 | 待开发 |
| 12 | 渠道状态卡片（`.channel-card`） | P0 | 发布自动化 | 待开发 |
| 13 | 进度总览条 | P0 | 发布自动化 | 待开发 |
| 14 | 历史发布列表 | P0 | 发布自动化 | 待开发 |
| 15 | 回滚确认对话框 | P0 | 发布自动化 | 待开发 |

### 8.2 Sprint 1 组件复用

以下 Sprint 1 组件在回放模式中复用，仅需增加回放状态适配：

| 组件 | 复用方式 | 修改点 |
|------|---------|--------|
| 流式发言气泡（`.speech-card`） | 回放模式直接复用 | 增加 `data-replay-state` 属性支持已播放态 |
| 打字光标（`.typing-cursor`） | 回放模式直接复用 | 暂停时不闪烁 |
| 完成标记（`.speech-checkmark`） | 回放模式直接复用 | 无延迟出现 |
| 轮次观点卡片（`.summary-card`） | 回放模式直接复用 | 增加时间戳显示 |
| 最终总结卡片（`.summary-card.final`） | 回放模式直接复用 | 呼吸辉光改为播放时才触发 |
| 收敛度进度条（`.convergence-bar`） | 讨论列表卡片中复用 | 无修改 |
| 自动滚动 | 回放模式复用 | 仅播放时启用 |

### 8.3 设计交付物清单

| # | 交付物 | 说明 | 状态 |
|---|--------|------|------|
| 1 | 回放播放器组件规范 | 控制栏布局、进度条样式、速度切换 | ✅ 本文档 §3 |
| 2 | 回放气泡样式 | 与实时模式的视觉区分 | ✅ 本文档 §3.5 |
| 3 | 讨论列表页规范 | 卡片布局、搜索筛选 | ✅ 本文档 §4 |
| 4 | 回放进度指示器 | 段数/轮次展示 | ✅ 本文档 §5 |
| 5 | 移动端回放适配 | 控制栏收缩、触摸手势 | ✅ 本文档 §6 |
| 6 | 发布状态看板规范 | 渠道状态、历史记录 | ✅ 本文档 §2 |
| 7 | 断点续播规范 | 本地存储、恢复流程 | ✅ 本文档 §7 |
| 8 | DESIGN-sprint2.md（本文件） | 完整设计规范 | ✅ |

### 8.4 验收对照表

对照 PRD §7 验收标准的设计侧检查：

| PRD 验收项 | 设计覆盖 | 文档位置 |
|-----------|---------|---------|
| B1 回放入口 | 回放入口卡片 | §3.1 |
| B2 逐段播放 | 回放气泡逐字流式 | §3.5 |
| B3 播放控制 | 播放/暂停按钮 | §3.4.3 |
| B4 进度条 | 可拖拽进度条 | §3.4.2 |
| B5 速度控制 | 1x/2x/4x 速度选择器 | §3.4.3 |
| B6 讨论列表 | 讨论列表页 | §4 |
| B7 断点续播 | localStorage + 续播提示 | §7 |
| B8 移动端适配 | 响应式断点 + 触摸手势 | §6 |
| A7 发布看板 | 发布状态看板面板 | §2 |

---

*本文档由像素姐（设计总监）编写，配合饼哥 Sprint 2 PRD 产出。如有疑问请联系设计负责人。* 🎨

