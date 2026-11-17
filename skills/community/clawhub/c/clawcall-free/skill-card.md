## Description:

AI语音代理拨打美国真实电话的免费版，支持基础外呼与轮询，并提供每日有限试用额度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and automation users use this skill to have an agent place basic outbound calls to US phone numbers, poll call status, and summarize the final outcome and transcript.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can cause an agent to place real outbound phone calls based on broad activation language.

Mitigation: Require explicit user consent before each call and keep call instructions scoped to the user's stated purpose.

Risk: The skill persistently stores an API key and phone number locally.

Mitigation: Obtain consent before credential storage and document how users can delete or rotate the stored key.

Risk: Call instructions and transcripts may contain sensitive information sent to or returned from an external service.

Mitigation: Include only necessary information in the call task and review transcripts before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/clawcall-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with JSON examples and shell/API command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include call_id, lifecycle status, outcome, talk_seconds, transcript, and API key handling guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
