# 发言卡片组件规范

> 设计师：像素姐 🎨 | 日期：2026-05-21 | 版本：v1.0

---

## 1. 组件结构

```
┌─────────────────────────────────────────────────┐
│ [头像]  饼哥  [产品]  ·  2 min ago              │
│         我觉得核心问题是降低门槛。现在用户要配置   │
│         channel 才能看到讨论内容，这个流程太重了。  │
└─────────────────────────────────────────────────┘
│←3px 品牌蓝描边→│← 20px padding →│
```

### DOM 结构

```html
<div class="speech-card">
  <div class="speech-avatar {role}">{姓}</div>
  <div class="speech-body">
    <div class="speech-meta">
      <span class="speech-name">{name}</span>
      <span class="speech-role {role}">{role_label}</span>
      <span class="speech-time">{relative_time}</span>
    </div>
    <div class="speech-text">{content}</div>
  </div>
</div>
```

---

## 2. 尺寸规范

| 元素 | 尺寸 | 说明 |
|------|------|------|
| 卡片最小高度 | auto (由内容撑开) | 不设固定高度 |
| 卡片 padding | 20px | 移动端 16px |
| 头像尺寸 | 40×40px | 移动端 36×36px |
| 头像圆角 | 50% (圆形) | — |
| 角色徽章 padding | 2px 8px | — |
| 角色徽章圆角 | 999px (药丸形) | — |
| 左侧描边宽度 | 3px | 新发言高亮时可见 |
| 卡片间距 | 16px | 卡片之间 margin-bottom |
| 卡片圆角 | 10px | var(--rt-radius-md) |

---

## 3. 角色徽章色值映射

| 角色 | 角色名 | 徽章色 | 徽章底色 | 头像底色 | 中文标签 |
|------|--------|--------|----------|----------|----------|
| product | 产品 | `#3B82F6` | `rgba(59,130,246,0.15)` | `#3B82F6` | 产品 |
| design | 设计 | `#A855F7` | `rgba(168,85,247,0.15)` | `#A855F7` | 设计 |
| engineer | 工程 | `#22C55E` | `rgba(34,197,94,0.15)` | `#22C55E` | 工程 |
| research | 研究 | `#F59E0B` | `rgba(245,158,11,0.15)` | `#F59E0B` | 研究 |
| marketing | 运营 | `#EC4899` | `rgba(236,72,153,0.15)` | `#EC4899` | 运营 |
| default | 默认 | `#64748B` | `rgba(100,116,139,0.15)` | `#64748B` | — |

### 徽章字体

- 字号：11px
- 字重：600 (Semi-Bold)
- 字色：与徽章色同色
- 转换：text-transform: uppercase
- 字距：letter-spacing: 0.05em

---

## 4. 头像规范

### 内容
- 取发言人名字的**第一个汉字**
- 字号：15px（桌面）/ 13px（移动端）
- 字重：600
- 字色：`#FFFFFF`（白色）

### 状态
- 默认态：角色色纯色填充
- 在线态：角色色 + 右下角绿色小圆点

---

## 5. 文字层级

| 元素 | 字号 | 字重 | 颜色 | 行高 |
|------|------|------|------|------|
| 发言人名字 | 14px | 600 | `--rt-text-primary` (#F1F5F9) | 1.4 |
| 角色标签 | 11px | 600 | 角色色 | 1.2 |
| 时间戳 | 12px | 400 | `--rt-text-muted` (#64748B) | 1.4 |
| 发言正文 | 15px | 400 | `--rt-text-secondary` (#94A3B8) | 1.7 |

---

## 6. 卡片状态

### 默认态
```css
background: var(--rt-bg-card);       /* #1E293B */
border: 1px solid var(--rt-border);  /* #334155 */
border-left: 3px solid transparent;
```

### Hover 态
```css
background: var(--rt-bg-card-hover); /* #334155 */
```

### 新发言高亮态（重点）
```css
border-left: 3px solid var(--rt-brand);  /* #4F46E5 */
box-shadow: 0 0 20px rgba(79, 70, 229, 0.15);
/* 2 秒后渐隐至默认态 */
animation: highlight-fade 2s ease-out forwards;
```

### 淡入态（新发言出现时）
```css
animation: fadeSlideIn 300ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
/* from opacity:0 translateY(12px) → to opacity:1 translateY(0) */
```

---

## 7. 发言人列表格式

发言人名字后跟角色徽章，用空格分隔。时间戳右对齐。

```
饼哥  [产品]              2 min ago
像素姐 [设计]             1 min ago
码飞  [工程]              just now
```

### 时间格式
- < 1 min → "just now"
- 1-59 min → "X min ago"
- ≥ 60 min → "X hr ago"
- 跨天 → "MM-DD HH:mm"

---

## 8. 结论卡片变体

讨论结束时追加结论卡片，与发言卡片区分：

| 属性 | 结论卡片 | 发言卡片 |
|------|----------|----------|
| 边框 | 1.5px solid 品牌蓝 | 1px solid 默认灰 |
| 背景 | 渐变 (#1E293B → #1a2744) | 纯色 #1E293B |
| 阴影 | 品牌蓝辉光 (脉动动画) | 无 |
| 圆角 | 16px | 10px |
| padding | 32px | 20px |
| 标签 | "💡 讨论结论" | 角色徽章 |

详见 `state-ended.html` 原型。

---

## 9. 实现注意事项

- 卡片使用 `display: flex` 布局，头像固定宽度，内容区 `flex: 1`
- 头像和内容区之间 gap 14px
- 移动端时间戳隐藏（`display: none`），节省空间
- 长文本自动换行：`word-break: break-word`
- 代码块使用等宽字体 `var(--rt-font-mono)`
