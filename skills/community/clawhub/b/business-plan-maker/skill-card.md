## Description:

输入产品/业务描述，自动生成完整的商业计划书（执行摘要、市场分析、竞争定位、收入模型、运营计划、财务预测、风险评估）

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyjaixiao](https://clawhub.ai/user/hyjaixiao)

### License/Terms of Use:

MIT-0

## Use Case:

Entrepreneurs, freelancers, and business builders use this skill to turn a product or business description into a structured business plan draft. It can generate Markdown sections for executive summary, market analysis, competitive positioning, revenue model, operations, financial projections, and risk assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full mode sends the user's business description to OpenAI.

Mitigation: Avoid entering confidential strategy, customer data, trade secrets, or other sensitive information when using full mode; use quick mode for local-only template generation.

Risk: Generated market sizing, financial projections, and business recommendations may be inaccurate or unsupported.

Mitigation: Review and replace generated assumptions with verified business data before using the plan for funding, operations, or customer-facing decisions.

Risk: The skill depends on the external openai Python package.

Mitigation: Install dependencies in a virtual environment and consider pinning the openai package version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyjaixiao/skills/business-plan-maker)
- [ClawHub publisher profile](https://clawhub.ai/user/hyjaixiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown business plan printed to stdout or written to a user-selected file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full mode sends the business description to OpenAI; quick mode produces a local template framework without API use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
