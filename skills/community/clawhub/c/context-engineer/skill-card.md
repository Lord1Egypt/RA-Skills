## Description:

Context window optimizer - analyze, audit, and optimize an agent's context utilization before it is sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect local workspace context files, OpenClaw tool definitions, memory files, and installed skill overhead so they can reduce token use and track optimization progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local context files, installed skill definitions, and OpenClaw/tool configuration from the selected workspace, which may contain sensitive instructions or secrets.

Mitigation: Run it only on intended workspaces and avoid workspaces containing sensitive content unless that content may be analyzed locally.

Risk: Terminal reports or optional JSON snapshots may summarize sensitive local context details.

Mitigation: Review generated output and snapshots before sharing them, and store or delete snapshots according to the workspace's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkuehnl/skills/context-engineer)
- [Project homepage](https://github.com/cacheforge-ai/cacheforge-skills)
- [Anvil AI](https://anvil-ai.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text reports with optional JSON snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts are approximate and based on local file analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and CHANGELOG report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
