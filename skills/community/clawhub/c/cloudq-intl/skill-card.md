## Description:

Helps users manage international Tencent Cloud and other cloud environments through architecture visualization, Smart Advisor assessments, and AI-assisted cloud operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1ncludesteven](https://clawhub.ai/user/1ncludesteven)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to ask multi-cloud operations questions, inspect resources and costs, assess architecture and security, and obtain Tencent Cloud Smart Advisor guidance for international accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-management prompts are sent to Tencent CloudQ.

Mitigation: Share only information appropriate for the cloud service and review sensitive details before submitting prompts.

Risk: Cloud-account operations use Tencent Cloud AK/SK credentials.

Mitigation: Set credentials through environment variables for a limited sub-account and review its access before use.

Risk: Enabling Smart Advisor changes account authorization.

Mitigation: Review the change and give explicit consent before enabling Smart Advisor.

Risk: Cloud cleanup can delete the advisor CAM role.

Mitigation: Avoid running cleanup.py with --cloud unless you intend to remove that role.

## Reference(s):

- [CloudQ International release](https://clawhub.ai/1ncludesteven/skills/cloudq-intl)
- [Tencent Cloud API credentials console](https://console.tencentcloud.com/cam/capi)
- [Tencent CloudQ console](https://console.tencentcloud.com/advisor/cloudq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with links and cloud operations guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include architecture information, assessments, and console links.]

## Skill Version(s):

1.9.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
