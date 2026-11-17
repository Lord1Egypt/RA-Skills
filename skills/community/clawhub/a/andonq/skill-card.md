## Description:

AndonQ helps agents answer Tencent Cloud support questions, query tickets and requirements, and retrieve cloud resource information through the AndonQ chat service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyuxlif](https://clawhub.ai/user/cyuxlif)

### License/Terms of Use:

MIT-0

## Use Case:

Tencent Cloud users and support operators use this skill to ask product questions, inspect ticket or requirement status, and retrieve account resource information without leaving the agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth temporary codes can grant access to Tencent Cloud support or resource workflows if exposed.

Mitigation: Prefer local interactive binding, avoid pasting codes into shared chats, keep ~/.andonq/auth.json restricted to the current user, and reauthorize if a code may have been exposed.

Risk: The skill sends user questions and resource-support context to the AndonQ backend.

Mitigation: Use it only for Tencent Cloud support and resource questions that are appropriate to send to the AndonQ service.

Risk: The environment check may contact clawhub.ai for update checks despite the stated Tencent-only network scope.

Mitigation: Review outbound network policy before deployment and use the provided skip-update mode when update checks are not permitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyuxlif/skills/andonq)
- [cyuxlif Publisher Profile](https://clawhub.ai/user/cyuxlif)
- [ChatCompletionsAndonQ API Reference](references/api/ChatCompletionsAndonQ.md)
- [AndonQ Gateway](https://andon.cloud.tencent.com)
- [Tencent Cloud Authorization](https://cloud.tencent.com/open/authorize)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and service-returned answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are returned from the AndonQ SSE service; authentication and session guidance may be included when setup or reauthorization is required.]

## Skill Version(s):

2.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
