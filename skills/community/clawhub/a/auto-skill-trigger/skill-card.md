## Description:

Auto Skill Trigger matches skills to tasks using keyword scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pre-filter available skills and surface prompt hints based on keyword overlap between a user message and skill descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically influence an agent prompt and skill selection with weak scoping.

Mitigation: Limit when automatic matching runs and provide a user-controlled way to disable or confirm prompt hints.

Risk: Installed skill metadata may be untrusted and could affect generated prompt hints.

Mitigation: Sanitize skill names and descriptions before including them in prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/skills/auto-skill-trigger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt-hint text that prioritizes matched skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
