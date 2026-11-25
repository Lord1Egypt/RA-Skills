## Description:

Bootstraps an agent workspace with identity and execution files, persistent timechain memory, quality gates, and service integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

BSL 1.1 (framework and AgentPathfinder); MIT (Timechain)

## Use Case:

Developers use this skill to initialize an agent workspace with identity, operating guidance, persistent memory, and quality checks, with optional service integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because scanners report extensive undeclared capabilities, broad access and execution paths, persistent behavior changes, and security weaknesses.

Mitigation: Before installation, review whether the dashboard, crypto-linked features, external services, and persistent memory behavior are needed; check their permissions and configuration, and avoid exposing sensitive files or credentials until those paths have been independently reviewed.

Risk: The scan covered 91 of 94 components; three were partially inspected and some analyzers were degraded, so unreported behavior remains unassessed.

Mitigation: Treat the scan as incomplete and review the affected behavior and permissions before enabling the skill in a sensitive workspace.

## Reference(s):

- [Agent Framework on ClawHub](https://clawhub.ai/certainlogicai/skills/certainlogic-agent-framework)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Python code, Shell commands, Guidance]

**Output Format:** [Markdown instructions, workspace files, JSON configuration, Python scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates agent identity, execution, memory, and timechain data files in the user's workspace.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
