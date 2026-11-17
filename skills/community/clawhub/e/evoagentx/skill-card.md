## Description:

EvoAgentX - Self-evolving AI agents framework integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to install, check, document, and run EvoAgentX workflows for self-evolving AI agent experiments or applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys may be exposed if hardcoded, pasted into shared prompts, or stored in logs.

Mitigation: Use environment secrets, avoid committing keys, and rotate any key that may have been exposed.

Risk: Workflow goals and prompts may be sent to the selected model provider.

Mitigation: Review data sensitivity before running workflows and use only approved providers for confidential material.

Risk: The evoagentx dependency is not pinned to a specific package version.

Mitigation: Install in an isolated environment and review the resolved package version before use.

Risk: The skill references a PowerShell helper script that is not included in the artifact evidence.

Mitigation: Confirm the helper script exists and review it before executing the documented commands.

## Reference(s):

- [EvoAgentX GitHub repository](https://github.com/EvoAgentX/EvoAgentX)
- [EvoAgentX website](https://evoagentx.org)
- [ClawHub skill page](https://clawhub.ai/nantes/skills/evoagentx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on Python 3.12, the evoagentx package, and provider API keys.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
