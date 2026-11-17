## Description:

Routes task-oriented requests through AgentOctopus when the best tool is not obvious or when the request may match one of many installed skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leiw5173](https://clawhub.ai/user/leiw5173)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route tool-backed requests to AgentOctopus when the best downstream skill is not obvious. It is intended for lookups, transformations, research, weather, translation, geolocation, search, finance, and similar task-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated prompts may be routed through downstream community skills that change over time.

Mitigation: Use only downstream skills and AgentOctopus sources you trust, and avoid sending secrets or confidential data in routed queries.

Risk: Global latest-package installation can change the installed code between reviews.

Mitigation: Prefer pinned or otherwise verified installation before using the skill in sensitive environments.

Risk: Automatic downstream skill execution can invoke an unexpected tool for a user request.

Mitigation: Require confirmation or maintain an allowlist for downstream skill execution where possible.

## Reference(s):

- [Agentoctopus Openclaw on ClawHub](https://clawhub.ai/leiw5173/skills/agentoctopus-openclaw)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup commands for missing API keys, rate limits, or AgentOctopus installation.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
