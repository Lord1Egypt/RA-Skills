# Archetype · 产品界面 / 应用原型

## 适用场景

**当用户要的不是"一份文档"，而是"一个产品界面长什么样"**，用这个 archetype。

典型场景：

- 管理后台 demo（用户管理、商品管理、订单审核）
- SaaS 应用首页 / 数据工作台
- 带侧栏导航的内部工具
- 需要模拟真实操作流的功能原型
- 截图用来放进 PPT、需求评审、竞标方案里"演示界面"

区别信号——用户话里有这些词 → 走这个 archetype：
- "做个后台 / 管理界面 / 控制台 / 工作台"
- "像 XX 产品那样的应用原型"
- "带侧栏 / 带导航 / 带菜单"
- "模拟真实产品 / 拿去演示界面"

## 和仪表盘 archetype 的区别

这是最容易混淆的两种。简单判断：

| | 仪表盘（作为文档） | 产品界面（作为产品） |
|---|---|---|
| 读者心态 | "我要看这份数据" | "我要体验这个产品" |
| 容器 | max-width 1280px 居中 | 全视口 100vw / 100vh |
| 导航 | 无（单页文档流） | sidebar + topbar 齐全 |
| 交互 | 只 hover，无切换 | 菜单切换、tab、按钮反馈 |
| 适合用途 | 分享、评审、归档 | 演示、截图、原型评审 |

**一句话**：如果用户把它当 PDF 发给人看，选仪表盘；如果用户把它截图放进 PPT 说"产品大概长这样"，选 app-screen。

如果用户的描述两边都像（"既是数据又要有侧栏"），**优先问一下**，或者默认选 app-screen——因为从 app-screen 降级为文档更容易，反过来补产品外壳更麻烦。

## 核心结构

```
┌───────────┬────────────────────────────────────────────┐
│           │  Topbar (56-64px)                          │
│           │  面包屑 · 页标题 · 搜索 · 操作按钮 · 头像   │
│  Sidebar  ├────────────────────────────────────────────┤
│  (224px)  │                                            │
│           │  Content 区                                 │
│  品牌区    │    页标题 + 操作                           │
│  菜单组 1  │    KPI 卡片 / 表单 / 表格 / 列表            │
│  菜单组 2  │    ...                                     │
│           │                                            │
│  用户卡    │                                            │
└───────────┴────────────────────────────────────────────┘
```

**关键约束**：
- 根元素满屏：`width: 100vw; height: 100vh; overflow: hidden`
- 内容区独立滚动：`main { overflow: auto }`
- sidebar 固定宽度 224px（`--sidebar-width`），桌面端不折叠

## 整体骨架

```html
<body>
  <div class="app">
    <aside class="sidebar">
      <!-- 品牌 + 导航 + 用户卡 -->
    </aside>
    <div class="workspace">
      <header class="topbar"><!-- 面包屑 + 标题 + 操作 --></header>
      <main class="content"><!-- 页面内容 --></main>
    </div>
  </div>
</body>
```

对应的布局样式：

```css
html, body { height: 100%; margin: 0; }
body {
  font-family: var(--font-sans);
  background: var(--color-bg-page);
  color: var(--color-text-1);
  line-height: var(--lh-normal);
}
.app {
  display: grid;
  grid-template-columns: 224px 1fr;
  height: 100vh;
  overflow: hidden;
}
.sidebar {
  background: #0b1220; /* 深色，与 content 区形成对比 */
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.workspace {
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}
.topbar {
  flex-shrink: 0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-1);
}
.content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  background: var(--color-bg-soft);
}
```

## 必备组件

### 1. Sidebar · 侧栏

品牌区 + 菜单 + 用户卡。深色底（`#0b1220`）让它和白色 content 区清晰分隔。

```html
<aside class="sidebar">
  <!-- 品牌 -->
  <div class="sidebar-brand">
    <div class="brand-logo">AI</div>
    <div>
      <div class="brand-name">产品名称</div>
      <div class="brand-sub">工作台</div>
    </div>
  </div>

  <!-- 菜单 -->
  <nav class="sidebar-nav">
    <div class="nav-group-title">工作区</div>
    <a class="nav-item active">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
        <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
      </svg>
      <span>仪表盘</span>
    </a>
    <a class="nav-item">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M4 7h16M4 12h16M4 17h16"/>
      </svg>
      <span>订单管理</span>
      <span class="nav-badge">12</span>
    </a>

    <div class="nav-group-title">配置</div>
    <a class="nav-item">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19 12a7 7 0 0 0-.1-1.2l2-1.6-2-3.4-2.4.9a7 7 0 0 0-2-1.2L14 3h-4l-.5 2.5a7 7 0 0 0-2 1.2l-2.4-.9-2 3.4 2 1.6A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.6 2 3.4 2.4-.9a7 7 0 0 0 2 1.2L10 21h4l.5-2.5a7 7 0 0 0 2-1.2l2.4.9 2-3.4-2-1.6c.1-.4.1-.8.1-1.2z"/>
      </svg>
      <span>系统设置</span>
    </a>
  </nav>

  <!-- 用户卡（sidebar 底部）-->
  <div class="sidebar-user">
    <div class="user-avatar">Y</div>
    <div>
      <div class="user-name">张三</div>
      <div class="user-role">管理员</div>
    </div>
  </div>
</aside>
```

