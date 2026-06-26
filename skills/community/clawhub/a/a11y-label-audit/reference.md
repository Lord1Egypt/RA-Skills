# 无障碍标签审查 — 详细参考

## WCAG 指南对照

本技能以 **WCAG 2.1 AA 级别**合规为目标，重点关注以下成功准则：

| 准则编号 | 名称 | 对应规则 |
|----------|------|----------|
| 1.1.1 | 非文本内容 | img-alt-a11y |
| 1.3.1 | 信息与关系 | form-label-a11y |
| 2.1.1 | 键盘可操作 | div-button-a11y |
| 2.4.6 | 标题和标签 | form-label-a11y |
| 4.1.2 | 名称、角色、值 | icon-button-a11y、div-button-a11y、dialog-a11y |
| 4.1.3 | 状态消息 | live-region-a11y |

## 规则详细说明

### icon-button-a11y

**什么算纯图标按钮？**

满足以下条件的元素属于纯图标按钮：
- 有 `onClick`（或等效的事件处理器）
- 唯一的子内容是图标组件或 SVG
- 不存在可见的文本内容（既没有子文本，也没有充当可访问名称的 `title` 属性）

**常见需要搜索的图标组件名：**
```
YbIcon、Icon、SvgIcon、FontIcon、IconButton（无文本）、
<svg> 内联、<img> 用作图标、<i className="icon-*">
```

**标签推断策略：**
1. `type` / `name` / `icon` 属性 → 转换 `ic_close_16` → "关闭"
2. 父组件语义 → `SearchBar` 中的关闭图标 → "清除搜索"
3. 附近的注释或变量名 → `handleDelete` → "删除"
4. 无法确定时，使用 TODO 注释：`aria-label={t('TODO: 描述此操作')}`

**边界情况：**
- 图标本身设置了 `aria-hidden="true"` 是合理的，前提是父元素有可访问名称
- 图标 + 视觉隐藏文本（`<span className="sr-only">`）已经是无障碍的 — 不需要标记
- SVG 上的 `title` 属性在大多数浏览器中提供可访问名称 — 如果存在则不标记

---

### div-button-a11y

**完整修复模式：**

```tsx
// 修复前
<div className={styles.item} onClick={handleClick}>
  <span>{label}</span>
</div>

// 修复后
<div
  className={styles.item}
  onClick={handleClick}
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick(e as any);
    }
  }}
>
  <span>{label}</span>
</div>
```

**不需要标记的情况：**
- 元素已经有 `role="button"` + `tabIndex` + 键盘处理器
- 元素内部使用了 `<button>` 或 `<a>`（div 只是外层容器）
- 元素有 `role="link"` 或 `role="tab"` 等（不同的交互模式）
- 元素纯粹是装饰性/视觉容器，实际的交互元素在子级中

**键盘处理注意事项：**
- **Enter**：应激活按钮（等同于点击）
- **Space**：应激活按钮并调用 `e.preventDefault()` 防止页面滚动
- 如果 `onClick` 处理器期望 `MouseEvent`，需要对键盘事件做类型转换或抽取处理逻辑

---

### img-alt-a11y

**判断决策树：**

```
图片是装饰性的（边框、占位符、背景纹理）？
  → alt="" + role="presentation"（或改用 CSS background-image）
图片是表达含义的图标？
  → alt="[图标代表的动作或概念]"
图片是照片/插图？
  → alt="[描述核心内容]"
图片是图表/数据可视化？
  → alt="[图表展示的要点摘要]" + 在别处提供详细描述
图片是 Logo？
  → alt="[公司名称] Logo"
```

**需要标记的错误 alt 值：**
- `alt="image"`、`alt="photo"`、`alt="picture"`、`alt="icon"`
- `alt={src}` 或 `alt={url}`（用文件名当 alt）
- `alt="undefined"`、`alt="null"`

---

### form-label-a11y

**关联方式（按优先级排序）：**

1. **包裹式 `<label>`**：`<label>姓名 <input /></label>`
2. **`htmlFor` / `id` 关联**：`<label htmlFor="name">姓名</label> <input id="name" />`
3. **`aria-labelledby`**：`<h2 id="title">搜索</h2> <input aria-labelledby="title" />`
4. **`aria-label`**：`<input aria-label="搜索" />`（最后选择 — 不可见）

**特殊情况：**
- 搜索输入框：使用 `aria-label={t('搜索')}` 是可接受的，因为搜索图标提供了视觉提示
- 隐藏输入框（`type="hidden"`）：不需要标签
- 表单中的按钮：按钮文本本身就是标签，不需要额外标注

