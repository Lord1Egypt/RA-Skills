## Description:

Fund Advisor helps users query public mutual fund information, compare funds, build allocation plans, assess portfolio risk, monitor markets, generate reports, and send investment reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xikal](https://clawhub.ai/user/xikal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent to support mutual fund research, portfolio allocation planning, risk review, market monitoring, investment education, and report-generation workflows. Its outputs should be reviewed before any financial decision because the source documentation states that suggestions are for reference and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill stores and shares sensitive investment information with weakly scoped controls.

Mitigation: Review the skill before installation in any real financial or multi-user environment and require explicit user opt-in before saving profiles, investment diaries, alerts, or notification settings.

Risk: Artifact behavior stores user profiles, investment plans, alerts, notifications, and investment diaries under /tmp.

Mitigation: Replace plaintext /tmp storage with protected per-user storage, strong path validation, encryption, retention limits, and deletion controls.

Risk: Artifact behavior can upload generated reports to S3 and send Feishu messages containing investment information.

Mitigation: Require explicit confirmation before report upload or message delivery, and restrict report and notification contents to the minimum data needed.

Risk: The skill produces fund allocation and risk-analysis guidance that users may treat as financial advice.

Mitigation: Keep the source documentation's financial-risk disclaimer visible in user-facing workflows and require users to verify important data against official sources before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xikal/skills/fund-advisor-agent)
- [README](artifact/README.md)
- [Usage examples](artifact/examples/usage-examples.md)
- [Tool development guide](artifact/references/tool-development.md)
- [Skill integration guide](artifact/references/skill-integration.md)
- [Agent best practices](artifact/references/agent-best-practices.md)
- [Data storage design](artifact/references/data-storage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, and code snippets; generated reports may be returned as PDF, Word, or Excel links when the document-generation integration is configured.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive fund data, generated report links, saved user profile or investment-plan records, and Feishu notification confirmations when integrations are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