```css
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: var(--space-5) var(--space-4);
  border-bottom: 1px solid rgba(148,163,184,0.12);
}
.brand-logo {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #2563eb, #8b5cf6);
  display: grid; place-items: center;
  color: white; font-weight: 700; font-size: 13px;
}
.brand-name { color: white; font-size: 14px; font-weight: 600; }
.brand-sub { color: #64748b; font-size: 11px; }

.sidebar-nav {
  flex: 1;
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
}
.nav-group-title {
  padding: var(--space-3) var(--space-3) var(--space-1);
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  color: #cbd5e1;
  font-size: 13.5px;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.15s;
  margin-bottom: 2px;
}
.nav-item:hover { background: rgba(148,163,184,0.08); color: white; }
.nav-item.active {
  background: linear-gradient(135deg, rgba(37,99,235,0.2), rgba(139,92,246,0.15));
  color: white;
  box-shadow: inset 0 0 0 1px rgba(139,92,246,0.25);
}
.nav-icon { width: 18px; height: 18px; flex-shrink: 0; }
.nav-badge {
  margin-left: auto;
  padding: 1px 6px;
  background: rgba(239,68,68,0.25);
  color: #fca5a5;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 600;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: var(--space-4);
  border-top: 1px solid rgba(148,163,184,0.12);
}
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #ec4899);
  display: grid; place-items: center;
  color: white; font-size: 13px; font-weight: 600;
}
.user-name { color: white; font-size: 13px; font-weight: 500; }
.user-role { color: #64748b; font-size: 11px; }
```

### 2. Topbar · 顶栏

左侧面包屑 + 页标题，右侧搜索/操作/头像。用 sticky 保证滚动时一直可见（在 app 布局里 topbar 本身就不滚）。

```html
<header class="topbar">
  <div class="topbar-left">
    <nav class="breadcrumb" aria-label="面包屑">
      <a>工作区</a>
      <span class="sep" aria-hidden="true">/</span>
      <a>订单管理</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">待处理订单</span>
    </nav>
  </div>
  <div class="topbar-right">
    <div class="search-box">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/>
      </svg>
      <input placeholder="搜索订单号、客户..." />
      <kbd>⌘ K</kbd>
    </div>
    <button class="icon-btn" aria-label="通知">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
        <path d="M10 21a2 2 0 0 0 4 0"/>
      </svg>
      <span class="badge-dot"></span>
    </button>
    <div class="avatar-sm">Y</div>
  </div>
</header>
```

```css
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  color: var(--color-text-3);
}
.breadcrumb a {
  color: var(--color-text-2);
  text-decoration: none;
  transition: color 0.15s;
}
.breadcrumb a:hover { color: var(--color-primary); }
.breadcrumb .sep { color: var(--color-text-4); }
.breadcrumb [aria-current="page"] {
  color: var(--color-text-1);
  font-weight: var(--fw-medium);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.search-box {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 6px 10px;
  background: var(--color-bg-soft);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-md);
  width: 280px;
  color: var(--color-text-3);
}
.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  color: var(--color-text-1);
}
.search-box kbd {
  padding: 2px 6px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-1);
  border-radius: 4px;
  font-size: 11px;
  font-family: var(--font-sans);
  color: var(--color-text-3);
}
.icon-btn {
  position: relative;
  width: 36px; height: 36px;
  display: grid; place-items: center;
  background: transparent;
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-md);
  color: var(--color-text-2);
  cursor: pointer;
  transition: all 0.15s;
}
.icon-btn:hover { color: var(--color-primary); border-color: var(--color-primary); }
.badge-dot {
  position: absolute;
  top: 8px; right: 8px;
  width: 6px; height: 6px;
  background: var(--color-danger);
  border-radius: 50%;
}
.avatar-sm {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #ec4899);
  color: white;
  display: grid; place-items: center;
  font-size: 13px;
  font-weight: 600;
}
```

### 3. Content · 内容区

内容区是**页面的真正主体**。常见布局有三种，按页面类型选：

#### 类型 A · 列表页（最常见）

```
┌─────────────────────────────────────┐
│  页面头（标题 + 主操作按钮）          │
│  ─────────────────────              │
│  筛选栏（搜索 + 筛选 + 刷新）         │
│  ─────                              │
│  数据表格                            │
│  ─────                              │
│  分页                                │
└─────────────────────────────────────┘
```

#### 类型 B · 仪表盘页

```
┌─────────────────────────────────────┐
│  页面头（时间范围 + 导出）            │
│  ─────                              │
│  KPI 卡片行                          │
│  ─────                              │
│  图表 · 左右两栏                     │
│  ─────                              │
│  明细表格                            │
└─────────────────────────────────────┘
```

