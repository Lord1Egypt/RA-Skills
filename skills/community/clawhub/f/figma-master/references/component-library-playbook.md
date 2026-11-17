# 组件库落地手册（Component Library Playbook）

> 子技能 `figma-component-library` 讲"从设计稿生成组件代码"，但没回答**生成前怎么规划组件边界、变体怎么命名、属性怎么映射、1:1 映射为什么是陷阱、生成后怎么去重与验收**。本篇把"设计稿 → 可维护组件库"的架构决策显性化，并给出实战示例。

## 1. 生成前的三问（避免盲目 1:1）

在让 AI 生成代码前，先回答：

1. **复用边界**：这个组件是"全局通用"（Button/Input）还是"业务专用"（CheckoutCard）？通用件进组件库，业务件进业务仓库。
2. **变体维度**：它的可变维度有几个？超过 3 个维度就该考虑拆组件而非堆 props。
3. **状态枚举**：每个维度的合法值是封闭集合吗？（是 → 用 union type / 枚举；否 → 用 slot/children）

## 2. 变体命名规范（与脚本对齐）

组件变体统一 `Component/prop=value` 形式，段首大写、值小写 kebab：

```
Button/size=large
Button/state=hover
Modal/variant=centered
```
脚本 `lint_design_tokens.py variants` 校验此格式。非法：`button-size-large`（缺 `/`）、`Button/Size=Large`（值大写）、`btn/s=lg`（缩写）。

## 3. 属性映射决策矩阵

| Figma 概念 | 代码映射 | 注意 |
|------------|----------|------|
| Variant property | React prop（union） | 枚举值即 Figma variant 名 |
| Boolean property | `isX` / `hasX` prop | 默认 false |
| Instance swap | `children` / `slot` | 不要硬编码子组件 |
| Auto-layout padding | `padding` Token | 用 `space.*` 而非写死 |
| Fill color | 引用 L2 语义 Token | 绝不写死 hex |
| Text style | 引用 `font.*` Token | 不用内联 font-size |

**铁律**：生成组件时**所有视觉值必须引用 Token**（见 `design-token-strategy.md`），生成的 `.css`/style 里不应出现裸 hex 或裸 `16px`。

## 4. 实战：从一个 Figma Button 变体集到代码

设计稿 `Button` 有变体 `size: small|large`、`state: default|hover|disabled`。正确产物：

```tsx
type ButtonSize = 'small' | 'large';
type ButtonState = 'default' | 'hover' | 'disabled';
interface ButtonProps {
  size?: ButtonSize;
  state?: ButtonState;
  isPrimary?: boolean;
  children: React.ReactNode;
}
// 视觉：background 取 var(--color-action-primary)，padding 取 var(--space-2/4)
```
变体清单文件 `variants.txt`（供脚本校验）：
```
Button/size=small
Button/size=large
Button/state=default
Button/state=hover
Button/state=disabled
```

## 5. 1:1 映射是陷阱（重要）

Figma 里一个 Frame ≠ 一个组件。直接 1:1 生成会产出：
- 巨型"页面组件"（把整页当一个组件，无法复用）
- 重复组件（同一按钮在不同 Frame 被生成 5 次）

**对策**：
1. 先抽"原子组件"（Button/Input/Card），再组合。
2. 用设计稿的 Component/ComponentSet 作为边界信号——Group/Frame 不应直接成组件。
3. 生成后跑去重：同名或同结构组件合并。

## 6. 生成后验收步骤

1. **去重**：列出生成组件，合并同名/同结构（如 5 个 `Button` → 1 个带变体）。
2. **Token 化扫描**：
   ```bash
   grep -rnE '#[0-9a-fA-F]{3,8}|[0-9]+px' src/components/Button/ || echo "OK: 无裸值"
   ```
3. **变体命名校验**：`python3 scripts/lint_design_tokens.py variants --file variants.txt`
4. **Story 覆盖**：每个组件有 Storybook story 或等价示例。
5. **可访问性**：交互元素含 `:focus-visible`、对比度达标。

## 7. 典型坑与规避（扩展）

| 坑 | 表现 | 规避 |
|----|------|------|
| 整页 1:1 成组件 | 不可复用、难维护 | 先抽原子组件再组合 |
| 变体维度过多 | props 爆炸 | >3 维度拆组件 |
| 写死颜色/尺寸 | 主题切换失效 | 全部引用语义 Token |
| 缩写变体名 | 团队读不懂 | 用完整 kebab 值 |
| 忽略 boolean 属性 | 状态靠传字符串 | 用 `isX` boolean prop |
| 重复生成同组件 | 维护双份 | 生成后去重合并 |
| 硬编码子组件 | 无法替换内容 | 用 `children`/`slot` |
| 跳过 focus 样式 | a11y 红线 | 每个交互件加 `:focus-visible` |
| 不写 story | 难验收/回归 | 每个组件有 story |
| 枚举用字符串裸传 | 拼写错误难发现 | 用 union type 约束 |

## 8. 组件 API 设计原则

- **组合优于配置**：能用 `children`/`slot` 表达的，绝不堆成大 props。
- **单一职责**：一个组件解决一件事，复杂界面用组合而非一个超级组件。
- **合理默认值**：最常见场景零配置即可用，进阶场景再传 prop。
- **可访问性内建**：语义标签、ARIA、键盘操作在组件内完成，调用方无需补救。

