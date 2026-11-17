## Description:

Guides agents in using AceDataCloud's LLM gateway for chat, embeddings, stateful conversations, and scheduled tasks across multiple model families.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure AceDataCloud access and build chat, embedding, multimodal, and scheduled-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation history, embeddings input, and uploaded file URLs may be sent to AceDataCloud.

Mitigation: Share only data approved for that provider and review submitted content before making requests.

Risk: An exposed API token could allow unauthorized use of the account.

Mitigation: Keep the token private, do not include it in prompts or committed files, and restrict allowed APIs where possible.

Risk: Scheduled agent runs are unattended and billable and may invoke permitted tools.

Mitigation: Confirm the task, tool permissions, schedule, and spending scope before enabling it; monitor runs and pause failures.

## Reference(s):

- [ClawHub AI Chat release](https://clawhub.ai/acedatacloud/skills/ai-chat)
- [AceDataCloud first-run guide](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud unattended-task confirmation guard](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/unattended.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover API requests, authentication, and scheduled-task setup.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
