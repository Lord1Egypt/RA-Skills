# Error Message Improver

## 功能

将含糊的应用、API、CLI 或客服错误改写成可诊断、可执行、不过度暴露内部细节的错误提示。

该技能来自 `20260623-040526` 运行中的需求信号，并已改写为面向发布的领域化说明，避免通用模板化内容。

## 适用场景

product engineers, platform teams, support leads, technical writers, and SaaS operators who need errors that reduce tickets and unblock users。

## 基本流程

1. 先确认目标、输入、约束、受众和成功标准。
2. 选择最小且可验证的处理路径，优先使用本地脚本、清单、文档或轻量工作流。
3. 产出具体可执行的结果，而不是泛泛建议。
4. 检查结果是否覆盖风险、边界条件、后续动作和可验证证据。

## 交付物

- 可直接使用的方案、文档、代码片段或检查清单。
- 针对风险、边界条件和验证方式的说明。
- 需要时提供后续改进或上线建议。

## 文件

- `SKILL.md`：英文技能说明。
- `SKILL.zh-CN.md`：中文技能说明。
- `README.md`：英文用户指南。
- `README.zh-CN.md`：中文用户指南。
- `references/requirement-plan.md`：需求证据和评分详情。
- `agents/openai.yaml`：默认调用元数据。