---

### dialog-a11y

**必需属性检查清单：**

| 属性 | 用途 | 来源 |
|------|------|------|
| `role="dialog"` 或 `role="alertdialog"` | 语义角色 | 通常由库设置 |
| `aria-modal="true"` | 表示模态行为 | 通常由库设置 |
| `aria-labelledby="dialog-title-id"` | 指向标题 | 需逐个使用场景验证 |
| `aria-describedby`（可选） | 指向描述内容 | 有则更好 |

**焦点管理检查项：**
- 打开弹窗时焦点应移入弹窗内（到第一个可聚焦元素或弹窗本身）
- 弹窗打开期间焦点应被捕获在弹窗内
- 关闭弹窗时焦点应归还到触发元素
- Esc 键应关闭弹窗

**TDesign / YbcDialog 注意事项：**
- TDesign `Dialog` 默认设置 `role="dialog"` 和 `aria-modal`
- `YbcDialog` 封装了 TDesign — 需验证 props 是否被透传
- 检查 `header` prop 的内容是否有 id，以及 `aria-labelledby` 是否指向它

---

### live-region-a11y

**`aria-live` 值的选择指南：**

| 场景 | 值 | 理由 |
|------|------|------|
| Toast / Snackbar 通知 | `polite` | 非紧急，等用户操作完再播报 |
| 表单验证错误 | `assertive` | 用户需要立即知道 |
| 加载中提示 | `polite` + `aria-busy="true"` | 信息性提示 |
| 聊天新消息 | `polite` | 不打断当前阅读 |
| 倒计时/计时器 | `off` 或带节流的 `polite` | 避免过于频繁 |
| 错误横幅/警告 | `assertive` + `role="alert"` | 关键信息 |
| 成功提示 | `polite` + `role="status"` | 确认反馈 |

**实现模式：**

```tsx
// 修复前：toast 仅视觉展示
<div className="toast">{message}</div>

// 修复后：屏幕阅读器可播报
<div className="toast" role="status" aria-live="polite" aria-atomic="true">
  {message}
</div>
```

**注意事项：**
- `aria-live` 区域必须在内容变化之前就存在于 DOM 中 — 动态插入带内容的 live region 不会触发播报
- 优先使用 `aria-atomic="true"` 以便整个区域被重新播报，而非仅播报变化的文本节点
- 不要在大型容器（整个页面区块）上设置 `aria-live` — 会造成过多干扰

## 跨平台兼容性详细参考

### 各引擎 ARIA 支持差异表

| ARIA 特性 | Chromium (桌面/扩展) | WKWebView (macOS) | WebView2 (Win) | X5 (微信) | 小程序 WebView |
|-----------|---------------------|-------------------|----------------|-----------|---------------|
| `aria-label` | 完整 | 完整 | 完整 | 部分（仅常见元素） | 部分 |
| `aria-labelledby` | 完整 | 完整 | 完整 | 部分 | 不稳定 |
| `aria-describedby` | 完整 | 完整 | 完整 | 部分 | 不稳定 |
| `aria-live="polite"` | 完整 | 完整 | 完整 | 不可靠 | 不可靠 |
| `aria-live="assertive"` | 完整 | 完整 | 完整 | 不可靠 | 不可靠 |
| `aria-modal` | 完整 | 完整 | 完整 | 部分 | 部分 |
| `role="button"` | 完整 | 完整 | 完整 | 完整 | 完整 |
| `role="status"` | 完整 | 完整 | 完整 | 不稳定 | 不支持 |
| `role="alert"` | 完整 | 完整 | 完整 | 不稳定 | 不支持 |
| `role="feed"` | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| `inert` 属性 | Chrome 102+ | Safari 15.5+ | 支持 | 不支持 | 不支持 |
| 原生 `<dialog>` | Chrome 37+ | Safari 15.4+ | 支持 | 不稳定 | 不支持 |
| `:focus-visible` | Chrome 86+ | Safari 15.4+ | 支持 | 不支持 | 不支持 |
| `scrollend` 事件 | Chrome 114+ | Safari 不支持 | 支持 | 不支持 | 不支持 |

### `inert` 属性回退方案