可以直接复用 `archetype-dashboard.md` 第 2-5 节的 KPI、图表、表格组件，只需把它们放进 content 区容器即可。

#### 类型 C · 表单页

```
┌─────────────────────────────────────┐
│  返回 · 页面头 · 取消 · 保存          │
│  ─────                              │
│  基础信息（分组）                     │
│  ─────                              │
│  详细信息（分组）                     │
│  ─────                              │
│  底部操作栏（sticky）                 │
└─────────────────────────────────────┘
```

### 4. 页面头（Page Header）

内容区顶部的"本页标题 + 主操作"区块，不同于 topbar。

```html
<div class="page-header">
  <div>
    <h1 class="page-title">订单管理</h1>
    <p class="page-sub">管理所有订单、处理退款申请、追踪物流</p>
  </div>
  <div class="page-actions">
    <button class="btn btn-ghost">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      导出
    </button>
    <button class="btn btn-primary">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 5v14M5 12h14"/>
      </svg>
      新建订单
    </button>
  </div>
</div>
```

```css
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--space-6);
  gap: var(--space-4);
  flex-wrap: wrap;
}
.page-title {
  margin: 0 0 4px;
  font-size: var(--fs-2xl);
  font-weight: var(--fw-bold);
  line-height: 1.2;
}
.page-sub {
  margin: 0;
  color: var(--color-text-3);
  font-size: var(--fs-sm);
}
.page-actions {
  display: flex;
  gap: var(--space-2);
}
```

### 5. 按钮系统

app-screen 比文档类 archetype 需要更丰富的按钮：

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: var(--fw-medium);
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
  border: 1px solid transparent;
}
.btn-primary {
  background: var(--color-primary);
  color: white;
}
.btn-primary:hover { background: var(--color-primary-hover); }
.btn-ghost {
  background: var(--color-bg-card);
  color: var(--color-text-2);
  border-color: var(--color-border-1);
}
.btn-ghost:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
.btn-danger {
  background: var(--color-danger);
  color: white;
}
```

### 6. 卡片容器

content 区的大部分内容都应该放在卡片里，避免视觉上"一摊散的"：

```css
.card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-4);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-2);
}
.card-title {
  margin: 0;
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
}
```

## 交互提示（关键）

产品界面原型**必须有一些交互反馈**，否则看起来像张死图：

1. **菜单项 `.active` 必须有**——让读者一眼看到"当前在哪个页面"
2. **Hover 过渡**——按钮、菜单项、表格行都要有 `transition: ... 0.15s`
3. **聚焦样式**——输入框 `:focus` 时 border 变主色
4. **状态 tag**——表格里的状态列用彩色 tag 而不是纯文字
5. **小徽标**——菜单项的"待处理数字"、通知的红点

但**不要**做：
- 菜单点击切换（会暴露只有一页的事实）
- 表单真实提交（原型不需要后端）
- 复杂的模态对话框（增加维护成本）

## 判断"是否需要复用其他 archetype 的组件"

app-screen 是容器，content 区可以装几乎任何东西。按用户的"内容需求"决定复用哪里：

| 内容需求 | 去哪里拿组件 |
|---|---|
| 数据表格、排行榜、状态 tag | `archetype-dashboard.md` 第 4-5 节 |
| KPI 卡片、图表 | `archetype-dashboard.md` 第 2-3 节 |
| 富文本内容、长段落 | `archetype-article.md` 的排版规则 |
| 大数字展示 | `archetype-poster.md` 第 2 节（stats-hero） |

**重要**：复用时要把组件外层的 `max-width: 1280px; margin: 0 auto` 去掉——app-screen 里内容区已经被 sidebar 约束过宽度了。

## 响应式

产品界面的响应式比文档类更难——因为 sidebar 很重要。常见策略：

```css
@media (max-width: 1024px) {
  .app { grid-template-columns: 200px 1fr; }
  .search-box { width: 180px; }
}

@media (max-width: 768px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  /* 桌面级的单文件原型可以选择在移动端直接隐藏 sidebar，
     因为原型主要用来演示，不需要真实移动端适配 */
  .search-box { display: none; }
  .content { padding: var(--space-4); }
}
```

## 常见失误

- **sidebar 色值和内容区反差太小**：两者都用白/浅灰会让界面扁平没层次。sidebar 用深色（`#0b1220`）是最保险的选择。
- **content 区直接写在 body 上**：没有 `overflow: auto` 包裹，内容多了会把整个页面撑破。
- **忘了给菜单项 active**：用户看不出当前在哪页。
- **按钮太多太花**：一页最多一个 primary 按钮，其他都是 ghost。
- **仿得太像真实产品**：原型需要"一眼能看懂是原型"，过度追求真实反而让下一轮 AI 难以区分"这是示意还是数据"。加个右上角小 badge 写"DEMO / 原型"是个好办法。
- **忘了给下一轮 AI 留语义**：即便是产品外壳，内容里的数据也要带 `data-*` 属性——毕竟下一轮 AI 可能要基于这个原型改进功能。
