# agent-roundtable v2 Sprint 1 设计规范

> **设计师**：像素姐 🎨 | **日期**：2026-05-26
> **分支**：feature/v2-ux-improvements
> **关联 PRD**：docs/product/PRD-sprint1.md

---

## 1. 概述与设计原则

### 1.1 设计目标

Sprint 1 为 agent-roundtable WebViewer 带来两项核心体验升级：

1. **流式输出**：Agent 发言从"整段突现"变为"逐字流出"，让讨论过程有实时思考的沉浸感
2. **观点提炼**：协调者的核心观点从发言流中独立出来，以卡片形式突出展示

### 1.2 设计原则

| 原则 | 说明 |
|------|------|
| **渐进呈现** | 信息按时间节奏逐步展示，不一次性淹没用户 |
| **角色可辨** | 每个 Agent 视觉上清晰可区分，头像+色彩双重标识 |
| **焦点明确** | 正在发言的 Agent 最突出，历史发言自然弱化 |
| **流畅过渡** | 状态切换（打字中→完成→新发言）全有动画衔接 |
| **移动友好** | 微信内置浏览器优先，触摸友好，无横向滚动 |

### 1.3 设计语言沿用

延续已有的 `theme.css` 设计体系：
- **色彩**：Dark Slate 底色（`#0F172A`）+ 角色色标识
- **圆角**：小 6px / 中 10px / 大 16px
- **字体**：系统字体栈（PingFang SC + SF Pro）
- **动效**：`cubic-bezier(0.4, 0, 0.2, 1)` 缓动曲线
- **间距**：4px 网格基准

---

## 2. 流式气泡组件规范

### 2.1 气泡结构

每个发言气泡由以下元素组成：

```
┌─────────────────────────────────────────────────────┐
│  [头像]  Agent 名称  [角色徽章]       [时间]        │
│                                                     │
│  发言正文内容，支持 Markdown 实时渲染...              │
│  █ (打字光标)                                       │
│                                                     │
│                                      [完成标记 ✓]   │
└─────────────────────────────────────────────────────┘
```

**DOM 结构**：
```html
<div class="speech-card" data-agent="alice" data-state="streaming">
  <div class="avatar avatar-alice">A</div>
  <div class="speech-body">
    <div class="speech-meta">
      <span class="speech-name">Alice</span>
      <span class="role-badge role-badge-product">产品</span>
      <span class="speech-time">10:23</span>
    </div>
    <div class="speech-text">
      <!-- Markdown 渲染后的 HTML -->
      <span class="typing-cursor">▊</span>
    </div>
  </div>
</div>
```

### 2.2 头像规范

| 属性 | 值 | 说明 |
|------|------|------|
| 尺寸（桌面） | 40×40px | 与现有设计一致 |
| 尺寸（移动端） | 36×36px | 节省横向空间 |
| 圆角 | 50%（圆形） | 人像/图标都用圆形 |
| 字号（首字母） | 15px / 13px | 桌面/移动端 |
| 字重 | 600 | 确保小尺寸可读 |
| 边框 | 无 | 靠底色区分 |

**头像内容**：优先使用 Agent 自定义头像图片（`avatar_url`），回退为首字母。

### 2.3 Agent 色彩分配

延续现有角色色体系，每个 Agent 分配独立色彩，用于：
- 头像背景色
- 左侧边框色（3px solid）
- 角色徽章背景+文字色

| Agent 类型 | 色值 | CSS 变量 | 头像类名 | 徽章类名 |
|-----------|------|---------|---------|---------|
| 产品型 | `#3B82F6` | `--rt-role-product` | `.avatar-product` | `.role-badge-product` |
| 设计型 | `#A855F7` | `--rt-role-design` | `.avatar-design` | `.role-badge-design` |
| 工程型 | `#22C55E` | `--rt-role-engineer` | `.avatar-engineer` | `.role-badge-engineer` |
| 研究型 | `#F59E0B` | `--rt-role-research` | `.avatar-research` | `.role-badge-research` |
| 运营型 | `#EC4899` | `--rt-role-marketing` | `.avatar-marketing` | `.role-badge-marketing` |
| 默认 | `#64748B` | `--rt-role-default` | `.avatar-default` | `.role-badge-default` |

