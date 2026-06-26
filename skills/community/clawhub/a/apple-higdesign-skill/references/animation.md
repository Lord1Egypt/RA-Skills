# Animation

> 来源：Apple HIG - Animation (2026)
> https://developer.apple.com/design/human-interface-guidelines/animation

## 动画原则

### Purposeful（有目的）
每个动画都应有明确的用途：
- **提供反馈** — 确认操作被接收
- **传达状态** — 显示当前进度或位置
- **引导注意力** — 指向重要变化
- **建立空间感** — 暗示界面元素之间的层级关系

### Immediate（即时响应）
动画延迟 ≤ 100ms 才感觉"即时"：
- 触摸反馈：即时（0-50ms）
- 视图切换：快速（200-400ms）
- 入场动画：优雅但不过慢（300-500ms）

### Efficient（高效）
- 动画期间保持 60fps
- 避免在动画过程中做重计算
- 使用 GPU 加速的动画（transform / opacity）

---

## 常用动画类型

### 视图切换
| 动画 | 平台 | 用途 |
|------|------|------|
| Push | iOS | 导航栈推入 |
| Pop | iOS | 从栈返回 |
| Modal Present | iOS | 模态页面出现 |
| Modal Dismiss | iOS | 模态页面消失 |
| Cross dissolve | macOS | 淡入淡出 |

### 内容过渡
| 动画 | 用途 |
|------|------|
| Fade | 内容替换 |
| Scale | 缩放反馈 |
| Slide | 滑入/滑出 |

### 手势驱动
- **橡皮筋效果（Rubber Banding）** — 列表到顶/到底的弹性
- **惯性滚动** — 滚动速度决定停止位置
- **拖放** — 元素跟随手指，松手后放置

---

## SF Symbols 动画
见 `sf-symbols.md` — SF Symbols 内置 12 种动画。

---

## 减少动画（Reduce Motion）

当用户开启"减弱动画效果"时：
- 将位移动画替换为淡入淡出
- 取消自动播放的视频
- 停止循环动画
- 用静态指示器替代旋转 loading

```swift
// 检测 Reduce Motion
if UIAccessibility.isReduceMotionEnabled {
    // 使用替代动画
}
```

---

## 性能建议

### 推荐（GPU 加速）
- `transform: translate/scale/rotate`
- `opacity`
- `backgroundColor`（简单颜色）

### 避免（触发重排）
- `width` / `height` 动画
- `margin` / `padding` 动画
- 布局相关的属性动画

---

## 平台风格

| 平台 | 动画风格 |
|------|---------|
| iOS | 手势驱动，弹性，物理感 |
| macOS | 直接，精确，克制 |
| visionOS | 空间感，深度，虚实转换 |
| watchOS | 快速，微型，grain 效果 |
| tvOS | 焦点驱动，夸张的放大效果 |
