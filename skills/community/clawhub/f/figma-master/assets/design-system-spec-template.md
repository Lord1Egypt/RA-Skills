# 设计系统规范模板（Design System Spec Template）

> 复制本模板，为每个设计系统/组件库产出一份可分享的规范文档。配合 [scripts/lint_design_tokens.py](../scripts/lint_design_tokens.py) 使用：文档里的 Token 命名需通过脚本校验。

## 1. 概览

- 系统名称：
- 适用产品 / 平台：
- 维护者：
- 版本：

## 2. Token 分层

| 层 | 说明 | 示例 |
|----|------|------|
| Primitive | 物理常量，无语义 | `color.blue-500` |
| Semantic | 用途/状态，引用 Primitive | `color.action.primary` |
| Component | 组件内部状态，引用 Semantic | `button.bg.default` |

## 3. 命名约定

- 每段 kebab-case / lowerCamel，禁止 `_`、空格、全大写
- 首段必须是受控分类：`color / space / size / radius / font / shadow / opacity / border / motion / zIndex / duration`
- 组件变体：`Component/prop=value`（如 `Button/size=large`）

## 4. 主题（暗色模式）

- 仅覆盖 Semantic 层绑定，不新建 Primitive
- 亮色：`color.action.primary = {color.blue-500}`
- 暗色：`color.action.primary = {color.blue-300}`

## 5. 组件清单

| 组件 | 变体维度 | 状态 | 引用 Token |
|------|----------|------|------------|
| Button | size / state | default/hover/disabled | `color.action.*` `space.*` `radius.*` |
| Input | size / state | default/focus/error | `color.text.*` `border.*` |

## 6. 自检

```bash
python3 scripts/lint_design_tokens.py tokens --file tokens.json
python3 scripts/lint_design_tokens.py variants --file variants.txt
```

## 7. 交付检查清单

- [ ] L1/L2/L3 三层分明
- [ ] 命名通过脚本校验（0 ERROR）
- [ ] 暗色主题只覆盖 Semantic
- [ ] 组件清单含变体与引用 Token