### 2.4 气泡样式

| 属性 | 值 | 说明 |
|------|------|------|
| 背景 | `var(--rt-bg-card)` #1E293B | 统一深灰底 |
| 边框 | 1px solid `var(--rt-border)` #334155 | 默认灰色边框 |
| 左侧边框 | 3px solid `{agent-color}` | **角色色标识**，流式完成时高亮 |
| 圆角 | `var(--rt-radius-md)` 10px | 与设计体系一致 |
| 内边距 | 20px | 桌面端 |
| 内边距（移动） | 16px | 移动端 |
| 卡片间距 | 12px | 卡片之间的垂直间距 |
| 最大宽度 | 100% | 不设气泡限宽，利用 content 容器 720px |

**正在发言态**（`.speech-card[data-state="streaming"]`）：
- 左侧边框颜色 = 当前 Agent 色
- 添加微弱辉光：`box-shadow: -4px 0 16px {agent-color}25`
- 背景微亮：`var(--rt-bg-card-hover)` #334155

**完成态**（`.speech-card[data-state="done"]`）：
- 左侧边框恢复透明
- 辉光渐隐（`2s ease-out` 动画）
- 显示完成标记 ✓

### 2.5 群聊视觉效果

多个 Agent 发言时，卡片左边缘的彩色条形成视觉节奏，让用户一眼看出"谁说了多少"。

```
  ┌─ Alice (蓝边) ─────────────────┐
  │ "我认为 FastAPI 性能..."        │
  └────────────────────────────────┘
  ┌─ Bob (紫边) ───────────────────┐
  │ "同意 Alice，但需要注意..."     │
  └────────────────────────────────┘
  ┌─ Carol (绿边) ─────────────────┐
  │ "从工程角度..."               ▊ │ ← 正在流式输入
  └────────────────────────────────┘
```

---

## 3. 打字光标与动画规范

### 3.1 打字光标

| 属性 | 值 | 说明 |
|------|------|------|
| 字符 | `▊` (U+2588 FULL BLOCK) | 方块光标，经典终端风格 |
| 颜色 | `var(--rt-text-muted)` #64748B | 低调灰，不抢正文焦点 |
| 闪烁频率 | 0.8s 一个周期 | 占空比 50%（亮 0.4s / 暗 0.4s） |
| 位置 | 紧贴最后一个 token 之后 | 使用 inline 定位 |
| 消失动画 | `opacity 1→0` 持续 200ms | 柔和消失 |

**CSS 实现**：
```css
.typing-cursor {
  display: inline;
  color: var(--rt-text-muted);
  animation: cursorBlink 0.8s step-end infinite;
  opacity: 1;
}

@keyframes cursorBlink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 发言完成后光标淡出 */
.speech-card[data-state="done"] .typing-cursor {
  animation: none;
  opacity: 0;
  transition: opacity 200ms ease-out;
}
```

### 3.2 气泡入场动画

新气泡从底部渐入，与群聊消息的自然流动感一致。

| 属性 | 值 |
|------|------|
| 动画名 | `fadeSlideIn` |
| 时长 | 300ms |
| 缓动 | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 效果 | `opacity: 0→1` + `translateY: 12px→0` |

```css
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.speech-card { animation: fadeSlideIn 300ms cubic-bezier(0.4, 0, 0.2, 1) both; }
```

### 3.3 流式高亮边框动画

正在发言的气泡，左侧边框有角色色辉光，发言结束后渐隐。

```css
@keyframes highlightFade {
  0% {
    border-left-color: var(--agent-color);
    box-shadow: -4px 0 16px color-mix(in srgb, var(--agent-color) 25%, transparent);
  }
  100% {
    border-left-color: transparent;
    box-shadow: none;
  }
}
```

