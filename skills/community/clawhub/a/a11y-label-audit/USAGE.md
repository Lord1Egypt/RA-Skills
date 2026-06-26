# a11y-label-audit 使用说明

## 一、简介

`a11y-label-audit` 是一个 Cursor AI Skill，用于**自动扫描和修复**前端项目中缺失的无障碍（Accessibility / a11y）标签。

它能在几分钟内完成人工可能需要数小时的无障碍审查工作：找出所有缺少 `aria-label`、`role`、`alt` 等属性的元素，生成审查报告，并逐项自动修复。

---

## 二、安装

将 `a11y-label-audit` 文件夹放到以下任一位置：

```
# 全局安装（所有项目可用）
~/.cursor/skills/a11y-label-audit/

# 项目级安装（仅当前项目可用）
<项目根目录>/.cursor/skills/a11y-label-audit/
```

文件夹结构：

```
a11y-label-audit/
├── SKILL.md         ← 核心技能文件（必需）
├── reference.md     ← 规则详细说明和边界情况
├── examples.md      ← 修复前后代码示例
├── clawhub.json     ← ClawHub 发布元数据
├── CHANGELOG.md     ← 版本变更日志
├── README.md        ← 项目说明
└── USAGE.md         ← 本使用说明
```

---

## 三、触发方式

### 方式 1：自然语言触发（推荐）

在 Cursor 对话中直接说：

> "帮我检查这个文件的无障碍问题"  
> "扫描 src/components/ 下的 a11y 标签"  
> "这个项目的 WCAG 合规性怎么样"  
> "给这些按钮加上 aria-label"  

Skill 会根据关键词自动匹配并启动。

### 方式 2：手动附加 Skill

1. 在 Cursor 聊天输入框中输入 `@`
2. 选择 `a11y-label-audit`
3. 输入你的指令

### 方式 3：指定扫描目标

```
@a11y-label-audit 扫描 src/components/bot-setting/
@a11y-label-audit 修复 src/components/my-bot/dialogs/
@a11y-label-audit 检查这个文件
```

---

## 四、工作流程

Skill 启动后会按以下 5 个步骤自动执行：

```
┌───────────────────────────────────────────────┐
│ 步骤 1：确定扫描范围                             │
│   └ 查找目标目录下所有 .tsx / .html 文件          │
│     （自动排除 node_modules, dist, .next 等）     │
├───────────────────────────────────────────────┤
│ 步骤 2：按 7 条规则搜索违规项                     │
│   └ 使用 Grep 逐条搜索潜在问题                   │
│     并通过上下文验证是否为真正的违规               │
├───────────────────────────────────────────────┤
│ 步骤 3：汇总审查报告                             │
│   └ 按文件分组输出表格：行号 | 规则 | 问题 | 建议  │
├───────────────────────────────────────────────┤
│ 步骤 4：应用自动修复                             │
│   └ 逐项修复，保留代码风格、缩进和 i18n 包裹       │
├───────────────────────────────────────────────┤
│ 步骤 5：验证修复                                │
│   └ 对修改过的文件运行 Lint 检查                  │
│     确保没有引入新错误                           │
└───────────────────────────────────────────────┘
```

---

## 五、检测规则一览

### 6 条核心规则

| # | 规则 ID | 检测内容 | 严重度 |
|---|---------|----------|--------|
| 1 | `icon-button-a11y` | 纯图标按钮（只有 SVG/图标，没有文本）缺少 `aria-label` | 🔴 高 |
| 2 | `div-button-a11y` | `<div>` / `<span>` 带 `onClick` 但缺少 `role="button"`、`tabIndex`、键盘事件 | 🔴 高 |
| 3 | `img-alt-a11y` | `<img>` 缺少 `alt` 或 `alt` 为无意义文本（"image"、"photo" 等） | 🟡 中 |
| 4 | `form-label-a11y` | `<input>` / `<select>` / `<textarea>` 缺少 `<label>` 或 `aria-label` | 🔴 高 |
| 5 | `dialog-a11y` | 弹窗/对话框缺少 `aria-modal`、`aria-labelledby`、焦点管理 | 🟡 中 |
| 6 | `live-region-a11y` | 动态内容（Toast、加载状态、错误提示）缺少 `aria-live` | 🟠 中 |

### 第 7 条跨平台兼容性规则

| 子规则 | 问题 | 影响平台 |
|--------|------|----------|
| `compat-inert` | 使用 `inert` 属性无回退 | X5、小程序 WebView |
| `compat-dialog` | 使用原生 `<dialog>` 无替代 | X5、旧版 WKWebView |
| `compat-focus-visible` | 仅用 `:focus-visible` 无 `:focus` 回退 | 微信 X5 |
| `compat-live-region` | `aria-live` 不被播报 | 微信/QQ 内置浏览器 |
| `compat-focus-trap` | `focus()` 行为不一致 | 小程序 WebView |
| `compat-role` | `role="status"` 等不被识别 | X5 内核 |
| `compat-hydration` | `suppressHydrationWarning` 元素的 `alt` 丢失 | SSR 项目 |

---

## 六、审查报告示例

Skill 扫描完成后会输出如下格式的报告：

