# CSS 面试题库

## 初级

### 题目1：什么是 BFC？如何触发 BFC？
**考察点：** BFC 概念、触发条件、实际应用场景

**参考答案：**
BFC（Block Formatting Context，块级格式化上下文）是一个独立的渲染区域，内部元素的布局不影响外部。

触发 BFC 的常见方式：
- `overflow` 不为 `visible`（如 `hidden`、`auto`）
- `display: flex`、`display: grid`
- `position: absolute` 或 `position: fixed`
- `float` 不为 `none`

实际应用：清除浮动、防止 margin 塌陷
```css
/* 清除浮动 */
.container {
  overflow: hidden; /* 触发 BFC */
}

/* 防止父子 margin 塌陷 */
.parent {
  overflow: hidden;
}
```

---

### 题目2：CSS 选择器优先级如何计算？
**考察点：** 优先级权重、!important、继承

**参考答案：**
优先级从高到低：
1. `!important`（覆盖一切）
2. 行内样式（1000）
3. ID 选择器（0100）
4. 类/伪类/属性选择器（0010）
5. 标签/伪元素选择器（0001）
6. 通配符/继承（0000）

```css
/* 优先级示例 */
#app .title { color: red; }   /* 0110 */
.title { color: blue; }       /* 0010 */
/* 最终 #app .title 优先级更高，显示红色 */

/* !important 慎用 */
.title { color: green !important; } /* 最高优先级 */
```

---

### 题目3：Flexbox 中 `flex: 1` 是什么意思？
**考察点：** flex 缩写属性、flex-grow/shrink/basis

**参考答案：**
`flex: 1` 等价于 `flex: 1 1 0%`，即：
- `flex-grow: 1`：剩余空间等比分配
- `flex-shrink: 1`：空间不足时等比收缩
- `flex-basis: 0%`：初始尺寸为0，完全依赖 grow 分配

```css
.container {
  display: flex;
}
.item {
  flex: 1; /* 等分容器宽度 */
}
.item-double {
  flex: 2; /* 占其他 flex:1 元素的2倍空间 */
}
```

---

## 中级

### 题目4：用 Grid 实现一个经典三栏布局（左右固定，中间自适应）
**考察点：** Grid 布局语法、fr 单位、grid-template-columns

**参考答案：**
```css
.layout {
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto;
  gap: 16px;
  min-height: 100vh;
}

.left { background: #f0f0f0; }
.main { background: #fff; }
.right { background: #f0f0f0; }
```
```html
<div class="layout">
  <aside class="left">左侧</aside>
  <main class="main">主内容</main>
  <aside class="right">右侧</aside>
</div>
```
`fr` 是弹性单位，`1fr` 会占用除固定宽度外的剩余空间。

---

### 题目5：CSS 动画 `transition` 和 `animation` 的区别？
**考察点：** 触发方式、关键帧、性能优化

**参考答案：**
| 对比项 | transition | animation |
|--------|-----------|-----------|
| 触发 | 需要状态变化触发 | 可自动播放 |
| 关键帧 | 只有起止两帧 | 可定义多个关键帧 |
| 循环 | 不支持 | 支持 iteration-count |

```css
/* transition：hover 触发 */
.btn {
  background: blue;
  transition: background 0.3s ease;
}
.btn:hover { background: red; }

/* animation：自动播放 */
@keyframes spin {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loader {
  animation: spin 1s linear infinite;
}
```
性能建议：优先使用 `transform` 和 `opacity`，避免触发重排。

---

### 题目6：什么是响应式设计？常用媒体查询断点如何设置？
**考察点：** 媒体查询、移动优先、常见断点

**参考答案：**
响应式设计让页面在不同设备上自适应展示，核心是媒体查询（Media Queries）。

移动优先策略（推荐）：
```css
/* 基础样式：移动端 */
.container { padding: 16px; }

/* 平板 ≥ 768px */
@media (min-width: 768px) {
  .container { padding: 24px; }
}

/* 桌面 ≥ 1024px */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px;
  }
}

/* 高分辨率屏幕 */
@media (-webkit-min-device-pixel-ratio: 2) {
  .logo { background-image: url('logo@2x.png'); }
}
```

---

## 高级

### 题目7：CSS 变量（自定义属性）的工作原理及应用场景
**考察点：** 变量作用域、动态更新、主题切换

**参考答案：**
CSS 变量以 `--` 开头，通过 `var()` 引用，具有级联和继承特性。

```css
/* 定义全局变量 */
:root {
  --color-primary: #3498db;
  --spacing-md: 16px;
  --border-radius: 8px;
}

/* 使用变量 */
.btn {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
}

/* 暗色主题：覆盖变量 */
[data-theme="dark"] {
  --color-primary: #2980b9;
}

/* JS 动态修改 */
```
```javascript
// 运行时修改主题色
document.documentElement.style.setProperty('--color-primary', '#e74c3c');

// 读取变量值
const color = getComputedStyle(document.documentElement)
  .getPropertyValue('--color-primary');
```
优势：比 Sass 变量更灵活，可在运行时修改，支持 JS 交互。

---

### 题目8：解释 CSS 层叠上下文（Stacking Context）与 z-index 的关系
**考察点：** 层叠上下文创建条件、z-index 失效原因、绘制顺序

**参考答案：**
层叠上下文是一个独立的渲染层，内部元素的 `z-index` 只在该上下文内比较。

创建层叠上下文的条件：
- `position` 非 `static` 且 `z-index` 非 `auto`
- `opacity < 1`
- `transform`、`filter`、`will-change` 非 `none`
- `isolation: isolate`

```css
/* z-index 失效场景 */
.parent-a { position: relative; z-index: 1; }
.child-a  { position: relative; z-index: 9999; } /* 被父级z-index限制 */

.parent-b { position: relative; z-index: 2; }
.child-b  { position: relative; z-index: 1; }
/* child-b 始终在 child-a 上方，因为 parent-b > parent-a */

/* 用 isolation 创建隔离层 */
.modal-backdrop {
  isolation: isolate;
}
```

---

### 题目9：如何实现 CSS 容器查询（Container Queries）？与媒体查询有何不同？
**考察点：** Container Queries 语法、与媒体查询的区别、组件化思维

**参考答案：**
容器查询让组件根据**父容器**尺寸而非视口宽度来响应，更适合组件化开发。

```css
/* 定义容器 */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* 容器查询 */
@container card (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }
}

/* 对比媒体查询 */
@media (min-width: 768px) {
  /* 依赖视口，多列布局中难以控制单个组件 */
  .card { flex-direction: row; }
}
```
**核心区别：** 媒体查询基于视口，容器查询基于父容器，后者更适合可复用组件。
