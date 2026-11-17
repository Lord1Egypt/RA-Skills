## Description:

Inventory local command-line tools, inspect their origins and capabilities, and install, upgrade, or remove them through their owning package managers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelegele](https://clawhub.ai/user/kelegele)

### License/Terms of Use:

MIT

## Use Case:

Developers and other technical users can use the skill to inventory local command-line tools, check versions and references, inspect available commands, and manage tools through their package managers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious and reports concerns involving unrelated agent-session functionality, uninstall and package-routing behavior, an unpinned installer, and an incomplete scan.

Mitigation: Follow the security guidance: avoid installation until the author clarifies the agent-session functionality, addresses the uninstall and package-routing risks, and the code has been fully reviewed.

## Reference(s):

- [CLI Butler requirements](artifact/docs/REQUIREMENTS.md)
- [CLI Butler provenance and channel model](artifact/docs/provenance.md)
- [CLI Butler ClawHub page](https://clawhub.ai/kelegele/skills/cli-butler)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text and shell commands with Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install, upgrade, or uninstall local tools when requested by the user.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
