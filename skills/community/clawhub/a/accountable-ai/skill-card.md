## Description:

Implements governance for AI teams by defining roles, decision authority, procedures, and delegation to support accountability and traceable actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgapol](https://clawhub.ai/user/kgapol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and teams running multi-agent AI workspaces use this skill to establish governance documents, repeatable procedures, delegation protocols, memory practices, and audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad standing authority over startup files, memory, documentation, and repository pushes without enough user review controls.

Mitigation: Require explicit approval before loading bootstrap instructions, deleting files, writing long-term memory or governance changes, sharing memory files, storing credentials, or pushing to a remote repository.

Risk: Installing governance files into a workspace with sensitive data or shared repositories may change how agents read, write, and retain operational context.

Mitigation: Review the governance documents before installation and deploy first in a non-sensitive workspace or with restricted permissions.

## Reference(s):

- [Accountable AI ClawHub listing](https://clawhub.ai/kgapol/skills/accountable-ai)
- [Trust AI Stack on ClawMart](https://www.shopclawmart.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown governance documents with installation shell commands and workspace configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs governance, procedures, delegation, and README documentation for agent workspaces.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
