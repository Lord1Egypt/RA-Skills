## Description:

Project onboarding for game development. Detects project state, asks guided questions to determine user context, and routes to the correct workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toilanguyen2910](https://clawhub.ai/user/toilanguyen2910)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game creators use this skill to onboard a new or existing game project, identify project state and experience level, choose an appropriate engine path, and route into follow-on game development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as /start or onboard me may invoke the skill in unrelated chats.

Mitigation: Confirm the agent is operating in the intended game project workspace before allowing file creation or edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toilanguyen2910/skills/game-dev-start)
- [Publisher profile](https://clawhub.ai/user/toilanguyen2910)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and a project context file template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update a context.md onboarding file when the agent has workspace write access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
