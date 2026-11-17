# Design Token 策略手册（Design Token Strategy）

> 子技能 `design-system-rules` 告诉你"要建立 Token 体系、语义 Token"，但没回答**怎么分层、怎么命名、什么时候该加语义层、暗色主题怎么不失控、从一堆散色怎么迁移**。本篇把 Token 架构从"列几个颜色变量"升级为可扩展的三层模型，给出命名分类法、迁移 playbook、工具对比与实战示例。

## 1. 三层 Token 模型（核心决策）

| 层 | 名称 | 绑定对象 | 例子 | 改它影响谁 |
|----|------|----------|------|------------|
| L1 | Primitive（原始） | 物理量，不含语义 | `color.blue-500 = #3b82f6` | 仅自身 |
| L2 | Semantic（语义） | 角色/用途 | `color.action.primary = {color.blue-500}` | 所有引用它的组件 |
| L3 | Component（组件） | 具体组件状态 | `button.bg.default = {color.action.primary}` | 仅该组件 |

**决策树**：
```
要定义一个值 →
 ├─ 它是"纯粹的物理常量"？ → L1 Primitive（与任何用途解耦）
 ├─ 它代表"某种用途/状态"？ → L2 Semantic（引用 L1）
 └─ 它只服务于某个组件的内部状态？ → L3 Component（引用 L2）
```

**铁律**：组件**永远引用 L2，不直接引用 L1**。否则暗色主题切换时你要改 200 个组件而非 1 个语义 Token。

## 2. 命名分类法（与 [scripts/lint_design_tokens.py](../scripts/lint_design_tokens.py) 对齐）

每一段用 kebab-case / lowerCamel，**禁止下划线、空格、全大写**，首段必须是受控分类：

受控分类（`token_rules.json` 的 `allowed_categories`）：
`color` `space` `size` `radius` `font` `shadow` `opacity` `border` `motion` `zIndex` `duration`

合法示例：
```
color.blue-500
color.action.primary
space.4
radius.md
font.heading-1.size
```
非法示例（脚本会报）：
```
Color.Blue          # 全大写段
color.primary_color # 下划线
2color              # 段首数字（且不在受控分类）
foo.bar             # 首段不在受控分类
```

## 3. 实战：一个完整的 Token 树

```json
{
  "color": {
    "blue-500": { "$value": "#3b82f6", "$type": "color" },
    "blue-300": { "$value": "#93c5fd", "$type": "color" },
    "action": {
      "primary":         { "$value": "{color.blue-500}", "$type": "color" },
      "primary-hover":   { "$value": "{color.blue-300}", "$type": "color" }
    },
    "text": {
      "default": { "$value": "#111827", "$type": "color" },
      "muted":   { "$value": "#6b7280", "$type": "color" }
    }
  },
  "space": {
    "1": { "$value": "4px",  "$type": "dimension" },
    "2": { "$value": "8px",  "$type": "dimension" },
    "4": { "$value": "16px", "$type": "dimension" },
    "8": { "$value": "32px", "$type": "dimension" }
  },
  "radius": {
    "sm": { "$value": "4px",  "$type": "dimension" },
    "md": { "$value": "8px",  "$type": "dimension" },
    "lg": { "$value": "16px", "$type": "dimension" }
  },
  "font": {
    "heading-1": {
      "size":   { "$value": "32px", "$type": "dimension" },
      "weight": { "$value": "700",  "$type": "fontWeight" },
      "line":   { "$value": "1.2",  "$type": "number" }
    }
  }
}
```
注意：所有 `$value` 的别名引用用 `{color.blue-500}` 形式（W3C DTCG），`$type` 让工具能推导类型并做校验。

## 4. 从散色迁移到三层（Migration Playbook）

已有项目里散落 `#3b82f6`、`blue`、`primary` 时，按步迁移：

1. **抽取 Primitive**：扫描代码/设计稿里所有硬编码值，去重后归入 L1，按色阶/尺度命名（`blue-500` 而非 `blue`）。
2. **归纳 Semantic**：问"这个值在界面里扮演什么角色"，命名为 `action/feedback/text/bg/surface` 等用途词，全部引用 L1。
3. **改写组件**：把组件里的 `#3b82f6` 替换为 `{color.action.primary}`（或对应平台变量）。
4. **补 `$type`**：给每个 Token 标类型，便于工具校验与多平台编译。
5. **跑脚本**：`python3 scripts/lint_design_tokens.py tokens --file tokens.json` 卡命名与分类。
6. **主题覆盖**：暗色只改 L2 绑定，验证全站变色。

> 常见错误：把 `color.blue` 当语义用（用途词缺失），导致暗色要新建 `color.dark.blue` —— 用途与主题耦合，后续爆炸。

## 5. 主题化（暗色模式）的正确姿势

不要复制整套 Token。只覆盖 L2 Semantic 的"目标值映射"：

```
亮色: color.action.primary = {color.blue-500}
暗色: color.action.primary = {color.blue-300}
```
L1 不变，组件不变，只换语义层绑定。用 `[data-theme="dark"]` 或平台主题通道注入。