```
## 无障碍审查报告

### 文件：src/components/bot-setting/index.tsx

| 行号 | 规则               | 问题                                          | 建议修复                                      |
|------|--------------------|-----------------------------------------------|-----------------------------------------------|
| 42   | icon-button-a11y   | onClick div 中的 <YbIcon> 缺少 aria-label      | 添加 aria-label={t('关闭')}                    |
| 78   | div-button-a11y    | <div onClick> 缺少 role 和键盘交互              | 添加 role="button" tabIndex={0} onKeyDown      |
| 120  | img-alt-a11y       | <img> 的 alt="image" 无意义                    | 替换为 alt="用户头像"                           |
| 195  | form-label-a11y    | <input placeholder="搜索"> 缺少 aria-label     | 添加 aria-label={t('搜索对话')}                 |
| 230  | dialog-a11y        | <Dialog> 缺少 aria-labelledby                  | 添加 aria-labelledby 指向标题 id                |
| 280  | live-region-a11y   | Toast 成功提示缺少 aria-live                    | 添加 role="status" aria-live="polite"           |
| 310  | compat-inert       | 使用 inert 无回退                               | 添加 aria-hidden="true" 作为 X5 回退            |

共发现 7 处违规，已全部修复。
```

---

## 七、修复示例

### 纯图标按钮

**修复前：**
```tsx
<div className={styles.closeBtn} onClick={onClose}>
  <YbIcon type="ic_close_16" />
</div>
```

**修复后：**
```tsx
<div
  className={styles.closeBtn}
  onClick={onClose}
  role="button"
  tabIndex={0}
  aria-label={t('关闭')}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClose();
    }
  }}
>
  <YbIcon type="ic_close_16" aria-hidden="true" />
</div>
```

### 表单元素

**修复前：**
```tsx
<input type="text" placeholder="请输入用户名" />
```

**修复后：**
```tsx
<input type="text" placeholder="请输入用户名" aria-label={t('用户名')} />
```

### 弹窗对话框

**修复前：**
```tsx
<Dialog visible={visible} onClose={onClose}>
  <div className={styles.title}>确认删除</div>
  ...
</Dialog>
```

**修复后：**
```tsx
<Dialog
  visible={visible}
  onClose={onClose}
  aria-labelledby="delete-dialog-title"
  aria-modal="true"
>
  <div id="delete-dialog-title" className={styles.title}>确认删除</div>
  ...
</Dialog>
```

---

## 八、修复优先级

当一个项目中存在大量违规时，Skill 会按照以下优先级排序修复：

```
优先级 1（最高）：交互控件缺少标签
   → 纯图标按钮、div 模拟按钮（完全阻碍辅助技术用户使用）

优先级 2：表单缺少标签
   → 无法输入（屏幕阅读器用户不知道输入什么）

优先级 3：图片缺少 alt
   → 信息丢失（图片内容无法传达）

优先级 4：弹窗缺少 aria 属性
   → 导航混乱（用户不知道进入了弹窗）

优先级 5（最低）：实时区域
   → 降低实时感知（但不影响基本操作）
```

---

## 九、支持的项目类型

| 项目类型 | 支持程度 |
|----------|----------|
| React + TypeScript（.tsx） | ✅ 完整支持 |
| 纯 HTML 文件 | ✅ 完整支持 |
| Next.js 项目 | ✅ 完整支持（含 Image 组件检查） |
| Tauri 桌面应用 | ✅ 完整支持（含跨平台兼容规则） |
| TDesign 组件库 | ✅ 适配（检查内置 a11y 是否被覆盖） |
| @tencent/yb-component | ✅ 适配（检查 props 透传） |
| Vue / Angular | ⚠️ 部分支持（基础 HTML 规则生效） |
| 微信小程序（WXML） | ❌ 不支持 |

---

## 十、常见问题

### Q1: 装饰性图片会误报吗？

**不会。** `alt=""` 被视为合法的装饰性图片标注，不会被标记。同时 `alt=""` + `role="presentation"` 也是合法的。

### Q2: 支持 i18n 项目吗？

**支持。** 如果项目中使用了 `useTranslation` / `t()` 函数，Skill 会自动用 `t()` 包裹新增的标签文本，例如 `aria-label={t('关闭')}`。

### Q3: 会破坏现有代码风格吗？

**不会。** 修复时会保留现有的缩进风格（空格/Tab）、引号风格（单引号/双引号），并与周围代码保持一致。

### Q4: 修复后需要手动验证吗？

Skill 在步骤 5 会自动运行 Lint 检查。但建议人工复查以下内容：
- `aria-label` 的文案是否准确描述了操作
- 弹窗的焦点管理是否符合预期
- 跨平台兼容回退是否覆盖了目标平台

### Q5: 一次能扫描多大的项目？

建议单次扫描不超过 50 个文件。大型项目可以分目录分批扫描：

```
@a11y-label-audit 扫描 src/components/
@a11y-label-audit 扫描 src/pages/
```

### Q6: 怎么只看报告不修复？

在指令中说明只需审查：

> "只做无障碍审查，输出报告，不要修复"

---

## 十一、相关资源

| 文件 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 核心技能文件，包含所有检测规则和扫描流程 |
| [reference.md](reference.md) | 规则详细说明、WCAG 对照表、边界情况处理 |
| [examples.md](examples.md) | 每条规则的修复前后代码对比（含跨平台兼容） |

外部参考：
- [WCAG 2.1 标准](https://www.w3.org/TR/WCAG21/)
- [WAI-ARIA 实践](https://www.w3.org/WAI/ARIA/apg/)
- [MDN 无障碍指南](https://developer.mozilla.org/zh-CN/docs/Web/Accessibility)