| 属性 | 值 |
|------|------|
| 触发时机 | `speech_end` 事件后 |
| 时长 | 2000ms |
| 缓动 | `ease-out` |
| 效果 | 左边框+辉光渐隐 |

### 3.4 完成标记

| 属性 | 值 |
|------|------|
| 符号 | `✓` |
| 颜色 | `var(--rt-text-muted)` #64748B |
| 字号 | 12px |
| 位置 | 气泡右下角，绝对定位 |
| 入场 | `fadeSlideIn` 300ms，延迟 200ms（等光标消失后） |

```css
.speech-checkmark {
  position: absolute;
  bottom: 8px;
  right: 12px;
  font-size: 12px;
  color: var(--rt-text-muted);
  opacity: 0;
  animation: fadeSlideIn 300ms 200ms ease-out forwards;
}
```

### 3.5 自动滚动行为

| 状态 | 行为 |
|------|------|
| 默认 | 新 token 到达时 `scrollTo({ top: scrollHeight, behavior: 'smooth' })` |
| 用户手动上翻 | 检测 `scrollY < scrollHeight - viewport - 50px` 时暂停自动滚动 |
| 回到底部 | 用户滚动到距底部 ≤50px 时恢复自动滚动 |
| 视觉提示 | 暂停时显示"↓ 新消息"悬浮按钮，点击回到底部 |

### 3.6 Token 节奏控制

| 属性 | 值 | 说明 |
|------|------|------|
| 渲染频率 | ≤50ms/token | PRD 要求 |
| 节流策略 | 前端 `requestAnimationFrame` 批量渲染 | 避免每 token 一次 reflow |
| 批量窗口 | 每 ~100ms 渲染一次累积的 token | 平衡流畅度与性能 |
| 代码块处理 | 代码块内 token 积攒到代码块结束后统一高亮 | 避免高亮闪烁 |

```javascript
// Token 节流渲染
let tokenBuffer = [];
let rafId = null;

function appendToken(speechId, delta) {
  tokenBuffer.push({ speechId, delta });
  if (!rafId) {
    rafId = requestAnimationFrame(flushTokens);
  }
}

function flushTokens() {
  // 按 speechId 分组，批量更新 DOM
  const grouped = groupBy(tokenBuffer, 'speechId');
  for (const [id, tokens] of Object.entries(grouped)) {
    const el = document.querySelector(`[data-speech-id="${id}"] .speech-text`);
    const text = tokens.map(t => t.delta).join('');
    appendMarkdown(el, text);  // 渐进式 Markdown 渲染
  }
  tokenBuffer = [];
  rafId = null;
  autoScroll();
}
```

### 3.7 SSE 断线重连视觉处理

| 阶段 | 视觉表现 |
|------|---------|
| 断线检测 | 正在发言的气泡光标变为 `...` 占位符（闪烁 3 个点） |
| 重连中 | 顶部出现 `⚡ 重新连接中...` 提示条，黄色底 |
| 补帧中 | 气泡内快速补齐缺失 token（无逐字动画，直接追加） |
| 恢复正常 | 提示条渐隐，光标恢复正常 |

---

## 4. 协调者观点卡片规范

### 4.1 观点卡片概述

每轮讨论结束后，协调者输出核心观点，以特殊卡片形式插入发言流。与普通发言气泡的视觉差异要足够明显——用户扫一眼就知道"这是总结"。

### 4.2 卡片结构

