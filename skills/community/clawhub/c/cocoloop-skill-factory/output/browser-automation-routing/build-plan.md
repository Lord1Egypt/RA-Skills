# Browser Automation Routing - 构建计划

## 目标

把浏览器自动化路线选择规则落实为可审查的正式文档产物。

## 构建目录

```text
browser-automation-routing/
├── research-summary.md
├── reference-skill-analysis.md
├── design-summary.md
├── spec.md
└── build-plan.md
```

## 构建动作

### 1. 更新正式需求

更新根级 `prd.md`，补入：

- 强需求浏览器自动化的路线比较要求
- `OpenCLI` 的优先推荐条件
- Browser Bridge 扩展安装说明要求

### 2. 更新产品需求文档

更新 `codex-prd`，把浏览器自动化路线比较写成正式需求基线。

### 3. 更新主 Skill 和阶段文档

至少更新：

- `SKILL.md`
- `ref/research.md`
- `ref/design.md`
- `sub-skills/brainstorm/SKILL.md`

### 4. 更新原子能力文档

至少更新：

- `atomic-capability/browser-access/index.md`
- 新增 `atomic-capability/browser-access/opencli-browser-bridge.md`

### 5. 生成输出产物

在 `output/browser-automation-routing/` 中生成：

- 研究摘要
- 参考 Skill 分析
- 设计摘要
- 统一 spec
- 构建计划
