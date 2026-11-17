## Description:

Reads an AgentScope project's pyproject.toml and reports declared dependencies for manual upgrade review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers reviewing an AgentScope project's declared dependencies can use this read-only report to plan manual updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency declarations alone may not establish whether an upgrade is available or compatible.

Mitigation: Check installed and available versions against your package index and review compatibility before changing dependencies.

Risk: The report reads the selected project's pyproject.toml.

Mitigation: Run it only on a project path whose dependency declarations you are comfortable sharing with the agent.

## Reference(s):

- [AgentScope project](https://github.com/agentscope-ai/agentscope)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists detected dependency declarations and prompts manual review; does not install upgrades or check available versions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
