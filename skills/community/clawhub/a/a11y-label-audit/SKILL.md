---
name: a11y-label-audit
description: >-
  扫描 React/TSX 组件中缺失的无障碍标签并自动修复。
  检测纯图标按钮缺少 aria-label、div/span 模拟按钮缺少 role 和键盘交互、
  图片缺少有意义的 alt 文本、表单元素缺少 label 关联、
  弹窗缺少 aria-modal 和焦点管理、动态内容缺少 aria-live 等问题。
  同时考虑跨平台兼容性问题：Tauri 桌面端（WKWebView/WebView2）、
  微信/QQ 内置浏览器、Chrome 扩展、受限 WebView 等不同引擎对
  ARIA 属性和焦点管理的支持差异。
  当用户提到无障碍审查、a11y 检查、WCAG 合规、添加 aria 标签、
  屏幕阅读器支持、无障碍改进、兼容性问题时使用此技能。
---

# 无障碍标签审查与自动修复

扫描当前目录或指定文件中 React/TSX 组件缺失的无障碍（a11y）标注，并自动修复。

## 快速开始

1. **确定扫描范围** — 用户可提供文件、目录或组件名。默认：当前工作目录。
2. **扫描** — 按照下方的检测规则搜索无障碍违规项。
3. **报告** — 按文件分组列出所有发现，包含行号和违规类型。
4. **修复** — 自动应用修复，保留现有代码风格和缩进。

## 检测规则

### 规则 1：纯图标按钮（icon-button-a11y）

**检测**：可点击元素中仅包含图标组件（如 `<YbIcon>`、`<Icon>`、`<SvgIcon>`、`<img>`），没有可见文本，也没有 `aria-label` / `aria-labelledby`。

**修复**：根据图标的 `type` / `name` 属性或上下文推断标签内容，添加 `aria-label`。如果项目使用 i18n 函数（`t()`），用其包裹标签文本。

### 规则 2：div 模拟按钮（div-button-a11y）

**检测**：`<div>` 或 `<span>` 带有 `onClick` 处理器但缺少：
- `role="button"`
- `tabIndex={0}`
- `onKeyDown` / `onKeyPress` 键盘事件处理（Enter/Space 触发点击）

**修复**：添加 `role="button"`、`tabIndex={0}`，以及一个在 Enter/Space 时触发点击的 `onKeyDown` 处理器。

### 规则 3：图片 alt 文本（img-alt-a11y）

**检测**：`<img>` 元素中：
- `alt` 属性完全缺失
- `alt` 为无意义值，如 `alt="image"`、`alt="photo"`、`alt="picture"`、`alt="icon"`

装饰性图片使用 `alt=""` 是**合法的**，不应标记。

**修复**：根据上下文（文件名、周围文本、父组件语义）添加描述性 `alt`。如确为装饰性图片，添加 `alt=""` 和 `role="presentation"`。

### 规则 4：表单标签（form-label-a11y）

**检测**：`<input>`、`<textarea>`、`<select>` 没有关联的 `<label>`（通过 `htmlFor` / 包裹方式）或 `aria-label` / `aria-labelledby`。

**修复**：根据 placeholder、附近标题或父级上下文推断文本，添加 `aria-label`。可行时优先使用显式的 `<label>` 包裹。

### 规则 5：弹窗/对话框无障碍（dialog-a11y）

**检测**：弹窗/对话框组件（如 `Dialog`、`Modal`、`YbcDialog`、`Drawer`）缺少：
- `aria-modal="true"`（如果底层库未设置）
- `aria-labelledby` 或 `aria-label` 指向对话框标题
- 焦点捕获 / 焦点归还逻辑

**修复**：添加指向标题元素 id 的 `aria-labelledby`，或在无标题元素时添加 `aria-label`。焦点管理问题以警告形式标注。

### 规则 6：实时区域（live-region-a11y）

**检测**：动态内容区域（Toast 通知、加载状态、错误提示、聊天消息）缺少 `aria-live`、`aria-atomic` 或 `role="status"` / `role="alert"`。

**修复**：添加合适的 `aria-live="polite"`（默认）或 `aria-live="assertive"`（错误/警告），以及需要整体重新播报时添加 `aria-atomic="true"`。