```
╔═══════════════════════════════════════════════════════╗
║  📋 第 1 轮 观点总结              [▸ 折叠]           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ■ 共识                                                ║
║  ┌─────────────────────────────────────────────────┐  ║
║  │ ✅ FastAPI 性能优势在 IO 密集场景明显             │  ║
║  │    [Alice ✓] [Bob ✓] [Carol ✓]                 │  ║
║  └─────────────────────────────────────────────────┘  ║
║  ┌─────────────────────────────────────────────────┐  ║
║  │ ✅ 团队熟悉 Python，学习成本可控                  │  ║
║  │    [Alice ✓] [Bob ✓]                            │  ║
║  └─────────────────────────────────────────────────┘  ║
║                                                       ║
║  ■ 分歧                                                ║
║  ┌─────────────────────────────────────────────────┐  ║
║  │ ⚠️ 是否应该全面迁移现有 Flask 代码               │  ║
║  │    [Alice 支持] [Bob 反对] [Carol 反对]         │  ║
║  └─────────────────────────────────────────────────┘  ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

### 4.3 卡片样式

| 属性 | 值 | 说明 |
|------|------|------|
| 背景 | `#1a2332`（比普通卡片深一级） | 视觉区分于普通发言 |
| 边框 | 2px solid `var(--rt-brand)` #4F46E5 | 品牌靛蓝边框，凸显重要性 |
| 圆角 | `var(--rt-radius-lg)` 16px | 比普通卡片更大的圆角 |
| 内边距 | 24px | 桌面端 |
| 阴影 | `0 0 20px rgba(79, 70, 229, 0.2)` | 微弱品牌色辉光 |
| 卡片间距 | 20px | 与上下普通气泡的间距更大 |

**CSS**：
```css
.summary-card {
  background: #1a2332;
  border: 2px solid var(--rt-brand);
  border-radius: var(--rt-radius-lg);
  padding: 24px;
  margin: 20px 0;
  box-shadow: 0 0 20px var(--rt-brand-glow);
}
```

### 4.4 收敛度进度条

每张观点卡片标题栏下方展示一条**渐变色条**，直观反映本轮讨论的收敛程度。

```
┌─────────────────────────────────────────────────┐
│  📋 第 1 轮 观点总结          [精简] [全文]  ▾  │
│  ████████████████░░░░░░░░░░  收敛度 68%         │
│  ← 共识绿 ───────────────→ ← 分歧橙 ────→      │
├─────────────────────────────────────────────────┤
```

| 属性 | 值 | 说明 |
|------|----|------|
| 高度 | 4px | 细而不碍眼 |
| 圆角 | 999px | 完全圆角 |
| 背景轨道 | `rgba(255,255,255,0.06)` | 极淡灰底 |
| 填充色 | `linear-gradient(90deg, var(--rt-success) 0%, var(--rt-warning) 100%)` | 从绿到橙 |
| 填充宽度 | `{convergence}%` | 0%-100% 动态 |
| 百分比文字 | `var(--rt-text-muted)`, 12px | 右对齐 |
| 位置 | 标题栏下方、内容区上方 | 独立一行 |
| 过渡动画 | `width 0.8s ease-out` | 数值变化时平滑过渡 |
| 边距 | `8px 0` | 与标题栏和内容区的间距 |

#### 收敛度含义

| 区间 | 颜色感知 | 含义 |
|------|----------|------|
| 80%-100% | 深绿为主 | 高度共识，仅边缘分歧 |
| 50%-79% | 绿→橙渐变 | 部分共识，有实质分歧 |
| 0%-49% | 橙色为主 | 分歧严重，需下轮聚焦 |

```css
.convergence-bar {
  height: 4px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  margin: 8px 0;
  overflow: hidden;
}

.convergence-bar-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--rt-success), var(--rt-warning));
  transition: width 0.8s ease-out;
}

.convergence-label {
  font-size: 12px;
  color: var(--rt-text-muted);
  text-align: right;
  margin-top: 2px;
}
```

### 4.5 标题栏与展示模式切换

| 属性 | 值 |
|------|----|
| 图标 | 📋 |
| 文字 | `第 N 轮 观点总结` |
| 字号 | 16px |
| 字重 | 600 |
| 颜色 | `var(--rt-text-primary)` #F1F5F9 |
| 展示模式切换 | 标题栏右侧 `[精简] [全文]` segmented control |
| 折叠按钮 | 最右侧 `▸` / `▾`，14px，可点击区域 44×44px |

#### 全文 / 精简展示模式

观点卡片支持两种展示粒度，通过标题栏 segmented control 切换：

| 模式 | 显示内容 | 适用场景 |
|------|----------|----------|
| **精简** (默认) | 核心观点标题 + 收敛度条 + 共识/分歧标签 | 快速浏览结论 |
| **全文** | 核心观点 + 支撑论据 + 反对者头像 + 支持者归属 | 深入理解推理过程 |

