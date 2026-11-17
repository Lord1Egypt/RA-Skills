## Description:

Main orchestration skill for a Python and finance app team with full-stack web capability; it routes tasks to sub-agents Simons, Carmen, and Ada.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camilla-oclm](https://clawhub.ai/user/camilla-oclm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate a Python and finance application team, route requests to role-specific sub-agents, and produce task plans, code, commands, configuration, or guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent behavior depends on missing or mutable workspace files such as AGENTS.md, MEMORY.md, and referenced orchestration files.

Mitigation: Install only in controlled workspaces where those files are trusted, reviewed, and versioned.

Risk: Sub-agent spawning or model changes could occur without enough user control.

Mitigation: Require explicit user approval before spawning sub-agents or changing models.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with code, shell command, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on trusted workspace state and referenced orchestration files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