## 扫描工作流

```
任务进度：
- [ ] 步骤 1：确定扫描范围（文件/目录）
- [ ] 步骤 2：按 7 条规则搜索违规项（含兼容性）
- [ ] 步骤 3：汇总审查报告
- [ ] 步骤 4：应用自动修复
- [ ] 步骤 5：验证修复未引入新问题
```

### 步骤 1：确定扫描范围

使用 Glob 查找目标目录下所有 `.tsx` 文件：
```
**/*.tsx
```

排除 `node_modules`、`dist`、`build`、`.next`、`__tests__`、`*.test.tsx`、`*.spec.tsx`。

### 步骤 2：搜索违规项

针对每条规则，使用 Grep 查找潜在违规项：

**纯图标按钮：**
```
onClick.*<(YbIcon|Icon|SvgIcon)
```
然后验证父级可点击元素是否存在 `aria-label`。

**div 模拟按钮：**
```
<(div|span)[\s\S]*?onClick
```
然后验证是否存在 `role="button"` 和 `tabIndex`。

**缺失 alt：**
```
<img[\s\S]*?(?!alt=)
```

**未标注的表单元素：**
```
<(input|textarea|select)[\s\S]*?(?!aria-label)
```

**未标注的弹窗：**
```
<(Dialog|Modal|YbcDialog|Drawer)
```
然后验证是否存在 `aria-labelledby` 或 `aria-label`。

**缺少实时区域标注的动态内容：**
```
(toast|Toast|notification|Notification|loading|Loading|errorMsg|errorMessage)
```
然后验证附近是否存在 `aria-live` 或 `role="alert"` / `role="status"`。

**兼容性问题：**
```
inert[^a-zA-Z]
```
检查是否有 `inert` 回退。
```
:focus-visible
```
检查是否有 `:focus` 基础样式回退。
```
suppressHydrationWarning
```
检查同一元素是否有正确的 `alt` / `aria-label`。
```
role="(status|alert|feed)"
```
在微信/QQ 环境中这些 role 不可靠，检查是否有语义化元素替代或多通道回退。

### 步骤 3：汇总报告

按以下格式输出审查结果：

```
## 无障碍审查报告

### 文件：src/components/Example.tsx

| 行号 | 规则 | 问题 | 建议修复 |
|------|------|------|----------|
| 42 | icon-button-a11y | onClick div 中的 `<YbIcon>` 缺少 aria-label | 添加 `aria-label={t('关闭')}` |
| 78 | div-button-a11y | `<div onClick>` 缺少 role 和键盘交互 | 添加 `role="button"` tabIndex={0} onKeyDown |
```

### 步骤 4：应用修复

使用 StrReplace 逐项应用修复。保留：
- 现有缩进风格（空格 vs Tab）
- 代码格式（引号风格与周围代码一致）
- i18n 包裹：若项目使用 `t()` / `useTranslation`，用其包裹标签文本

### 步骤 5：验证

修复后，对修改过的文件运行 ReadLints，检查是否引入了新错误。

## 框架特定注意事项

### TDesign 组件

TDesign 的 `Button`、`Dialog`、`Input` 等通常内部处理了基本无障碍。重点关注：
- 覆盖或遗漏了内置属性的自定义包装组件
- `content` 或 `children` 等提供隐式标签的 props

### @tencent/yb-component

`YBButton`、`YbcDialog` 是薄层封装。检查 a11y props 是否被正确透传。如果封装层吞掉了 `aria-*` props，需要标记。

### Next.js `<Image>`

Next.js 的 `Image` 组件默认要求 `alt` 并会发出警告。仍需验证 alt 文本是否有实际意义。

## 规则 7：跨平台兼容性（compat-a11y）

本项目运行在多种平台上，不同引擎对无障碍 API 的支持存在差异，修复时必须考虑兼容性。

### 目标平台一览

