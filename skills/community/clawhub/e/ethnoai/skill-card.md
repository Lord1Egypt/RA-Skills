## Description:

An embedded UX research skill that studies OpenClaw interactions through passive ethnographic observation, structured micro-surveys, task-cost tracking, and retrospective daily reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:


## Use Case:

Developers, product teams, and UX researchers use this skill to observe OpenClaw sessions, collect post-task and end-of-day feedback, track usage cost, and generate local UX research reports. It is intended for users who want qualitative and quantitative insight into agent workflows while retaining review control over generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to build detailed local records of conversations, task context, survey responses, costs, and case studies that may include sensitive work context.

Mitigation: Use only where this collection is appropriate, narrow collection scope where possible, and add clear retention, export review, and deletion practices before use with proprietary, regulated, secret, or private personal data.

Risk: The authoritative security summary says the implemented redaction does not match the skill's privacy claims.

Mitigation: Review logs and generated reports before any sharing, avoid entering secrets or regulated data during observed sessions, and strengthen redaction before relying on it for privacy protection.

Risk: Generated reports and super-summary bundles can expose session context if shared without careful review.

Mitigation: Require explicit user confirmation for sharing, review and edit generated files first, and delete unneeded local data when the study is complete.

## Reference(s):

- [Analysis Framework for Daily Distillation](artifact/references/analysis-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/giulianomorse/skills/ethnoai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSONL observation and survey records, local configuration JSON, zipped case-study bundles, and conversational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local UX research data under ~/.uxr-observer/ and relies on user review before sharing generated reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
