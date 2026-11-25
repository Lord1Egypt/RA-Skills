# 设计系统参考（示例）

> **这是一个示例。** 把这个文件复制为 `design-system.md`，并替换为你自己的设计 token。chrome-qa-agent skill 使用 `design-system.md`（而非本文件）作为视觉一致性检查的基准。
>
> ```bash
> cp references/design-system.example.md references/design-system.md
> # 然后用你品牌的取值编辑 design-system.md
> ```

---

下面是一个设计系统示例，展示期望的格式和细节程度。

## 品牌色（Brand Colors）

```
brand-primary: #F03603   (亮橙红 — 主品牌色)
brand-blue:    #4DA9E4   (活跃/运行中状态)
brand-yellow:  #F4BA41   (警告、高亮)
brand-purple:  #9C71F0   (强调色)
brand-pink:    #EC679B   (强调色)
brand-green:   #90C94D   (成功/已完成)
brand-black:   #100D0D   (文本、悬停状态)
brand-gray:    #514F4F   (边框、次要文本)
brand-white:   #F9F6F4   (暖调灰白背景)
```

### 语义化颜色用法

| State | Color | Hex |
|-------|-------|-----|
| Success/Completed | brand-green | #90C94D |
| Running/Active | brand-blue | #4DA9E4 |
| Warning/Timed Out | brand-yellow | #F4BA41 |
| Error/Failed | brand-primary | #F03603 |
| Neutral | brand-gray | #514F4F |

### UI 元素

- **主要操作**：brand-primary (#F03603)
- **主要操作悬停**：brand-black (#100D0D)
- **主色上的文字**：白色 (#FFFFFF)
- **边框**：brand-gray (#514F4F) 或 gray-200 (#edebeb)
- **背景**：白色 (#FFFFFF) 或 brand-white (#F9F6F4)

## 排版（Typography）

- **正文**：Inter 400/500/600/700（Google Fonts）
- **展示/品牌字**：PP Supply Sans（自定义，通过 woff2 加载）
- **代码**：JetBrains Mono（等宽）
- **正文字号**：14px (`text-sm`) 为标准
- **标签**：14px medium (`text-sm font-medium`)
- **徽标**：12px semibold (`text-xs font-semibold`)

## 圆角（Border Radius）

基于 `--radius: 6px` 的分级体系：

| Token | Size | Usage |
|-------|------|-------|
| `rounded-none` | 0px | 品牌强调按钮（brand variant） |
| `rounded-[2px]` | 2px | 徽标、小型指示 |
| `rounded-sm` | 4px | **最常用** — 按钮、输入框、卡片 |
| `rounded-md` | 6px | 中型容器 |
| `rounded-lg` | 8px | 提示框、大型弹窗 |
| `rounded-full` | 100% | 状态圆点、头像 |

## 间距（Spacing）

4px 基础单位。常见模式：

- `p-2` / `px-2` / `py-2` — 8px
- `p-3` / `px-3` / `py-3` — 12px（非常常用）
- `p-4` / `px-4` / `py-4` — 16px（非常常用）
- `gap-2` — 8px，`gap-3` — 12px，`gap-4` — 16px

## 组件模式（Component Patterns）

### 按钮（Buttons）

| Variant | Background | Hover | Border radius |
|---------|-----------|-------|---------------|
| `brand` | #F03603 | #100D0D | `rounded-none` |
| `default` | primary bg | darker | `rounded-sm` |
| `destructive` | red | darker red | `rounded-sm` |
| `outline` | transparent | gray-100 | `rounded-sm` |
| `ghost` | transparent | accent bg | `rounded-sm` |

**尺寸**：default=40px (h-10)，sm=36px (h-9)，lg=44px (h-11)，icon=40x40

### 输入框（Inputs）

- 高度：40px (`h-10`)
- 边框：`border border-brand-gray` (#514F4F)
- 圆角：`rounded-sm` (4px)
- 内边距：`px-3 py-2`
- 聚焦：`ring-2 ring-ring ring-offset-2`

### 徽标（Badges）

- 圆角：`rounded-[2px]` (2px)
- 内边距：`px-2.5 py-0.5`
- 字体：`text-xs font-semibold`

### 卡片（Cards）

- 圆角：`rounded-sm` (4px)
- 边框：`border border-gray-200`
- 内边距：`p-4`

### 状态圆点（Status Dots）

- 尺寸：`h-2 w-2`
- 形状：`rounded-full`
- 颜色：匹配上述语义化状态色

## 聚焦状态（Focus States）

所有交互元素：
```
focus-visible:outline-none
focus-visible:ring-2
focus-visible:ring-ring
focus-visible:ring-offset-2
```

## 禁用状态（Disabled States）

```
disabled:pointer-events-none
disabled:cursor-not-allowed
disabled:opacity-50
```

## 视觉原则（Visual Principles）

- **边框优于阴影** — 本示例偏好用边框做视觉分隔，而非 box-shadow
- **锐利的品牌边角** — 品牌专属的 CTA 使用 `rounded-none`（直角）
- **暖调中性色** — 背景使用灰白 (#F9F6F4) 而非纯白
- **基于 class 的暗色模式** — 在 `<html>` 元素上加 `.dark` class
- **4px 间距网格** — 所有间距都应为 4px 的倍数