| 平台 | 引擎 | 无障碍支持等级 |
|------|------|----------------|
| 桌面端（Tauri macOS） | WKWebView | 较好，VoiceOver 支持完整 |
| 桌面端（Tauri Windows） | WebView2 (Chromium) | 好，NVDA/JAWS 支持完整 |
| 桌面端（Tauri Linux） | WebKitGTK | 一般，Orca 支持有限 |
| Chrome/Edge 扩展 | Chromium | 好 |
| 微信内置浏览器 | 自研 X5 / 系统 WebView | 较差，部分 ARIA 属性被忽略 |
| QQ 内置浏览器 | MQQBrowser 内核 | 较差 |
| PC 微信 | Chromium 内嵌 | 一般 |
| 企业微信 | 系统 WebView | 一般 |
| 小程序 WebView | 受限沙箱 | 差，焦点管理受限 |

### 兼容性检测规则

**7a. `inert` 属性兼容（compat-inert）**

`inert` 属性在旧版 WebView 中不被支持。如果使用了 `inert`，需要同时提供 polyfill 或回退方案（`aria-hidden="true"` + `tabIndex={-1}`）。

**7b. `<dialog>` 元素兼容（compat-dialog）**

原生 `<dialog>` 元素在 X5 内核、旧版 WKWebView、小程序 WebView 中可能不受支持。优先使用库组件（TDesign `Dialog` / `YbcDialog`）而非原生 `<dialog>`。

**7c. `focus-visible` 伪类兼容（compat-focus-visible）**

`:focus-visible` 在微信 X5 内核中可能不生效。需要同时保留 `:focus` 样式作为回退：

```css
.btn:focus { outline: 2px solid var(--focus-color); }
.btn:focus:not(:focus-visible) { outline: none; }
.btn:focus-visible { outline: 2px solid var(--focus-color); }
```

**7d. `aria-live` 在受限 WebView 中的兼容（compat-live-region）**

微信/QQ 内置浏览器中 `aria-live` 可能不触发屏幕阅读器播报。对于关键通知，除了 ARIA 标注外，建议同时提供视觉反馈（如 Toast 动画）和触觉反馈（如震动 API）作为多通道回退。

**7e. 焦点管理在小程序 WebView 中的限制（compat-focus-trap）**

小程序 WebView 沙箱中 `document.activeElement` 和程序化 `focus()` 行为不一致。弹窗焦点捕获应通过库组件实现，避免直接操作 DOM focus。检查是否存在 `isMpWebview` 条件分支来处理此类差异。

**7f. `role` 属性在 X5 内核中的支持（compat-role）**

微信 X5 内核对某些 ARIA role（如 `role="status"`、`role="alert"`、`role="feed"`）支持不完整。在这些环境中，优先使用语义化 HTML 元素（`<button>` 替代 `role="button"`、`<nav>` 替代 `role="navigation"`）。

**7g. `suppressHydrationWarning` 与无障碍的交叉（compat-hydration）**

项目中大量使用 `suppressHydrationWarning`。检查设置了此属性的 `<img>` 元素是否同时有正确的 `alt`，防止 SSR/CSR 不一致导致 alt 文本丢失。

### 兼容性修复策略

1. **优先使用语义化 HTML** — 原生 `<button>`、`<a>`、`<input>` 在所有引擎中的无障碍支持都优于 ARIA 标注的 `<div>`
2. **ARIA 作为增强而非依赖** — 先确保语义化，再用 ARIA 补充
3. **多通道反馈** — 不依赖单一的辅助技术 API，结合视觉、听觉、触觉反馈
4. **平台条件分支** — 利用项目现有的 `isDesktop`、`isMpWebview`、`isWeChat` 等环境检测，为受限平台提供替代方案
5. **渐进增强** — 使用特性检测（`if ('inert' in HTMLElement.prototype)`）而非 UA 嗅探

## 修复优先级

当存在大量违规时，按以下顺序修复（影响从高到低）：
1. **交互控件**缺少标签（纯图标按钮、div 模拟按钮）— 完全阻碍使用
2. **表单**缺少标签 — 无法输入
3. **图片**缺少 alt — 信息丢失
4. **弹窗**缺少 aria 属性 — 导航混乱
5. **实时区域** — 降低实时感知

## 补充资料

- 规则的详细说明和边界情况，参见 [reference.md](reference.md)
- 修复前后的代码示例，参见 [examples.md](examples.md)