**反模式**：为暗色新建 `color.dark.primary` —— 把"用途"和"主题"耦合，组件要写两套引用。

## 6. 工具链命令（参考，非强制）

```bash
# Style Dictionary：把 Token JSON 编译成多平台产出
npx style-dictionary build --config style-dictionary.config.json
# 典型 platforms 输出：css-variables / scss / ios / android / json

# 自检命名与分类
python3 scripts/lint_design_tokens.py tokens --file tokens.json

# 校验变体命名
python3 scripts/lint_design_tokens.py variants --file variants.txt
```

| 工具 | 角色 | 适合 |
|------|------|------|
| Style Dictionary | Token → 多平台代码 | 工程化输出 CSS/SCSS/iOS/Android |
| Tokens Studio | Figma ↔ Token 同步 | 设计稿直接导出 Token |
| W3C DTCG | 格式标准 | 跨工具互通的基准格式 |

## 7. 典型坑与规避（扩展）

| 坑 | 表现 | 规避 |
|----|------|------|
| 组件直连 L1 | 换主题要改几百处 | 组件只引用 L2 Semantic |
| 命名带空格/`_` | 编译到 CSS 变量失败 | 统一 kebab，跑 lint 脚本 |
| 语义 Token 命名按"颜色" | `color.blue` 当语义用，主题切换崩 | 语义层用 `action/feedback/text/bg` |
| 把尺寸写死像素在组件 | 响应式断裂 | 尺寸走 `space.*` / `size.*` |
| Token 无 `$type` | 工具无法推导类型 | 每个 Token 标 `$type` |
| 一股脑平铺 | 找不到、易重复 | 强制三层嵌套，按分类归集 |
| 别名循环引用 | `A={B}` 且 `B={A}` 编译死循环 | lint 阶段检测环（手动核对） |
| 数字段冲突 | `space.4` 与 `space.04` 混用 | 统一用整数档 `1/2/4/8` |
| 暗色新建 L1 | 主题与用途耦合 | 暗色只覆盖 L2 绑定 |
| 跳过 `$type` 校验 | 类型错误到运行时才爆 | 提交前跑脚本 |

## 8. Token 治理与版本化

- **单一来源**：Token 只在一处（一个仓库/一个文件）维护，组件库通过构建产物消费，不在各自代码里重定义。
- **变更走 PR**：Token 改名/删值必须评审；破坏性改动用 alias 过渡期（旧名指向新值，一学期后删）。
- **文档即产物**：从 Token 文件自动生成可视化文档（Style Dictionary / 自定义脚本），人读的是产物不是源。
- **双端共审**：设计方与工程方共同 review，避免任一方单方面漂移导致"设计稿对、代码偏"。

## 9. 跨平台输出示例

同一份 Token 源，多平台产物由工具生成，避免手改漂移：

```css
/* CSS 变量（亮色） */
:root { --color-action-primary: #3b82f6; --space-4: 16px; --radius-md: 8px; }
[data-theme="dark"] { --color-action-primary: #93c5fd; }
```
```swift
// iOS（UIColor 生成）
let actionPrimary = UIColor(red: 0.231, green: 0.510, blue: 0.965, alpha: 1)
```
```xml
<!-- Android（resources/values） -->
<color name="action_primary">#3B82F6</color>
<dimen name="space_4">16dp</dimen>
```

## 10. Token 体系检查清单

- [ ] L1 Primitive 只含物理量，无语义
- [ ] L2 Semantic 用"用途词"，全部引用 L1
- [ ] 组件只引用 L2，无 L1 直连
- [ ] 命名每段 kebab/lowerCamel，无 `_`/空格/全大写
- [ ] 首段 ∈ 受控分类
- [ ] 每个 Token 标 `$type`
- [ ] 别名引用用 `{...}` 且无循环
- [ ] 暗色主题只覆盖 L2 绑定，不新建 L1
- [ ] 已跑 `python3 scripts/lint_design_tokens.py tokens` 且 0 ERROR
- [ ] 数字档位统一（如 1/2/4/8），无 `04` 与 `4` 混用

## 相关子技能与层次边界

- 本手册是 **L2 决策层**（Token 怎么分层 / 命名 / 迁移 / 主题化），把规范落成文档交给子技能：
  - [skills/design-system-rules/SKILL.md](../skills/design-system-rules/SKILL.md) — 将三层 Token 模型落成设计系统规范与 Token 文档
  - [skills/figma-component-library/SKILL.md](../skills/figma-component-library/SKILL.md) — 组件代码生成时所有视觉值必须引用本手册的 L2 语义 Token（见 §3 铁律）
- 兄弟参考：
  - [references/component-library-playbook.md](../references/component-library-playbook.md) — 组件边界与变体命名（与本手册"Token 化铁律"配合）
  - [references/design-review-checklist.md](../references/design-review-checklist.md) — 一致性扫描命令可机械核查本手册要消灭的硬编码色值
- **层次边界**：本手册只讲 Token 架构决策，不替你写组件代码、不替你拍板具体色值；组件落地与评审分别交给上面子技能 / 参考。
