## Description:

调用自定义摘要 API，对用户提供的文本进行处理并返回结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqq-github](https://clawhub.ai/user/heqq-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to send provided text to a configured summary API for summarization, key point extraction, or normalized text processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for summarization is sent to a disclosed external API, which may expose sensitive or regulated content to that service.

Mitigation: Do not use the skill for passwords, API keys, private business documents, regulated data, or other sensitive material unless the external API and its retention practices are trusted.

## Reference(s):

- [Configured summary API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON response with concise user-facing status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends the user-provided text as the content field to an external HTTP API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