```
📋 第 1 轮 观点总结    [精简] [全文]    ▾
```

| 属性 | 值 |
|------|----|
| 样式 | Segmented control，圆角按钮组 |
| 默认状态 | 精简模式激活 |
| 切换动画 | 内容区高度过渡 `300ms ease-out` |
| 按钮尺寸 | 28×28px，12px 文字 |
| 激活态 | `var(--rt-brand)` 背景 + 白色文字 |
| 非激活态 | 透明背景 + `var(--rt-text-muted)` |

```css
.mode-toggle {
  display: inline-flex;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}
.mode-toggle-btn {
  padding: 4px 12px;
  font-size: 12px;
  color: var(--rt-text-muted);
  cursor: pointer;
  transition: all 0.2s;
}
.mode-toggle-btn.active {
  background: var(--rt-brand);
  color: #fff;
}
```

```css
.summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 4px 0;
  min-height: var(--rt-touch-target); /* 44px 触摸友好 */
  user-select: none;
}

.summary-header-icon { margin-right: 8px; font-size: 16px; }
.summary-header-text { font-size: 16px; font-weight: 600; }
.summary-toggle {
  font-size: 14px;
  color: var(--rt-text-muted);
  transition: transform 0.2s;
}
.summary-toggle.collapsed { transform: rotate(-90deg); }
```

### 4.6 共识条目

| 属性 | 值 |
|------|------|
| 标签 | ✅ 共识 |
| 标签颜色 | `var(--rt-success)` #22C55E |
| 标签背景 | `var(--rt-success-bg)` rgba(34, 197, 94, 0.15) |
| 核心观点文字 | 16px 加粗（`font-weight: 600`） |
| 支撑论据 | 14px 常规 |
| Agent 归属 | `[名字 ✓]` 标签，颜色同 Agent 色 |
| 条目背景 | `rgba(34, 197, 94, 0.08)` |
| 条目边框 | 1px solid `rgba(34, 197, 94, 0.2)` |
| 条目圆角 | 8px |
| 条目内边距 | 12px 16px |
| 条目间距 | 8px |

### 4.7 分歧条目

| 属性 | 值 |
|------|------|
| 标签 | ⚠️ 分歧 |
| 标签颜色 | `var(--rt-warning)` #F59E0B |
| 标签背景 | `var(--rt-warning-bg)` rgba(245, 158, 11, 0.15) |
| 核心观点文字 | 16px 加粗 |
| Agent 归属 | `[名字 支持]` / `[名字 反对]`，支持用 Agent 色，反对用 `#EF4444` |
| 反对者头像 | 在观点右侧显示反对者的 20×20px 小头像 |
| 条目背景 | `rgba(245, 158, 11, 0.08)` |
| 条目边框 | 1px solid `rgba(244, 158, 11, 0.2)` |

### 4.8 Agent 归属标签

```html
<span class="agent-tag" data-agent="alice" data-stance="support">
  Alice ✓
</span>
<span class="agent-tag" data-agent="bob" data-stance="oppose">
  Bob 反对
</span>
```

| 属性 | 值 |
|------|------|
| 字号 | 12px |
| 内边距 | 2px 8px |
| 圆角 | 999px（胶囊形） |
| 支持者背景 | `{agent-color}20` |
| 支持者文字 | `{agent-color}` |
| 反对者背景 | `rgba(239, 68, 68, 0.15)` |
| 反对者文字 | `#EF4444` |

### 4.9 折叠/展开交互

| 属性 | 值 |
|------|------|
| 默认状态 | 展开 |
| 折叠动画 | `max-height` 从实际值→0，300ms ease-out |
| 展开动画 | `max-height` 从0→实际值，300ms ease-in |
| overflow | hidden（折叠时裁切内容） |
| 标题栏 | 始终可见，点击切换 |
| 箭头动画 | `transform: rotate(-90deg)` ↔ `rotate(0deg)`，200ms |

