# 品牌设计系统接入

## 目录结构

每个品牌系统放在独立子目录下，遵循相同的四文件结构：

```
design-system/brand/
└── <brand-name>/
    ├── tokens.css            # 语义 token 覆盖（只写与 universal 不同的部分）
    ├── component-tokens.css  # 组件 token 覆盖（只写需要定制的组件）
    ├── components.md         # 品牌组件规格补充（可选）
    └── usage-guidelines.md   # 品牌语义规则（可选）
```

## 加载优先级

1. Skill 启动时检查 `design-system/brand/` 目录
2. 有匹配的品牌子目录 → 加载品牌系统，**完全覆盖** universal 中同名 token
3. 品牌 tokens.css 中未定义的 token → 自动 fallback 到 universal
4. 无品牌系统 → 使用 universal fallback，告知用户：`Using universal defaults`

## tokens.css 接入示例

只写与 universal 不同的部分，其余自动 fallback：

```css
/**
 * Brand: Example Brand
 * 只定义与 universal 不同的 token
 */
:root {
  /* 主色替换为品牌色 */
  --color-primary:         #2F6BFF;
  --color-primary-dark:    #1F4FD1;
  --color-primary-surface: #EAF1FF;

  /* 品牌字体 */
  --font-family: "Example Sans", "PingFang SC", "Noto Sans SC", sans-serif;

  /* 品牌圆角风格（偏大） */
  --radius-md:   12px;
  --radius-lg:   16px;
}

[data-theme="dark"] {
  --color-primary: #FFD040;
}
```

## components.md 接入示例

只写需要覆盖的组件：

```markdown
# Example Brand 组件规格（覆盖 universal）

## Button
primary: bg var(--color-primary) text #ffffff  ← 主按钮使用品牌色
height: var(--btn-height-mobile)               ← 其余继承 universal

## Card
border: 1px solid var(--color-border)  ← 品牌卡片描边
shadow: var(--shadow-md)
```

## 注意事项

- 不要完整复制 universal 的内容再修改，只写差异部分，降低维护成本
- token 名称必须与 universal 中的名称完全一致（包括大小写）才能正确覆盖
- 品牌系统的 tokens.css 同样会被复制到产出目录，与 universal tokens.css 合并（品牌优先）
