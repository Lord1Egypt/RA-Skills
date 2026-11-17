## Description:

调用自定义摘要 API，对用户提供的文本进行处理并返回结果

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqq-github](https://clawhub.ai/user/heqq-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize, extract key points from, or otherwise process user-provided text through a custom HTTP API when a summarization request is explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is forwarded to a disclosed external API.

Mitigation: Use only with text that is approved for external processing and avoid secrets, personal data, confidential documents, or regulated content unless suitable controls are added.

Risk: The local service is unauthenticated and logs submitted text.

Mitigation: Restrict access to trusted clients, add authentication and rate limits, and remove raw payload logging before handling sensitive or production traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heqq-github/skills/custom-api-summary)
- [Disclosed external summary API](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [JSON response containing success status, result data, or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires non-empty text content and returns backend API results without fabricating output on failure.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
