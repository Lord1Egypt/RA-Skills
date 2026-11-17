## Description:

g1geo guides agents in using the official @g1geo/cli for GEO content workflows, AI search visibility analysis, brand monitoring, article generation and rewriting, reporting, and multi-platform publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzoob](https://clawhub.ai/user/mzoob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content operations teams use this skill to route g1geo tasks through the installed CLI for brand visibility checks, GEO optimization, article production, trend analysis, reports, and publishing workflows. It is intended for agents that need to discover available CLI capabilities, authenticate safely, and execute complete content or monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or update a mutable global npm CLI and to treat the installed CLI guide as authoritative.

Mitigation: Review the skill before installation, require explicit approval for installs and updates, and prefer a pinned, reviewed @g1geo/cli version.

Risk: Authenticated CLI use can grant account-level access and may initiate publishing workflows.

Mitigation: Require explicit approval for authentication and publication, confirm product and publishing context before execution, and review CLI results before acting on them.

## Reference(s):

- [ClawHub g1geo skill page](https://clawhub.ai/mzoob/skills/g1geo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run authenticated CLI workflows that return text, JSON-wrapped results, reports, or publishing task status depending on the installed CLI version.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
