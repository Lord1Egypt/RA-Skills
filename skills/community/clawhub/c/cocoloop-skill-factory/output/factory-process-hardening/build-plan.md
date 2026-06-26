# Factory Process Hardening - 构建计划

## 目标

把两条已完成 todo 重新落实为可以被审查、被提交、被复用的正式产物。

## 构建目录

```text
factory-process-hardening/
├── research-summary.md
├── reference-skill-analysis.md
├── design-summary.md
├── spec.md
└── build-plan.md
```

## 构建动作

### 1. 更新正式需求来源

更新根级 `prd.md`，把以下内容写入正式产品需求：

- 调研阶段必须补齐的收集项
- 设计阶段对搜索结果的本地拉取和深度分析要求
- 每次正式收口都要形成的产物清单

### 2. 更新 `codex-prd`

至少更新这些文档：

- `research-and-conversation.md`
- `design-and-construction.md`
- `search-capabilities-and-dependencies.md`
- `source-requirements-map.md`
- 新增 `todo-strict-redo-design.md`

### 3. 更新主 Skill 和阶段文档

至少更新这些文件：

- `SKILL.md`
- `ref/research.md`
- `ref/design.md`
- `ref/construction.md`
- `sub-skills/brainstorm/SKILL.md`

### 4. 生成输出产物

在 `output/factory-process-hardening/` 中生成：

- 研究摘要
- 参考 Skill 本地分析
- 设计摘要
- 统一 spec
- 构建计划

### 5. git 提交策略

由于工作区根目录不是 git 仓库，提交分两段进行：

- 在 `codex-prd` 仓库提交需求与设计文档
- 在 `cocoloop-skill-factory` 仓库提交主 Skill、阶段文档和 `output/` 产物

根级 `prd.md` 与 `todo.md` 会被修改，但无法在当前目录直接提交，需要作为工作区级修改单独保留。

### 6. 独立审查

在文档和产物完成后，发起一次独立子 agent 审查，重点检查：

- 两条已完成 todo 是否都满足新的完成标准
- 构建产物是否真实存在，而不是只在流程中被提到
- 搜索相关 Skill 的本地分析是否足够具体

## 交付检查

- [x] 已写入根级 `prd.md`
- [x] 已形成正式设计文档
- [x] 已进入 `output/` 构建产物
- [x] 已完成 git 提交
- [x] 已完成独立子 agent 审查

## 审查结果回写

- 第二轮独立审查结论：没有 findings
- 当前可以继续将两条 todo 保留为“已完成”
- 审查保留的残余风险：根级目录不是 git 仓库；`cocoloop-skill-factory` 子仓库仍有与本次任务无关的删除项未清理