```css
.summary-body {
  overflow: hidden;
  transition: max-height 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.summary-body.collapsed {
  max-height: 0 !important;
}
```

---

## 5. 最终总结卡片规范

### 5.1 最终总结 vs 轮次总结

| 属性 | 轮次总结（`round_summary`） | 最终总结（`final_summary`） |
|------|---------------------------|---------------------------|
| 时机 | 每轮讨论结束后 | 整场讨论结束后 |
| 标题 | `第 N 轮 观点总结` | `🎯 讨论总结` |
| 边框 | 2px solid brand | 2px solid brand + 发光脉冲 |
| 结论 | 无 | 有 `verdict` 一句话结论 |
| 辉光 | 静态微弱辉光 | 动态呼吸辉光 |

### 5.2 最终总结结构

```
╔════════════════════════════════════════════════════════════╗
║  🎯 讨论总结                          [▸ 折叠]           ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ┌──────────────────────────────────────────────────────┐ ║
║  │ 💡 结论：采用 FastAPI 重写核心模块，保留 Flask 遗留   │ ║
║  │    代码渐进迁移                                       │ ║
║  └──────────────────────────────────────────────────────┘ ║
║                                                            ║
║  ■ 全部共识 (3)                                            ║
║  ┌──────────────────────────────────────────────────────┐ ║
║  │ ✅ FastAPI 性能优势在 IO 密集场景明显                  │ ║
║  │ ✅ 团队熟悉 Python，学习成本可控                       │ ║
║  │ ✅ 新项目推荐用 FastAPI                               │ ║
║  └──────────────────────────────────────────────────────┘ ║
║                                                            ║
║  ■ 全部分歧 (1)                                            ║
║  ┌──────────────────────────────────────────────────────┐ ║
║  │ ⚠️ 是否应该全面迁移现有 Flask 代码                    │ ║
║  │    [Alice 支持] [Bob 反对] [Carol 反对]              │ ║
║  └──────────────────────────────────────────────────────┘ ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### 5.3 最终总结特殊样式

| 属性 | 值 | 说明 |
|------|------|------|
| 边框 | 2px solid `var(--rt-brand)` | 与轮次总结相同 |
| 发光效果 | `box-shadow` 呼吸脉冲动画 | 3s 周期 |
| 辉光色 | `rgba(79, 70, 229, 0.2)` ↔ `rgba(79, 70, 229, 0.4)` | 柔和呼吸 |
| 结论区 | 18px 加粗，品牌色渐变文字 | 全场最重要信息 |

**呼吸辉光动画**：
```css
@keyframes glowBreath {
  0%, 100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.2); }
  50%      { box-shadow: 0 0 30px rgba(79, 70, 229, 0.4); }
}

