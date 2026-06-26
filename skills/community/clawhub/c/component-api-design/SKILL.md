---
name: component-api-design
description: Designs reusable React/Vue component APIs and file structure for clarity, flexibility, and maintainability. Use when 设计组件, 组件API, 封装组件, component design, or defining props/slots/events.
---

# 组件与 API 设计（Component & API Design）

设计易用、可扩展、易维护的组件 API 与文件结构，提升后续开发效率。

## 触发场景

- 用户说「设计这个组件」「组件怎么封装」「API 怎么定」「props 怎么设计」
- 要新建通用组件、业务组件或对现有组件做 API 升级

## 设计维度

### 1. 职责单一

- 一个组件只做一类事（展示 / 表单 / 布局 / 反馈）
- 若同时管「数据获取 + 展示 + 复杂交互」，考虑拆成容器 + 展示组件或拆子组件

### 2. Props 设计

| 原则 | 说明 |
|------|------|
| 必要才加 | 能由 children/组合表达的不要变成 prop |
| 命名一致 | 用项目约定：value/onChange、open/onOpenChange、disabled 等 |
| 类型明确 | TypeScript 定义清晰，必填/可选、联合类型写清 |
| 可控与不可控 | 若支持受控，则 value + onChange 成对；可提供 defaultValue 做非受控 |
| 避免冗余 | 能从现有 props 推导的不再单独提供（如 loading 时 disabled 可内部处理） |

### 3. 扩展方式

- **children**：默认内容区；复杂布局用 **slots/render props**（如 header、footer、itemRenderer）
- **className / style**：允许外层控制布局和主题
- **透传**：表单类组件对 **aria-*、data-*、剩余 HTML 属性** 做透传，便于无障碍与测试
- **主题/变体**：用 variant/size 等枚举优于一堆布尔 prop（如 type="primary" size="md"）

### 4. 事件与回调

- 命名：on + 动词或 on + 名词 + 动词（onChange、onSubmit、onOpenChange）
- 参数：先传「与事件强相关的数据」，再传原生 event（若需要）
- 避免在回调里强塞过多业务逻辑，保持组件「中性」

### 5. 文件与目录

- 单组件可单文件；组件带样式、类型、子组件多时可用目录：
  - `ComponentName/index.tsx`（入口）
  - `ComponentName/ComponentName.tsx`（实现）
  - `ComponentName/types.ts`
  - `ComponentName/styles.module.scss`
  - `ComponentName/SubPart.tsx`（内部子组件）
- 类型、常量、工具函数可共用的放上层或 shared

## 执行流程

### 1. 先判断用户在哪个阶段

| 用户描述 | 实际需求 | 第一步 |
|---------|---------|-------|
| 「设计这个组件」「新建一个组件」 | 从零设计 | 问：这个组件是通用组件还是业务组件？会在几个地方用？ |
| 「这个组件 API 怎么改」「props 太多了」 | 改现有组件 | 先读现有代码，找出问题所在，再给改法 |
| 「props 怎么设计」「要不要用 children」 | 具体设计决策 | 直接给出该场景的推荐和理由 |
| 「要不要拆组件」 | 拆分决策 | 问：是因为文件太长，还是因为逻辑复用需要？两个原因的拆法不同 |

### 2. 从零设计时，先问清楚再动手

设计前必须知道：
- **使用场景**：在哪里用？用几次？（一次性业务组件 vs 多处复用的通用组件，设计原则完全不同）
- **调用方是谁**：同一个人写还是团队共用？（团队共用的要更严格的类型和文档）
- **技术栈约束**：项目用 Radix/shadcn 还是自己写？用 Tailwind 还是 CSS Modules？

**通用组件和业务组件的设计原则不同：**

| | 通用组件 | 业务组件 |
|--|---------|---------|
| props | 尽量少，保持中性 | 可以有业务语义 |
| 样式 | 支持 `className` 覆盖 | 可以写死 |
| 数据获取 | 不做，由外部传入 | 可以自己请求 |
| 复杂度 | 宁可简单，不要过度设计 | 按业务需要 |

### 3. Props 设计的决策规则

遇到这些情况，给出明确建议：

**「要不要加这个 prop」**
- 能用 `children` 或组合表达的 → 不加 prop（如 `<Button icon={<Icon />}>` 优于 `<Button iconName="star">`）
- 只有一个地方用到的特殊行为 → 不加 prop，在调用处处理
- 3 处以上地方需要这个行为 → 加 prop

**「布尔 prop 还是枚举」**
- 两种状态 → 布尔（`disabled`、`loading`）
- 三种及以上 → 枚举（`variant="primary|secondary|ghost"` 优于 `isPrimary isSecondary isGhost`）

**「受控还是非受控」**
- 需要外部控制状态（如表单联动）→ 受控：`value` + `onChange`
- 独立使用、不需要外部感知 → 非受控：`defaultValue`
- 两种都支持 → 同时提供 `value`/`onChange` 和 `defaultValue`，内部用 `useControllableState`

**「要不要透传 HTML 属性」**
- 表单类（input、button、select）→ 必须透传，用 `...rest` 传给原生元素
- 展示类容器 → 至少透传 `className` 和 `style`
- 原因：不透传会导致调用方无法加 `aria-*`、`data-*`、事件监听

### 4. 给出设计方案时，必须包含反例

只给正确做法不够，要说明**什么是错的**：

```tsx
// ❌ 错：用字符串传图标名，组件内部耦合图标库
<Button iconName="star" />

// ✅ 对：用 children 或 render prop，调用方决定用什么图标
<Button icon={<StarIcon />} />
```

```tsx
// ❌ 错：一堆布尔 prop，互斥关系不清晰
<Button isPrimary isLarge isRounded />

// ✅ 对：枚举表达变体，组合表达修饰
<Button variant="primary" size="lg" rounded />
```

### 5. 文件结构的判断

- 单文件（< 150 行，无子组件）→ 一个 `.tsx` 文件
- 有样式文件或子组件 → 目录结构：
  ```
  Button/
  ├── index.tsx        # 导出入口
  ├── Button.tsx       # 实现
  ├── types.ts         # Props 类型
  └── Button.module.css
  ```
- 不要过早拆目录，等真的需要时再拆

## 输出模板

```markdown
## 组件设计：{组件名}

### 职责
- 一句话描述组件用途与使用场景

### API（Props）
| 属性 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| … | … | … | … | … |

### 事件/回调
| 事件 | 参数 | 说明 |
|------|------|------|
| … | … | … |

### 插槽/扩展
- default：…
- 其他具名插槽：…

### 使用示例
\`\`\`tsx
<ComponentName ... />
\`\`\`

### 文件结构
- 路径与主要文件说明
```

## 与项目一致

- 若项目用 Radix/shadcn：对齐其「组合 + 可控」风格与命名
- 若项目用 Tailwind：组件根节点支持 `className`，内部用 `cn()` 合并
- 表单组件与现有表单库（如 react-hook-form）的 value/onChange 约定保持一致
