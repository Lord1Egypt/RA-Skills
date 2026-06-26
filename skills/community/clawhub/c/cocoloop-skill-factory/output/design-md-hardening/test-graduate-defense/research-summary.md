# 研究摘要

## 测试目标

验证 `design_md` 接入后，是否能稳定生成一个“研究生毕业答辩 PPT skill”的最小测试产物。

## 已确认事实

- 当前生成链已经支持从 `spec.yaml` 渲染 Skill。
- 视觉任务可以通过 `design_md` 指定默认预设，并映射到最终 Skill 的 `references/design.md`。
- 本地环境没有 `python-pptx`，也没有 `pptxgenjs`。
- `factory-skill-builder` 运行所需的 `yaml` 包可用。

## 结论

- 本轮可以验证 `spec -> skill` 的 `design_md` 链路。
- 本轮不能直接在当前环境内生成可编辑 `.pptx`，需要降级为结构化 slides 文档。