.summary-card.final {
  animation: glowBreath 3s ease-in-out infinite;
}
```

### 5.4 结论区设计

```
┌──────────────────────────────────────────────────────┐
│ 💡 结论：采用 FastAPI 重写核心模块，保留 Flask 遗留   │
│    代码渐进迁移                                       │
└──────────────────────────────────────────────────────┘
```

| 属性 | 值 |
|------|------|
| 背景 | `rgba(79, 70, 229, 0.1)` |
| 边框 | 1px solid `rgba(79, 70, 229, 0.3)` |
| 圆角 | 10px |
| 图标 | 💡 |
| 文字 | 18px，`font-weight: 600` |
| 内边距 | 16px 20px |
| 位置 | 标题下方、共识/分歧上方 |

---

## 6. 页面布局与响应式适配

### 6.1 页面结构总览

```
┌─────────────────────────────────────────────────────┐
│ [TOP BAR]  🟢 LIVE  主题标题  👥 在线  ⏱ 时间  分享 │ ← sticky
├─────────────────────────────────────────────────────┤
│                                                     │
│  [speech-card] Alice 发言...                        │
│  [speech-card] Bob 发言...                          │
│  [typing-indicator] Carol 正在输入...               │
│  [speech-card] Carol 发言...                        │ ← 流式输入中
│  [summary-card] 第 1 轮观点总结                     │
│  [speech-card] Bob 回应...                          │
│  [summary-card] 第 2 轮观点总结                     │
│  [summary-card.final] 🎯 讨论总结                   │
│                                                     │
├─────────────────────────────────────────────────────┤
│ [BOTTOM BAR]  Roundtable · 多 Agent 圆桌讨论        │ ← fixed
└─────────────────────────────────────────────────────┘
```

### 6.2 内容容器

| 属性 | 值 |
|------|------|
| 最大宽度 | 720px（`var(--rt-max-width)`） |
| 水平居中 | `margin: 0 auto` |
| 内边距（桌面） | `20px 24px 80px` |
| 内边距（移动） | `16px 16px 80px` |
| 底部留白 | 80px（避免被底栏遮挡） |

### 6.3 顶栏（Top Bar）

| 属性 | 值 |
|------|------|
| 定位 | `sticky`，`top: 0` |
| z-index | 100 |
| 背景 | `rgba(15, 23, 42, 0.85)` + `backdrop-filter: blur(12px)` |
| 内容 | LIVE 徽章 + 标题 + 元信息 + 分享按钮 |
| 移动端 | 隐藏元信息和分享按钮，仅保留 LIVE 徽章和标题 |

### 6.4 输入中指示器（Typing Indicator）

当 Agent 正在发言但尚无 token 到达时，显示"正在输入"动画。

| 属性 | 值 |
|------|------|
| 位置 | 对应 Agent 头像右侧 |
| 样式 | 3 个弹跳圆点 + "正在输入..." 文字 |
| 圆点尺寸 | 6×6px |
| 颜色 | `var(--rt-text-muted)` |
| 动画 | `typingBounce` 1.4s，错开 0.2s |
| 边距缩进 | 54px（对齐气泡正文） |

### 6.5 响应式断点

| 断点 | 调整 |
|------|------|
| `≤768px`（手机） | 隐藏顶栏元信息/分享按钮；气泡内边距缩小至 16px；头像 36×36px；发言时间隐藏；卡片字号缩小 1px；观点卡片内边距 16px |
| `≤480px`（小手机） | 观点卡片改为单列堆叠；Agent 归属标签换行显示 |
| `prefers-reduced-motion: reduce` | 所有动画 duration 设为 0ms；光标不闪烁，固定显示 |

### 6.6 无障碍考虑

| 项 | 处理 |
|------|------|
| 减弱动效 | `@media (prefers-reduced-motion: reduce)` 全局禁用动画 |
| 键盘导航 | 折叠/展开支持 Enter/Space 键 |
| 屏幕阅读器 | 气泡使用 `role="article"`；观点卡片使用 `role="region"` + `aria-label` |
| 对比度 | 所有文字/背景组合 ≥ WCAG AA（4.5:1） |

### 6.7 观看模式切换

支持「实时」和「完成后查看」两种观看模式，通过顶栏右侧切换器切换。

```
┌─────────────────────────────────────────────────────┐
│  ● 实时   ▶ 完成后查看    │  🟢 LIVE │  3/5 轮次  │
└─────────────────────────────────────────────────────┘
```

#### 模式对比

| 模式 | 图标 | 行为 | 适用场景 |
|------|------|------|----------|
| **实时** (默认) | ● (红色脉冲圆点) | 实时显示流式输出，启用自动滚动 | 观看进行中的讨论 |
| **完成后查看** | ▶ (播放图标) | 不逐字渲染，讨论结束后一次性展示全部内容 | 回看历史讨论 |

#### 切换器 UI

| 属性 | 值 |
|------|----|
| 位置 | 顶栏左侧，LIVE 徽章之前 |
| 样式 | Segmented control |
| 实时模式激活态 | 红色脉冲圆点 `#EF4444` + `pulse 2s infinite` |
| 完成后模式激活态 | `var(--rt-brand)` 背景 + 白色文字 |
| 右侧信息 | 当前轮次进度 `N/M 轮次`，`var(--rt-text-muted)` 12px |
| 切换行为 | 平滑过渡，不中断后台数据接收 |

