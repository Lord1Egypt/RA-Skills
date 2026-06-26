# Output 目录契约

## 目标

`output/` 用来保存每一轮正式收口后的可审查产物。
这些文件不是草稿缓存，也不是临时笔记。
它们是后续设计、构建、审查和回溯的直接输入。

## 目录命名

每一轮规则补充、流程加固、任务域研究或方案收口，都使用一个独立目录：

```text
output/<topic-slug>/
```

示例：

- `output/spec-schema-hardening/`
- `output/browser-automation-routing/`
- `output/preset-system-hardening/`

## 必选产物

每个目录至少包含：

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`

## 条件产物

在以下情况中继续补充：

- 进入结构化协议收口：补 `spec.yaml`，而且它应先于后续摘要产物形成
- 涉及协议审查：补 `spec-review.md`
- 涉及 benchmark：补 `benchmark-plan.md` 或评估文档

## 文件职责

- `research-summary.md`
  记录这轮研究核实了什么、得到什么稳定结论
- `reference-skill-analysis.md`
  记录本地拉取和对比过的 Skill、CLI、API/MCP、模板或参考方案
- `design-summary.md`
  记录设计决策、路线比较和最终收敛原因
- `spec.md`
  记录当前这轮要落实的统一要求
- `build-plan.md`
  记录后续文档或实现该怎么推进
- `spec.yaml`
  保存结构化协议实例；只要该轮已经进入统一协议层，它就是后续摘要的上游输入

## 生成顺序

建议固定顺序：

1. 先形成 `spec.yaml`（如果该轮已经进入统一协议层）
2. `research-summary.md`
3. `reference-skill-analysis.md`
4. `design-summary.md`
5. `spec.md`
6. `build-plan.md`
7. 需要时再补评估文档

## 使用规则

- 不要把正式结论只留在对话里
- 不要把不同主题混进同一个目录
- 设计阶段引用的结论，应能在对应 `output/` 目录中找到来源
- 如果当前研究覆盖还不充分，必须通过 `coverage_status` 和 `open_gaps` 表达
