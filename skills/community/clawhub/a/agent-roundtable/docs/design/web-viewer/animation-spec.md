# 实时更新动效规范

> 设计师：像素姐 🎨 | 日期：2026-05-21 | 版本：v1.0

---

## 1. 核心动效清单

| # | 动效名称 | 触发时机 | 持续时间 | 缓动函数 |
|---|---------|---------|---------|---------|
| 1 | 新发言淡入 | SSE 推送新发言 | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| 2 | 品牌蓝描边高亮 | 新发言出现 | 2000ms | ease-out |
| 3 | 结论卡片辉光 | 讨论结束 | 3000ms 循环 | ease-in-out |
| 4 | 倒计时呼吸 | 等待中状态 | 3000ms 循环 | ease-in-out |
| 5 | 打字指示器 | 发言流式输出中 | 1400ms 循环 | ease-in-out |
| 6 | LIVE 徽章闪烁 | 进行中状态 | 1500ms 循环 | ease-in-out |

---

## 2. 新发言淡入动画（核心）

### 触发条件
SSE 推送 `event: speech` 时，将新发言卡片插入到时间流底部。

### 动画参数
```css
@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.speech-card.fade-in {
  animation: fadeSlideIn 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
```

### 关键细节
- 初始状态：`opacity: 0` + `translateY(12px)`（从下方 12px 淡入）
- 结束状态：`opacity: 1` + `translateY(0)`
- 使用 `forwards` 保持结束状态
- 缓动：标准减速曲线（ease-out 感知）

---

## 3. 品牌蓝描边高亮（核心）

### 触发条件
新发言卡片出现后，左侧边框亮起品牌蓝，2 秒后渐隐。

### 动画参数
```css
@keyframes highlight-fade {
  0% {
    border-left-color: #4F46E5;
    box-shadow: 0 0 20px rgba(79, 70, 229, 0.3);
  }
  100% {
    border-left-color: transparent;
    box-shadow: none;
  }
}

.speech-card.highlighted {
  border-left: 3px solid #4F46E5;
  animation: highlight-fade 2s ease-out forwards;
}
```

### 关键细节
- 高亮持续时间：**2000ms**（PRD 原写 3s，经设计评审调整为 2s，更流畅）
- 左侧描边：3px 宽度，品牌蓝 `#4F46E5`
- 辉光阴影：`0 0 20px rgba(79, 70, 229, 0.3)`
- 渐隐曲线：`ease-out`（先快后慢，自然消退）
- 2 秒后完全透明，恢复默认态

### 时序关系
```
0ms     ← 新发言出现
0-300ms ← 淡入动画（fadeSlideIn）同时进行
0-2000ms ← 蓝色描边高亮渐隐
2000ms  ← 完全恢复默认态
```

---

## 4. 结论卡片辉光脉动

### 触发条件
讨论结束后，结论卡片自动追加并滚动定位。

### 动画参数
```css
@keyframes glow-pulse {
  0%, 100% {
    box-shadow:
      0 0 20px rgba(79, 70, 229, 0.2),
      0 0 60px rgba(79, 70, 229, 0.1),
      0 8px 24px rgba(0, 0, 0, 0.4);
  }
  50% {
    box-shadow:
      0 0 30px rgba(79, 70, 229, 0.35),
      0 0 80px rgba(79, 70, 229, 0.15),
      0 8px 24px rgba(0, 0, 0, 0.4);
  }
}

.conclusion-card {
  animation: glow-pulse 3s ease-in-out infinite;
}
```

### 关键细节
- 辉光三层阴影：近光 → 远光 → 投影
- 脉动周期：3 秒
- 缓动：`ease-in-out`（柔和呼吸感）
- 无限循环，但不影响阅读（变化幅度克制）

---

## 5. 倒计时呼吸动画（等待中）

```css
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.08); opacity: 1; }
}

.logo-ring {
  animation: breathe 3s ease-in-out infinite;
}
```

- 缩放范围：1.0 → 1.08（微妙放大）
- 透明度：0.8 → 1.0
- 周期：3 秒

---

## 6. 打字指示器（进行中）

```css
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-6px); opacity: 1; }
}
```

- 三个圆点依次跳动（delay 0s / 0.2s / 0.4s）
- 跳动高度：6px
- 周期：1.4 秒

---

## 7. 自动滚动行为

### 新发言滚动
```javascript
// 新发言出现后，如果用户已在底部，自动滚动
if (isNearBottom(threshold = 100)) {
  speechCard.scrollIntoView({ behavior: 'smooth', block: 'end' });
}
```

### 结论卡片滚动
```javascript
// 讨论结束后，自动滚动到结论卡片
conclusionCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
```

### 滚动规则
- 用户在底部 100px 范围内 → 自动滚动
- 用户手动向上翻 → 不自动滚动（避免打断阅读）
- 结论卡片 → 始终自动滚动

---

## 8. 性能规范

### 允许的动画属性
- `transform`（GPU 加速）
- `opacity`（GPU 加速）
- `box-shadow`（少量使用）

### 禁止的动画属性
- `width` / `height`（触发 layout）
- `top` / `left` / `margin`（触发 layout）
- `background-color`（频繁重绘）

### prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

尊重系统减弱动效设置，所有动画降为瞬间完成。

---

## 9. 动效时序总览

```
等待中状态：
  [呼吸动画] 持续循环 → [倒计时] 实时更新

进行中状态：
  [LIVE 闪烁] 持续循环
  [新发言] → 淡入 300ms + 描边高亮 2s
  [打字指示器] → 等待下一个发言时出现

已结束状态：
  [结论卡片] → 淡入 + 辉光脉动持续循环
  [自动滚动] → smooth scroll 到结论
```