## 9. 文档与测试

- **文档**：每个组件含用途、props 表、变体示例、可访问性说明。
- **测试**：快照测试 + 交互测试（RTL/Jest），覆盖各变体与状态。
- **视觉回归**：关键组件截图对比，防止无意的样式变更溜进主干。
- **版本**：破坏性变更走 major，向下兼容走 minor，配套更新 changelog。

## 10. 实战：把 Figma 的 Card 变体集变成代码

设计稿 `Card` 变体：`variant: elevated|outlined`、`state: default|hover`、`media: none|image`。

错误做法：生成 12 个独立组件（2×2×3 笛卡尔积）→ 爆炸且难维护。
正确做法：
```tsx
type CardVariant = 'elevated' | 'outlined';
type CardState = 'default' | 'hover';
interface CardProps {
  variant?: CardVariant;
  state?: CardState;
  media?: React.ReactNode;   // Instance swap → children
  children: React.ReactNode;
}
// 视觉：box-shadow 取 var(--shadow-md)（elevated）或 border 取 var(--border-default)（outlined）
```
变体清单 `variants.txt`：
```
Card/variant=elevated
Card/variant=outlined
Card/state=default
Card/state=hover
```
跑 `lint_design_tokens.py variants --file variants.txt` → 0 ERROR；`media` 用 `children` 不硬编码。

## 11. 组件反模式（扩展）

| 反模式 | 后果 | 修正 |
|--------|------|------|
| 整页 1:1 成组件 | 不可复用 | 先抽原子 |
| 变体维度 >3 | props 爆炸 | 拆组件 |
| 写死色/尺寸 | 主题失效 | 引用 Token |
| 缩写变体名 | 难读 | 完整 kebab |
| 忽略 boolean | 状态靠串 | isX prop |
| 重复生成 | 维护双份 | 去重 |
| 硬编码子组件 | 不可换 | children/slot |
| 缺 focus | a11y 红线 | :focus-visible |
| 无 story | 难验收 | 每组件 story |
| 枚举裸串 | 易拼错 | union type |

## 12. 版本与变更管理

- **语义化版本**：破坏性改 major，向下兼容 minor，修复 patch。
- **changelog**：每次发版写"新增/变更/修复/破坏性"，链接 PR。
- **废弃策略**：旧 API 先标 `@deprecated` 给过渡期，再删；不在同版又改又删。
- **消费方升级**：提供 codemod / 迁移指南，降低升级成本。

## 13. 组件库交付检查清单

- [ ] 已区分通用件 / 业务件，通用件入组件库
- [ ] 变体命名符合 `Component/prop=value`，脚本校验 0 ERROR
- [ ] 属性映射表已建（Figma 概念 → 代码）
- [ ] 生成样式无裸 hex / 裸 px（全部 Token 化）
- [ ] 去重合并过重复组件
- [ ] 每个组件有 Storybook story 或等价示例
- [ ] Boolean 属性用 `isX`，枚举用 union type
- [ ] 交互元素含 `:focus-visible`，对比度达标
- [ ] 已跑一致性扫描，硬编码值已归 Token

## 14. 跨团队协作与治理

组件库一旦被多团队共用，就需要治理机制防止规范被各自 fork 污染：

- **单一事实源**：组件定义在库内只有一份，消费方通过版本号引用，禁止各自 fork 改一份后在内部维护，否则修复无法回流。
- **变更评审**：破坏性变更先发 RFC / 讨论帖，给消费方迁移窗口；紧急修走 hotfix 分支，不与常规发布混。
- **消费方清单**：维护"谁在用哪个组件"的清单，破坏性改时定向通知，避免无声打断。
- **废弃策略**：旧 API 先 `@deprecated` 标注 + 提供替代路径，过渡期后再删，绝不在同版本又改又删。
- **贡献入口**：外部团队提组件前先过 design token 与变体命名自检（`lint_design_tokens.py`），避免污染命名规范。
- **文档即契约**：每个组件的 props 表、变体示例、a11y 说明是消费方的契约，变更须同步更新文档与 changelog。

> 治理的核心是**可预测**：消费方只要看版本号与 changelog，就能判断是否需要改自己的代码。

## 相关子技能与层次边界

- 本手册是 **L2 决策层**（组件边界 / 变体命名 / 属性映射 / 去重验收），代码生成交给子技能：
  - [skills/figma-component-library/SKILL.md](../skills/figma-component-library/SKILL.md) — 从 Figma 设计稿生成 React/Vue 组件代码库（本手册是其"生成前规划"配套）
  - [skills/design-system-rules/SKILL.md](../skills/design-system-rules/SKILL.md) — 组件引用的 Token 命名规范由该子技能定义
- 兄弟参考：
  - [references/design-token-strategy.md](../references/design-token-strategy.md) — 本手册 §3 铁律"视觉值必须引用 Token"的命名 / 分层依据在此
  - [references/design-review-checklist.md](../references/design-review-checklist.md) — 生成后一致性扫描命令（见 §6 验收步骤）
- **层次边界**：本手册只讲组件库架构决策与验收，不替你写业务代码、不替你选具体框架；生成与规范分别交给上面子技能 / 参考。
