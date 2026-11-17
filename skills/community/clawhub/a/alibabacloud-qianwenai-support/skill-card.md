## Description:

Manage QianWen support tickets from conversation, including creating, listing, viewing, replying to, closing, rating, and escalating issues for QianWen AI, Bailian, DashScope, and Alibaba Cloud model services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

QianWen platform users and developers use this skill to troubleshoot common service issues and manage support tickets for QianWen AI, Bailian, DashScope, and Alibaba Cloud model services. It helps prepare ticket content and report ticket status and support replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting may change local configuration, and update checks may invoke a neighboring skill whose exact script is not identified.

Mitigation: Require user approval for configuration repairs and verify the exact sibling script before allowing an update check.

Risk: Ticket drafts may contain sensitive details, and closing a ticket can affect its status.

Mitigation: Review ticket drafts for language and sensitive details, and confirm the ticket and its current status before closure.

Risk: The artifact manifest version does not match the skill metadata version.

Mitigation: Have the publisher correct the manifest version mismatch.

## Reference(s):

- [QianWen Support Portal](https://platform.qianwenai.com/home/support)
- [ClawHub Skill Release](https://clawhub.ai/sdk-team/skills/alibabacloud-qianwenai-support)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Human-readable Markdown summaries, ticket links, and actionable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese ticket requests; state-changing ticket actions require user confirmation.]

## Skill Version(s):

0.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
