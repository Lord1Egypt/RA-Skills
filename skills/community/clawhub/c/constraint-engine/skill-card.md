## Description:

Learn from consequences, not instructions -- generate and enforce constraints from experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate, check, override, and manage workspace constraints derived from repeated failure observations. It supports local guardrails, circuit breaker status, and constraint lifecycle workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically check or block agent actions and create local constraints that affect future workflow behavior.

Mitigation: Review generated constraints before activating them, use overrides deliberately, and confirm the thresholds match the workspace's risk tolerance.

Risk: The skill writes local constraint files and audit logs under output/constraints/ and output/hooks/.

Mitigation: Keep those workspace paths under normal access controls and review generated files before sharing the workspace.

Risk: Constraint generation depends on observation data from the failure-memory skill.

Mitigation: Install the declared dependency when generation is needed and pin dependencies where stronger supply-chain controls are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leegitw/skills/constraint-engine)
- [Publisher Profile](https://clawhub.ai/user/leegitw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-like text with command examples, status output, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local constraint files under output/constraints/ and audit logs under output/hooks/ when used by an agent.]

## Skill Version(s):

1.3.1 (source: server release evidence; artifact frontmatter lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
