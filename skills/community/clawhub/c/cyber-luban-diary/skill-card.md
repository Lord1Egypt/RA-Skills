## Description:

AI diary service - push diary entries, query diaries, get AI analysis and cover images via HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengye607](https://clawhub.ai/user/fengye607)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to save diary entries, retrieve diary records, request AI-generated diary analysis, and fetch diary cover images through an HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary entries, dates, AI-analysis requests, and the Feishu-linked token are sent to image.yezishop.vip.

Mitigation: Use the skill only for diary content appropriate for that external service, and avoid submitting secrets or highly sensitive personal information.

Risk: The API token is long-lived and tied to a Feishu account.

Mitigation: Store AI_DIARY_TOKEN securely, avoid logging or sharing it, and rotate the token if it may have been exposed.

Risk: Privacy, retention, deletion, and AI-provider details are not fully disclosed in the evidence.

Mitigation: Review the service operator's privacy and credential-handling information before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengye607/skills/cyber-luban-diary)
- [Publisher profile](https://clawhub.ai/user/fengye607)
- [Feishu authorization endpoint](https://image.yezishop.vip/api/openclaw/auth-redirect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and AI_DIARY_TOKEN.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
