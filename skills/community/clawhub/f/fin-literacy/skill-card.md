## Description:

金融知识问答 supports A-share financial-literacy questions, tiered investor education, A-share analysis workflows, and risk-management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External A-share investors, finance learners, and finance-oriented teams use this skill to ask financial-knowledge questions, receive audience-tiered educational material, and structure A-share analysis or risk-management outputs. Its outputs should be treated as informational support rather than professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill offers personalized investment guidance that users may mistake for professional financial advice.

Mitigation: Present outputs as informational, require user confirmation for consequential decisions, and avoid representing outputs as brokerage, legal, tax, or investment advice.

Risk: The skill requests broad read, command-execution, and data-access capabilities for finance workflows.

Mitigation: Scope permissions to the active task, require confirmation before command execution or API-key-backed data access, and avoid sharing brokerage credentials or sensitive trading history unless explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/fin-literacy)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON examples with optional shell or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference user-provided A-share data sources or API-key-backed market data access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
