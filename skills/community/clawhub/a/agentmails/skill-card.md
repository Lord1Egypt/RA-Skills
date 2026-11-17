## Description:

Pub Agentmail helps agents use SkillBoss APIs to create and manage email inboxes and call 50+ models for chat, media generation, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpollitt](https://clawhub.ai/user/martinpollitt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route agent tasks through SkillBoss APIs for multimodal model calls, email sending, SMS verification, search, document parsing, and related automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External data transfer to SkillBoss and downstream providers may include prompts, files, generated content, email, or SMS payloads.

Mitigation: Install only where external API use is approved, avoid regulated or secret data unless explicitly authorized, and review requests before sending.

Risk: Email and SMS capabilities can send content to external recipients.

Mitigation: Restrict use to approved recipients and workflows, and require operator review for outbound messages.

Risk: Helper commands such as run.mjs are not validated by the security evidence.

Mitigation: Prefer the documented curl examples, or inspect and pin any helper before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/martinpollitt/skills/agentmails)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Chat model documentation](artifact/chat-models.md)
- [Tool model documentation](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; examples may send prompts, files, generated content, email, or SMS payloads to external services.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
