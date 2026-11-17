## Description:

AI内容变现助手，帮助内容创作者、知识付费从业者评估内容价值、推荐变现渠道、制定定价策略、预测收入。当用户询问"如何变现"、"内容如何赚钱"、"知识如何变现"等内容变现相关问题时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickyhu1699](https://clawhub.ai/user/nickyhu1699)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, knowledge-commerce operators, freelancers, and side-business builders use this skill to assess monetization potential, choose channels, plan pricing, forecast revenue, and generate execution checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports include specific personal contact details that are not clearly disclosed in the skill documentation.

Mitigation: Review generated reports before sharing them and remove or replace undisclosed contact details unless the publisher explicitly approves their inclusion.

Risk: The report-saving helper can receive caller-provided filenames without path validation.

Mitigation: Do not pass user-controlled filenames to save_report unless path validation or filename sanitization is added.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports and conversational guidance with optional Python-generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes generated Markdown reports to an OpenClaw workspace directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