#### 「完成后查看」模式细节

- 页面加载后不逐字渲染，显示居中等待态
- 等待态：spinner + 「讨论进行中，完成后将自动展示...」
- 讨论结束后自动渲染所有内容，各气泡 `fadeSlideIn 300ms` 依次出现（间隔 100ms）
- 用户可随时切回「实时」模式追赶进度

```css
.view-mode-switch {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #EF4444;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50%      { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
}
```

---

## 7. 组件清单与交付物

### 7.1 组件清单

| # | 组件 | 优先级 | 状态 |
|---|------|--------|------|
| 1 | 流式发言气泡（`.speech-card`） | P0 | 待开发 |
| 2 | 打字光标（`.typing-cursor`） | P0 | 待开发 |
| 3 | 完成标记（`.speech-checkmark`） | P0 | 待开发 |
| 4 | 输入中指示器（`.typing-indicator`） | P0 | 待开发 |
| 5 | 自动滚动控制 | P0 | 待开发 |
| 6 | "↓ 新消息"浮动按钮 | P0 | 待开发 |
| 7 | SSE 断线重连提示条 | P0 | 待开发 |
| 8 | 观看模式切换器（实时/完成后查看） | P0 | 待开发 |
| 9 | 轮次观点卡片（`.summary-card`） | P1 | 待开发 |
| 10 | 最终总结卡片（`.summary-card.final`） | P1 | 待开发 |
| 11 | 收敛度进度条（`.convergence-bar`） | P1 | 待开发 |
| 12 | 共识/分歧条目 | P1 | 待开发 |
| 13 | Agent 归属标签（`.agent-tag`） | P1 | 待开发 |
| 14 | 全文/精简模式切换器（`.mode-toggle`） | P1 | 待开发 |
| 15 | 折叠/展开交互 | P1 | 待开发 |

### 7.2 设计交付物清单

| # | 交付物 | 说明 | 状态 |
|---|--------|------|------|
| 1 | 流式气泡组件规范 | 头像、颜色、气泡样式、DOM 结构 | ✅ 本文档 §2 |
| 2 | 打字光标动画规范 | 闪烁频率、颜色、消失动画 | ✅ 本文档 §3.1 |
| 3 | 观点卡片组件规范 | 共识/分歧标签、折叠交互 | ✅ 本文档 §4 |
| 4 | 最终总结卡片规范 | 发光效果、边框样式、结论区 | ✅ 本文档 §5 |
| 5 | 移动端适配规则 | 断点、字号、间距调整 | ✅ 本文档 §6.5 |
| 6 | DESIGN-sprint1.md（本文件） | 完整设计规范 | ✅ |

### 7.3 验收对照表

对照 PRD §7 验收标准的设计侧检查：

| PRD 验收项 | 设计覆盖 | 文档位置 |
|-----------|---------|---------|
| A1 逐字渲染 ≤50ms | §3.6 Token 节奏控制 | §3.6 |
| A2 打字光标闪烁/消失 | §3.1 打字光标 | §3.1 |
| A3 Agent 区分 | §2.3 色彩分配 + §2.2 头像 | §2.2-2.3 |
| A4 自动滚动 | §3.5 自动滚动行为 | §3.5 |
| A5 断线续传视觉 | §3.7 SSE 断线重连 | §3.7 |
| A6 完成标记 ✓ | §3.4 完成标记 | §3.4 |
| B1 观点卡片 | §4 卡片规范 | §4 |
| B2 共识/分歧标签 | §4.5 + §4.6 | §4.5-4.6 |
| B3 折叠/展开 | §4.8 折叠交互 | §4.8 |
| B4 观点归属 | §4.7 Agent 归属标签 | §4.7 |
| B5 最终总结 | §5 最终总结卡片 | §5 |
| C1 移动端适配 | §6.5 响应式断点 | §6.5 |

---

*本文档由像素姐（设计总监）编写，配合饼哥 PRD 产出。如有疑问请联系设计负责人。* 🎨
