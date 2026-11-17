## Description:

通过扣子开放 API（api.coze.cn）一键部署并发布 AI 客服智能体，覆盖知识库创建、文档上传、智能体创建与配置、知识库绑定、API 发布、回归测试、上架文案与提审材料生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenwo1314](https://clawhub.ai/user/zhenwo1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI automation builders, and service providers use this skill to create, configure, publish, test, and prepare listing materials for Coze-based customer-service agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Coze API token to create and publish bot resources.

Mitigation: Use a minimally scoped token and run the skill only when you intend to create or publish Coze resources.

Risk: Selected knowledge-base files are uploaded to Coze during deployment.

Mitigation: Review the knowledge-base directory before running and remove secrets, unnecessary personal data, or files that should not leave the local environment.

Risk: Customer-facing appointment or lead-capture templates may involve privacy or consent obligations.

Mitigation: Add appropriate privacy and consent wording before using generated templates with customers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenwo1314/skills/bot-publish)
- [Coze API](https://api.coze.cn)
- [Coze chat API endpoint](https://api.coze.cn/v3/chat)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with command output, resource identifiers, JSON test summaries, and listing-material text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Coze bot and dataset resources, publish an API connector, and upload selected knowledge-base files when run with a Coze API token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
