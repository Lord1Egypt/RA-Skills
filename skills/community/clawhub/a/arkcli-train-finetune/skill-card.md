## Description:

使用 ArkCLI 创建、查询和管理模型精调训练任务，并从训练指标选择最佳 step、导出训练产物为 custom model、衔接模型仓库与推理部署。任何包含精调任务 ID（`mcj-*`）的查询、查不到原因诊断、日志、trajectory、状态或生命周期操作都应使用本 skill；也适用于选择训练方法、查询精调价格和超参数、校验精调训练/验证数据、匹配精调资源组、创建任务及导出部署。本 skill 不负责独立 Dataset 生命周期管理；精调工作流中的数据校验和 Dataset 引用仍由本 skill 编排。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和机器学习工程师使用此 skill 查询模型精调能力、价格和资源，校验数据并创建或监控训练任务，再分析指标并导出训练产物以衔接部署。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that the SDK download source is unpinned, so its integrity cannot be established from the release evidence.

Mitigation: Avoid installing the SDK until its source is pinned and its integrity can be verified.

Risk: The security assessment reports conflicting authentication guidance.

Mitigation: Resolve the conflicting authentication example against authoritative documentation before using the SDK workflow.

Risk: Activity reporting and remote data submission are not clearly disclosed in the skill, according to the security assessment.

Mitigation: Clarify what activity and data are sent remotely before execution, and ensure that disclosure is clear to the user.

Risk: The security assessment flags a pipeline testing command as potentially outside the stated finetuning purpose.

Mitigation: Review whether the pipeline test is needed for the requested task and explain its purpose before running it.

## Reference(s):

- [Create and validate finetuning jobs](references/create.md)
- [List finetuning jobs](references/list.md)
- [Manage jobs, logs, and trajectories](references/manage.md)
- [Select, export, and deploy finetuning artifacts](references/export-deploy.md)
- [Job configuration](references/job-configuration.md)
- [Testing, debugging, and monitoring](references/testing-debug-monitoring.md)
- [Ark Finetune SDK fallback](references/ark-finetune-sdk.md)
- [RL plugins](references/rl-plugins.md)
- [Volcengine finetuning dataset format](https://www.volcengine.com/docs/82379/1099461?lang=zh)
- [Volcengine ArkCLI documentation](https://www.volcengine.com/docs/82379/1099350)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command and JSON/YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize validation results, job status, metrics, pricing, and training artifacts returned by ArkCLI.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
