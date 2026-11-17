## Description:

Checks an AgentScope project's dependency, environment file, and Python files for common configuration issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check an AgentScope project before running agents and identify missing dependencies, environment settings, or AgentScope usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads project files, including .env, in the selected directory.

Mitigation: Point it only at the intended project; avoid unrelated directories containing sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/trend0522/skills/agentscope-config-validator)
- [AgentScope project homepage](https://github.com/agentscope-ai/agentscope)

## Skill Output:

**Output Type(s):** [Markdown, Configuration guidance]

**Output Format:** [Short Markdown report with pass, warning, and failure findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks local project files; no network access is reported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
