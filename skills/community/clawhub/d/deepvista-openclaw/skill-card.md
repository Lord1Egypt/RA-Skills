## Description:

DeepVista auto-capture and knowledge integration for OpenClaw agents that saves notable user statements, decisions, and insights to a DeepVista knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an OpenClaw agent preserve facts, decisions, plans, meeting highlights, and relationship context in DeepVista during conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic capture can store personal, meeting, relationship, planning, and business-strategy details externally without clear user consent or review.

Mitigation: Require explicit opt-in and per-note confirmation before saving conversation content to DeepVista.

Risk: Authentication guidance in the artifact asks the user to share a login code in chat.

Mitigation: Direct users to complete DeepVista authentication outside the chat and do not request or handle authentication codes.

Risk: Shell commands that interpolate note content can mishandle sensitive or adversarial text.

Mitigation: Use documented safe CLI invocation patterns and avoid shell interpolation for user-provided note content.

## Reference(s):

- [Deepvista Openclaw on ClawHub](https://clawhub.ai/jingconan/skills/deepvista-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the DeepVista CLI to create or update external notes when configured.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
