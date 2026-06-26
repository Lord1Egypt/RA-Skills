# Web Viewer 设计规范总览

> 设计师：像素姐 🎨 | 日期：2026-05-21 | 版本：v1.0
> 关联 PRD：`/docs/product/PRD-web-viewer.md`
> 关联讨论：`/docs/discussions/web-viewer-discussion.md`（rt_36c7dbdd）

---

## 设计理念

**"现场直播感"** — 让查看圆桌讨论就像观看一场现场直播。

- **等待中**：紧张的倒计时 + 温暖的欢迎语 → 期待感
- **进行中**：实时滚动的发言流 + 品牌蓝高亮 → 参与感
- **已结束**：发光的结论卡片 → 仪式感 + 收获感

---

## 文件清单

```
docs/design/web-viewer/
├── WEB-VIEWER-SPEC.md          ← 本文件（总览）
├── theme.css                   ← CSS 变量表（交付给码飞）
├── state-waiting.html          ← 等待中原型
├── state-live.html             ← 进行中原型
├── state-ended.html            ← 已结束原型
├── component-spec.md           ← 发言卡片组件规范
├── mobile-spec.md              ← 移动端适配规则
├── animation-spec.md           ← 实时更新动效规范
└── share-interaction-spec.md   ← 分享交互稿（链接复制 + 撤销确认）
```

---

## 色彩体系

### 主色调

| 用途 | 色值 | 变量名 |
|------|------|--------|
| 品牌蓝（主） | `#4F46E5` | `--rt-brand` |
| 品牌蓝 hover | `#4338CA` | `--rt-brand-hover` |
| 品牌蓝浅 | `#6366F1` | `--rt-brand-light` |

### 背景层级

| 层级 | 色值 | 变量名 | 用途 |
|------|------|--------|------|
| Body | `#0F172A` | `--rt-bg-body` | 页面底色 |
| Card | `#1E293B` | `--rt-bg-card` | 卡片/面板 |
| Card Hover | `#334155` | `--rt-bg-card-hover` | 悬浮态 |

### 文字层级

| 层级 | 色值 | 变量名 | 用途 |
|------|------|--------|------|
| Primary | `#F1F5F9` | `--rt-text-primary` | 标题、名字 |
| Secondary | `#94A3B8` | `--rt-text-secondary` | 正文 |
| Muted | `#64748B` | `--rt-text-muted` | 时间戳、提示 |
| Disabled | `#475569` | `--rt-text-disabled` | 禁用态 |

### 角色色

| 角色 | 色值 | 场景 |
|------|------|------|
| 产品 | `#3B82F6` | 饼哥 |
| 设计 | `#A855F7` | 像素姐 |
| 工程 | `#22C55E` | 码飞 |
| 研究 | `#F59E0B` | 小赫 |

> 完整色值见 `theme.css`

---

## 页面三态

### 状态 1：等待中

- **布局**：居中单列，max-width 480px
- **核心元素**：呼吸动画 Logo 环 + 倒计时 + 话题预览 + 参与者头像
- **氛围**：期待感、温暖
- **原型**：`state-waiting.html`

### 状态 2：进行中

- **布局**：单列时间流，max-width 720px
- **核心元素**：LIVE 徽章 + 发言卡片流 + 打字指示器
- **氛围**：实时感、参与感
- **新发言动效**：淡入 300ms + 品牌蓝描边高亮 2s
- **原型**：`state-live.html`

### 状态 3：已结束

- **布局**：同进行中 + 结论卡片置顶
- **核心元素**：结论发光卡片 + 统计摘要 + 历史发言
- **氛围**：仪式感、收获感
- **自动行为**：smooth scroll 到结论卡片
- **原型**：`state-ended.html`

---

## 核心组件

### 发言卡片

- Flex 布局：头像(40px) + gap(14px) + 内容区(flex:1)
- 左侧 3px 描边（新发言时品牌蓝高亮）
- 角色徽章：药丸形，角色色浅底 + 角色色文字
- 详见 `component-spec.md`

### 结论卡片

- 渐变背景 + 品牌蓝边框 + 辉光脉动
- 与发言卡片视觉层级明确区分
- 包含：标签 + 标题 + 正文 + 元信息
- 详见 `state-ended.html`

---

## 动效规范

| 动效 | 时长 | 缓动 | 触发 |
|------|------|------|------|
| 新发言淡入 | 300ms | ease-out | SSE 推送 |
| 蓝色描边高亮 | 2000ms | ease-out | 新发言出现 |
| 结论辉光 | 3000ms 循环 | ease-in-out | 讨论结束 |
| 倒计时呼吸 | 3000ms 循环 | ease-in-out | 等待中 |

> 完整动效规范见 `animation-spec.md`

---

## 移动端规则

- 断点：768px
- 最小字号：14px（正文）
- 最小触控区：44×44px
- 时间戳移动端隐藏
- 微信兼容：sticky + 毛玻璃降级 + 安全区域
- 详见 `mobile-spec.md`

---

## 与现有设计体系的关系

本 Web Viewer 使用**独立色彩方案**（Dark Slate + 品牌靛蓝），与 Roundtable 主品牌（Tokyo Night）并行：

| 项目 | 主品牌 (Tokyo Night) | Web Viewer |
|------|---------------------|------------|
| 使用场景 | CLI / 终端 / README | 浏览器 Web 页面 |
| 主色调 | 蓝紫渐变 `#7aa2f7→#bb9af7` | 靛蓝 `#4F46E5` |
| 背景 | `#1a1b26` | `#0F172A` |
| 选型原因 | 终端可读性 | Tailwind 暗色系通用性 |

两者共享设计语言（圆环、节点、讨论感），但色彩体系独立，互不冲突。

---

## 分享交互

### 链接复制

- 桌面端：Popover 弹出面板（360px），显示可复制链接
- 移动端：Bottom Sheet 底部滑出
- 复制反馈：「复制」→「✓ 已复制」绿色提示，2s 恢复
- 降级：`navigator.clipboard` → `execCommand` fallback（微信兼容）

### 链接撤销

- 确认对话框：红色「确认撤销」按钮 + 警告文案
- 撤销后 ≤5s 页面切换为失效提示页
- 详见 `share-interaction-spec.md`

---

## 给码飞的开发提示

1. **theme.css** 直接引入，CSS 变量全局可用
2. **Tailwind CDN** 搭配 CSS 变量使用，不需 build step
3. 新发言用 JS 添加 `.fade-in` 和 `.highlighted` class，2s 后移除 `.highlighted`
4. 结论卡片用 JS 添加 `.conclusion-card` class 触发辉光
5. `scrollIntoView({ behavior: 'smooth' })` 做自动滚动
6. 移动端记得加 `-webkit-sticky` 前缀
7. 微信环境下 SSE 降级为长轮询

---

## 交付物清单

- [x] CSS 变量表（theme.css）
- [x] 等待中页面原型（state-waiting.html）
- [x] 进行中页面原型（state-live.html）
- [x] 已结束页面原型（state-ended.html）
- [x] 发言卡片组件规范（component-spec.md）
- [x] 移动端适配规则（mobile-spec.md）
- [x] 实时更新动效规范（animation-spec.md）
- [x] 分享交互稿（share-interaction-spec.md）
- [x] 设计规范总览（本文件）
