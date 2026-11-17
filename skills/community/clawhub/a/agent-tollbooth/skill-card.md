## Description:

Web access privileges for your agent so your agent stops hitting walls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check observed operating profiles for external services before making web or API calls, including rate-limit patterns, caching guidance, authentication requirements, and known failure modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use authenticated third-party APIs when the user's task requires them.

Mitigation: Confirm API credentials, write permissions, and paid API use before allowing the agent to perform authenticated or billable actions.

Risk: Generated or promoted service profiles may be drafts based on local observations.

Mitigation: Review generated profiles before relying on them for writes, paid APIs, or repeated automated calls.

Risk: The skill keeps local logs and cache files in the OpenClaw workspace.

Mitigation: Review the workspace log and cache location and clear retained data when it is no longer needed.

## Reference(s):

- [Service Profiles - Observed Operating Behavior](references/profiles.md)
- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/agent-tollbooth)
- [Project homepage](https://github.com/highnoonoffice/agent-tollbooth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local OpenClaw log and cache paths under $OPENCLAW_WORKSPACE/data/agent-tollbooth/.]

## Skill Version(s):

2.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
