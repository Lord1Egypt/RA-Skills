## Description:

Audit Homebrew installation - outdated packages, cleanup opportunities, and health checks for macOS package maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit a macOS Homebrew installation for outdated packages, cleanup opportunities, and health issues before maintenance or upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output may prompt package upgrades or cleanup that change installed software or remove cached versions if run separately.

Mitigation: Review the audit output before manually running brew upgrade or brew cleanup commands.

Risk: The skill inspects local Homebrew package state on the user's machine.

Mitigation: Install and run it only when local Homebrew package inspection is intended.

## Reference(s):

- [Homebrew Homepage](https://brew.sh)
- [ClawHub Skill Page](https://clawhub.ai/rogue-agent1/skills/brew-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON from the audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Homebrew on macOS; the audit script supports full audits, sectional audits, and JSON output for outdated packages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
