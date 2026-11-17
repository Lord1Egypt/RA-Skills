## Description:

Create, share, import, render, and manage standardized Feishu ClawBot identity cards for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmyaoyuan](https://clawhub.ai/user/hmyaoyuan)

### License/Terms of Use:

ISC

## Use Case:

Developers and Feishu bot operators use this skill to mint local FCC v1 identity cards, exchange them with other agents, and render cards as Feishu rich text JSON for chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendered cards can include import commands built from untrusted card text.

Mitigation: Treat received cards as untrusted data and rewrite import actions into a safe file-based or stdin-based workflow before execution.

Risk: The skill modifies the local rolodex.json registry when minting or importing cards.

Mitigation: Review registry changes after use and keep backups or version control for local card data.

Risk: Dependency posture may change over time.

Mitigation: Pin or update Node.js dependencies before deployment and review the lockfile as part of installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmyaoyuan/skills/feishu-clawbot-card)
- [Feishu ClawBot Card usage guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and Feishu rich text JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reads and writes a local rolodex.json registry and validates cards against the FCC v1 schema.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
