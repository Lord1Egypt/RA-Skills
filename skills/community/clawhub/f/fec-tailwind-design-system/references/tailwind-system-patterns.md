# Tailwind 系统模式

## Token 映射

优先使用语义化名称：

| 需求 | 推荐 | 避免 |
| ---- | ---- | ---- |
| 品牌色 | `brand.600`, `--color-brand-primary` | 到处复制 `blue-600` |
| 表面层级 | `surface.canvas`, `surface.panel` | 一次性灰色值 |
| 圆角 | `radius.control`, `radius.panel` | 随意重复的具体值 |
| 阴影 | `shadow.floating`, `shadow.focus` | 没有状态含义的装饰阴影 |

如果项目已有 CSS 变量，把 Tailwind token 映射到这些变量，而不是重复维护字面量。

## Variant 归属

长 class 组合应收敛到以下位置之一：

- 带 `variant`、`size`、`tone`、`density`、`state` props 的共享组件。
- 复合组件的 slot 映射表。
- CVA、tailwind-variants 或本地 `classNames` 映射等类型化 helper。
- 只在一个模块内复用时，使用局部常量。

不要根据不受控的用户输入拼接 class 名。使用显式映射：

```ts
const toneClass = {
  neutral: "bg-slate-100 text-slate-900",
  danger: "bg-red-600 text-white",
  success: "bg-emerald-600 text-white",
} as const;
```

## 暗色模式

- 优先选择单一的项目级策略：`class`、`data-theme` 或 CSS 变量。
- 如果应用支持手动切换主题，在 body 绘制前初始化已选主题。
- 在亮色和暗色主题下都测试 disabled、focus、selected、invalid、chart 和 skeleton 状态。
- 不要把降低透明度作为 disabled 的唯一提示；要保留对比度和可感知性。

## 响应式工具类

- 默认 class 列表从移动端布局开始。
- 只有信息架构变化时，才增加更大断点前缀。
- 重复出现的响应式区块应沉淀为布局组件或 CSS 容器查询，不要反复复制同一串断点。
- 控件、标签页、看板和数据单元格使用稳定尺寸，避免 hover 和 loading 状态造成布局跳动。

## 评审清单

- Token 值有语义角色，并且没有分叉既有设计规则。
- 组件 variants 覆盖 loading、disabled、selected、invalid、focus-visible 和暗色模式。
- 动态 class 可被静态扫描识别，或已安全加入 safelist。
- Tailwind 工具类没有破坏可访问性、点击目标或 reduced-motion 要求。
- 最终 UI 已在移动端、平板和桌面宽度检查过。
