## Description:

Agent Sbti runs a Chinese-language SBTI-style personality quiz, generates a personality report, and helps configure an OpenClaw agent's SOUL.md communication style with backup and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to take a Chinese-language SBTI-style personality quiz, review the resulting personality profile, and generate a matching, complementary, tuned, or custom agent personality configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the user's OpenClaw SOUL.md configuration after confirmation.

Mitigation: Review the generated configuration preview before confirming any write to SOUL.md.

Risk: Rollback replaces the current SOUL.md with a previous backup.

Mitigation: Keep track of the backup path and confirm the intended backup before using rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/agent-sbti)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands]

**Output Format:** [Chinese-language Markdown-style conversational responses, JSON-like configuration snippets, and local SOUL.md file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before applying configuration; backups are kept under ~/.openclaw/workspace/backup/agent-sbti/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
