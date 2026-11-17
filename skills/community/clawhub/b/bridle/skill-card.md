## Description:

Unified configuration manager for AI coding assistants. Manage profiles, install skills/agents/commands, and switch configurations across Claude Code, OpenCode, Goose, and Amp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:


## Use Case:

Developers and engineers use Bridle to manage assistant profiles, install skills, agents, commands, and MCP configuration, and switch configurations across Claude Code, OpenCode, Goose, and Amp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bridle can install unpinned third-party skills, agents, commands, or MCP configuration into trusted assistant directories.

Mitigation: Install only from trusted publishers and repositories, prefer pinned versions or reviewed commits, and review components before deployment.

Risk: Forced installs or profile changes can overwrite existing assistant configurations.

Mitigation: Back up assistant configuration directories and avoid --force unless the target changes have been reviewed.

## Reference(s):

- [Bridle ClawHub Skill Page](https://clawhub.ai/bjesuiter/skills/bridle)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include text, JSON, or auto-formatted command output guidance for Bridle workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
