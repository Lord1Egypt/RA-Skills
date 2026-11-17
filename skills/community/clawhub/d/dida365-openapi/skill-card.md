## Description:

Enables an agent to manage Dida365 tasks, projects, tags, reminders, and repeat rules through the official Dida365 OpenAPI and OAuth2 using a bundled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workingcoder](https://clawhub.ai/user/workingcoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent read and change Dida365 projects and tasks, including task creation, completion, movement, filtering, reminders, tags, and recurrence settings. It is intended for direct OpenAPI-backed task management after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint override options can send OAuth secrets, bearer tokens, and task data to non-Dida365 URLs.

Mitigation: Use only the default Dida365 endpoints unless deliberately testing with trusted infrastructure, and verify environment variables, config.json, and command flags before authentication or API calls.

Risk: OAuth client secrets, authorization codes, and cached tokens are sensitive account credentials.

Mitigation: Keep credentials out of shared logs and prompts, protect token.json, and clear cached tokens when the skill is no longer needed.

Risk: Task and project delete or move operations can alter user data.

Mitigation: Confirm destructive requests before execution and use read-back checks when the stored result matters.

## Reference(s):

- [Auth And Config](references/auth-and-config.md)
- [API Reference Notes](references/api-reference.md)
- [Examples](references/examples.md)
- [Dida365 Developer Platform](https://developer.dida365.com)
- [ClawHub Skill Page](https://clawhub.ai/workingcoder/skills/dida365-openapi)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python standard-library scripts and returns structured JSON on stdout with structured errors on stderr.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
