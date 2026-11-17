## Description:

Helps agents identify repetitive automation opportunities, choose workflow or RPA approaches, design process templates, and estimate ROI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laziobird](https://clawhub.ai/user/laziobird)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate repetitive browser, file, and SaaS workflows, select a suitable automation route, and draft setup steps for workflow platforms or RPA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may operate on authenticated sessions or sensitive business data.

Mitigation: Use least-privilege automation accounts, isolate runs from personal browser profiles, and avoid entering passwords or MFA codes into chat prompts.

Risk: The skill recommends saved login sessions and includes plaintext credential examples.

Mitigation: Prefer OAuth or a secrets manager and review any generated automation before using it with internal systems.

Risk: The skill points users to an unpinned third-party RPA package.

Mitigation: Inspect and pin the referenced openclaw-rpa package before granting it access to internal systems or business data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laziobird/skills/automation-workflow-helper)
- [Dify](https://dify.ai)
- [Dify GitHub Repository](https://github.com/langgenius/dify)
- [Coze](https://www.coze.com)
- [n8n](https://n8n.io)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)
- [OpenClaw RPA GitHub Repository](https://github.com/laziobird/openclaw-rpa)
- [OpenClaw RPA on ClawHub](https://clawhub.ai/laziobird/openclaw-rpa)
- [OpenClaw RPA Amazon Best Sellers Tutorial](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-amazon-bestsellers.en-US.md)
- [OpenClaw RPA Airbnb Competitor Price Tracker Tutorial](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-airbnb-compare.en-US.md)
- [OpenClaw RPA AP Reconciliation Tutorial](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with workflow templates, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend browser automation, saved login sessions, and third-party workflow or RPA tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
