## Description:

OpenClaw AgentForge Compare is a remote MCP skill for comparing AI coding tools, reviewing feature and pricing profiles, generating recommendations, and calculating team costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to compare AI coding assistants, inspect tool profiles, estimate costs, and request recommendations based on team size, budget, workflow, and required features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendation inputs such as team size, budget, workflow, and required features are sent to a remote MCP service.

Mitigation: Avoid sending sensitive internal details, and use only information appropriate for the remote service.

Risk: Pricing and recommendation outputs may be incomplete or outdated for purchasing decisions.

Mitigation: Verify current prices, plan terms, and feature availability on official vendor sites before buying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yedanyagamiai-cmd/skills/agentforge-compare)
- [OpenClaw MCP servers homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses with comparison matrices, profiles, recommendations, cost breakdowns, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP service responses may depend on current tracked pricing and tool metadata; users should verify vendor pricing before purchasing.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