```tsx
// 如果使用 inert，需提供回退
const supportsInert = typeof HTMLElement !== 'undefined' && 'inert' in HTMLElement.prototype;

// 修复前 — 仅用 inert
<div inert={isModalOpen ? true : undefined}>
  {content}
</div>

// 修复后 — 兼容回退
<div
  {...(supportsInert
    ? { inert: isModalOpen ? true : undefined }
    : {
        'aria-hidden': isModalOpen ? 'true' : undefined,
        tabIndex: isModalOpen ? -1 : undefined,
      }
  )}
>
  {content}
</div>
```

### 原生 `<dialog>` 回退方案

不要在本项目中直接使用原生 `<dialog>` 元素。应统一使用 `YbcDialog`（封装了 TDesign `Dialog`），它在所有目标平台上行为一致。

如果必须使用原生 `<dialog>`，检查支持情况：

```tsx
const supportsDialog = typeof HTMLDialogElement !== 'undefined';
```

### `:focus-visible` 回退方案

```scss
// 兼容写法：先写 :focus 基础样式，再用 :focus:not(:focus-visible) 移除
.interactive-element {
  &:focus {
    outline: 2px solid var(--brand-color);
    outline-offset: 2px;
  }

  // 支持 :focus-visible 的浏览器中，鼠标点击不显示 outline
  &:focus:not(:focus-visible) {
    outline: none;
  }

  &:focus-visible {
    outline: 2px solid var(--brand-color);
    outline-offset: 2px;
  }
}
```

### 微信/QQ 内置浏览器特殊处理

**已知限制：**
- X5 内核对 `aria-live` 区域的更新播报不可靠
- `document.activeElement` 在某些场景返回 `null` 或 `<body>`
- 自定义 `role` 值可能被忽略，但语义化原生元素（`<button>`、`<a>`）可正常工作
- CSS `:focus-visible` 不生效，`:focus` 生效

**推荐策略：**
1. 对关键交互使用原生语义元素，不依赖 `role` 属性
2. 对动态内容同时使用视觉反馈（动画/颜色变化），不仅依赖 `aria-live`
3. 焦点管理使用库组件内置能力，不直接操作 DOM

### 小程序 WebView 沙箱限制

**已知限制：**
- `focus()` 调用可能被沙箱拦截
- `MutationObserver` 对 ARIA 属性变化的监听不可靠
- 无法使用 `inert`、原生 `<dialog>`
- `tabIndex` 在自定义元素上行为不一致

**推荐策略：**
1. 检查 `isMpWebview` 环境变量，为小程序提供简化的焦点管理
2. 避免复杂的焦点捕获逻辑，依赖库组件
3. 交互控件必须使用原生 HTML 元素

### SSR 水合与无障碍的交叉问题

项目中大量 `<img>` 元素设置了 `suppressHydrationWarning`（主要解决远程 URL / 时间戳不一致问题）。审查时注意：

1. 设置了 `suppressHydrationWarning` 的 `<img>` 仍需有正确的 `alt`
2. SSR 和 CSR 渲染的 `aria-label` 值应保持一致，避免水合不匹配
3. 如果 `aria-label` 依赖客户端数据（如用户名），使用 `suppressHydrationWarning` 或在 `useEffect` 中设置

### 平台环境检测工具

项目中已有的环境检测函数，修复兼容性问题时可直接使用：

```tsx
// 桌面端判断
import { isDesktop } from '@tencent/yb-util/src/common/environment/is-yuanbao-app';

// 微信小程序 WebView 判断
import { isMpWebview } from '@tencent/yb-util/src/utils/detect-env';

// 微信内置浏览器判断
// window.__wxjs_environment === 'miniprogram'
// UA 包含 'MicroMessenger'

// Tauri 桌面端判断
// window.__TAURI__
```

## Grep 搜索模式速查

```bash
# 纯图标按钮
rg 'onClick.*<(YbIcon|Icon|SvgIcon)' --type tsx
rg '<(YbIcon|Icon|SvgIcon)' --type tsx  # 再检查父级是否有 onClick

# div 模拟按钮
rg '<(div|span)[^>]*onClick' --type tsx

# 缺失 alt
rg '<img\b' --type tsx  # 再检查是否有 alt=

# 未标注的表单元素
rg '<(input|textarea|select)\b' --type tsx  # 再检查是否有 aria-label 或 label

# 弹窗
rg '<(Dialog|Modal|YbcDialog|Drawer)\b' --type tsx

# 动态内容（潜在的 live region）
rg '(toast|Toast|Notification|loading|error[Mm]sg|error[Mm]essage|successToast|errorToast)' --type tsx
```
