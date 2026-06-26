# 移动端适配规则

> 设计师：像素姐 🎨 | 日期：2026-05-21 | 版本：v1.0

---

## 1. 断点策略

| 断点 | 宽度 | 设备 | 布局 |
|------|------|------|------|
| 桌面 | > 768px | iPad 横屏、笔记本、桌面 | 单列居中，max-width 720px |
| 移动 | ≤ 768px | 手机、iPad 竖屏 | 单列堆叠，全宽 + 16px padding |

> MVP 只需两个断点，不做更细粒度的适配。

---

## 2. 字号规范

### 最小字号底线：14px

任何文字元素不得小于 14px（标题/徽章等装饰性元素允许 12px，但正文必须 ≥ 14px）。

| 元素 | 桌面 | 移动 | 说明 |
|------|------|------|------|
| 页面标题 h1 | 24px | 20px | 同比例缩小 |
| 副标题 h2 | 20px | 18px | — |
| 正文 | 15px | 14px | 底线 14px |
| 发言人名 | 14px | 14px | 保持不变 |
| 角色标签 | 11px | 11px | 装饰元素，可 <14px |
| 时间戳 | 12px | 隐藏 | 移动端隐藏节省空间 |
| 辅助说明 | 13px | 13px | 装饰元素 |
| 倒计时数字 | 48px | 36px | — |

---

## 3. 触控规范

### 最小触控区：44×44px

所有可交互元素必须满足：

| 元素 | 视觉尺寸 | 触控区 | 说明 |
|------|----------|--------|------|
| 头像 | 36×36px | 44×44px | padding 扩大触控区 |
| 按钮 | h: 40px | h: 44px | min-height: 44px |
| 链接 | auto | auto | 上下 padding ≥ 10px |
| 徽章 | auto | 不可点击 | 纯展示 |

---

## 4. 间距适配

| 间距 | 桌面 | 移动 |
|------|------|------|
| 内容区 padding | 24px | 16px |
| 卡片 padding | 20px | 16px |
| 卡片间距 | 16px | 16px |
| 区块间距 | 32px | 24px |
| 顶部导航 padding | 12px 24px | 10px 16px |
| 底部栏 padding | 12px 24px | 12px 16px |

---

## 5. 组件适配规则

### 发言卡片
- 桌面：头像 + 内容横排（flex-direction: row）
- 移动：保持横排，但头像缩小至 36px
- 时间戳移动端隐藏

### 结论卡片
- 桌面：padding 32px，标题 20px
- 移动：padding 24px，标题 18px
- 辉光效果保持（不影响性能）

### 统计行
- 桌面：3 列 grid
- 移动：3 列 grid（保持），gap 缩小至 8px

### 倒计时
- 桌面：48px 数字
- 移动：36px 数字

### 导航栏
- 桌面：显示参与者数 + 时长
- 移动：只显示 LIVE 徽章 + 标题

---

## 6. 微信内置浏览器兼容

### 已知问题
1. SSE 可能被拦截 → 需降级为长轮询
2. `backdrop-filter: blur()` 部分机型不支持 → 提供 fallback 纯色背景
3. `position: sticky` 需要 `-webkit-sticky` 前缀
4. 安全区域（刘海屏）需要 `env(safe-area-inset-*)`

### CSS 兼容处理

```css
/* sticky 兼容 */
.top-bar {
  position: -webkit-sticky;
  position: sticky;
}

/* 毛玻璃降级 */
.top-bar {
  background: rgba(15, 23, 42, 0.95); /* 降级：更不透明 */
}
@supports (backdrop-filter: blur(12px)) {
  .top-bar {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
  }
}

/* 安全区域 */
.bottom-bar {
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
}
```

---

## 7. 性能考量

- 移动端不做大量卡片虚拟滚动（MVP 阶段发言数通常 < 50）
- 动画使用 `transform` 和 `opacity`，避免触发 layout
- 图片/头像用 CSS 纯色圆形，无图片请求
- CSS 变量通过 `:root` 全局定义，移动端通过 media query 覆盖

---

## 8. 验收标准（移动端）

| 项目 | 标准 |
|------|------|
| 横向滚动 | 微信内置浏览器无横向滚动 |
| 字号 | 正文 ≥ 14px |
| 触控区 | 可交互元素 ≥ 44px |
| 导航栏 | sticky 定位正常工作 |
| 底部栏 | 不遮挡内容（padding-bottom 预留） |
| 安全区域 | 刘海屏/底部横线区域不遮挡 |
