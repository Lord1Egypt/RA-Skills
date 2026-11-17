## Description:

DevLoop Agent Pack defines a six-agent workflow for product discovery, architecture design, parallel development, testing, research, and marketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weitanai](https://clawhub.ai/user/weitanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate product-driven development loops across specialized agents for product planning, architecture, coding, testing, research, and marketing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may read persistent project memory and shared documents, write workflow files, run shell commands, commit, push branches, and in some roles operate on main.

Mitigation: Install only in repositories where that authority is acceptable, require branch protections and code review, and require explicit approval for pushes and merges.

Risk: Persistent instruction files such as MEMORY, SOUL, and BOOTSTRAP can influence future sessions.

Mitigation: Review generated or modified persistent-instruction files before starting sessions and before accepting workflow changes.

Risk: Web-search roles can expose confidential topics through external queries.

Mitigation: Avoid confidential research topics or sanitize queries before allowing web-search agents to run.

## Reference(s):

- [DevLoop Agent Pack on ClawHub](https://clawhub.ai/weitanai/skills/devloop-agent-pack)
- [README](README.md)
- [Collaboration Protocol](skills/devloop-workflow/references/collaboration-protocol.md)
- [Agent Design Background](skills/devloop-workflow/references/agent-design-background.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, workflow templates, and agent instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update project memory, PRDs, design documents, test specifications, bug trackers, review notes, reports, branch instructions, and marketing copy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
