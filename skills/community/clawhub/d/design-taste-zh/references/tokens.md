# Token 体系（三层）

```
Primitive（原始层） → 原始值，按“它是什么”命名        （--blue-600, --space-4, --radius-2）
Semantic（语义层）  → 按“用途”命名，引用原始层        （--color-accent, --color-text-muted, --space-section）
Component（组件层） → 按“组件”命名，引用语义层        （--button-bg, --card-padding）
```

规则：
- 组件只消费**语义层或组件层** token，绝不直接用原始层或字面量。
- 换主题（深色模式、品牌变体）= 替换语义层；原始层和组件层保持不变。
- 原始层集合保持小巧。如果某个值不在尺度上，先质疑设计，再考虑添加。

## 示例（CSS 变量）
```css
:root {
  /* primitive */
  --neutral-0:#fff; --neutral-50:#f7f6f3; --neutral-200:#e7e5e0; --neutral-600:#6b6a66; --neutral-900:#1c1b19;
  --brand-500:#d9480f; --brand-600:#b93d0c;
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-6:24px; --space-8:32px; --space-12:48px; --space-16:64px;
  --radius-1:4px; --radius-2:8px; --radius-full:9999px;
  --font-sans:"Söhne","Helvetica Neue",system-ui,sans-serif; --font-serif:"Newsreader",Georgia,serif;
  --text-sm:14px; --text-base:16px; --text-lg:20px; --text-xl:32px; --text-2xl:48px;
  --ease-out:cubic-bezier(.2,.8,.2,1); --dur-fast:120ms; --dur-base:220ms;

  /* semantic */
  --color-bg:var(--neutral-0); --color-surface:var(--neutral-50); --color-border:var(--neutral-200);
  --color-text:var(--neutral-900); --color-text-muted:var(--neutral-600);
  --color-accent:var(--brand-500); --color-accent-hover:var(--brand-600);
  --space-inline:var(--space-3); --space-stack:var(--space-4); --space-section:var(--space-16);
  --shadow-raised:0 1px 2px rgb(28 27 25 / .06), 0 2px 8px rgb(28 27 25 / .04);

  /* component */
  --button-bg:var(--color-accent); --button-bg-hover:var(--color-accent-hover); --button-radius:var(--radius-1);
  --button-pad:var(--space-2) var(--space-4);
  --card-bg:var(--color-surface); --card-radius:var(--radius-2); --card-pad:var(--space-6);
}
[data-theme="dark"] {
  --color-bg:#121110; --color-surface:#1c1b19; --color-border:#2c2a27;
  --color-text:#ecebe8; --color-text-muted:#a3a19c; --color-accent:#f76b2b;
}
```

中文界面可在字体栈中拉丁字体之后追加 `"PingFang SC","Noto Sans SC"`。

## Tailwind / 其他技术栈
把语义层映射到 `theme.extend`（colors、spacing、borderRadius、fontSize）或框架的主题对象中；标记中避免任意值（`text-[13px]`、`#3b82f6`）。

## 文档化
设计系统中，每一层维护一张简短表格：token、值、用途、该做/不该做。组件规格列出：结构、变体、尺寸、状态、使用的 token、无障碍说明。
