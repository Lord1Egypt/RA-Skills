# Factory Process Hardening - 统一 Spec

## 基本信息

- 名称：`factory-process-hardening`
- 目标：将已完成 todo 重新落实为正式需求、设计文档和构建产物
- 适用对象：`cocoloop-skill-factory` 自身的流程治理与构建准备
- 当前阶段：文档与产物加固，不进入脚本实现

## 要解决的问题

本轮重做之前，这两条已完成 todo 只进入了部分规则文档，缺少根级 `prd.md`、正式设计文档和 `output/` 样例产物。

本轮重做后，上述三项已经补齐，相关子仓库也已经完成提交，并补齐了一轮独立审查。

当前剩余的只是工作区级残余事项：

- 根级 `prd.md` 与 `todo.md` 因工作区根目录不在 git 中，无法形成根级提交记录
- `cocoloop-skill-factory` 子仓库里仍有与本次任务无关的删除项尚未清理

## 必须满足的要求

### 要求 1

调研阶段必须收集：

- 主平台和次平台
- 脚本偏好与禁用项
- 视觉输出风格偏好和相关 Skill 推荐条件
- 创作写作任务的风格约束
- 网站自动化风险提示

### 要求 2

设计阶段必须：

- 将进入正式比较的候选 Skill 全量拉取到本地
- 查看其 `SKILL.md`、目录结构、脚本、引用文件、依赖和资源
- 将可复用能力、设计要点、最佳实践和不采用原因详细写入设计文档

### 要求 3

每个正式收口的 todo 补充都要形成以下构建产物：

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`

## 输入

- 根级 `prd.md`
- `todo.md`
- `codex-prd` 中的需求文档
- 本地可读的参考 Skill 文件
- `cocoloop-skill-factory` 当前主 Skill 和阶段文档

## 输出

- 更新后的 `prd.md`
- 一份严格重做设计文档
- 一组位于 `output/factory-process-hardening/` 的产物样例
- 子仓库中的 git 提交
- 一份独立审查结果

## 成功标准

- 两条已完成 todo 的内容都已经进入 `prd.md`
- 存在一份正式设计文档承接本次重做
- `output/` 下存在可直接审查的构建产物
- 至少一个独立审查结论被记录
