## Description:

Automatically records and backs up OpenClaw conversations with importance tagging to preserve emotional and technical context outside OpenClaw internals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfanmy](https://clawhub.ai/user/zfanmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and configure local conversation backups. It records agent exchanges with importance tags and keeps recovery-friendly Markdown and JSONL history files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete agent exchanges may be copied into local plaintext history, including passwords, tokens, or private data.

Mitigation: Add redaction rules before recording sensitive content, restrict file permissions on the memory directory, and define a retention policy for backups.

Risk: The installation instructions include downloading executable shell code from a mutable remote URL without an integrity check.

Mitigation: Use the bundled script or a pinned verified release, review the shell commands before installation, and verify checksums where available.

## Reference(s):

- [Conversation Guard ClawHub Page](https://clawhub.ai/zfanmy/skills/conversation-guard)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [VERSION-ISOLATION.md](artifact/VERSION-ISOLATION.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash snippets; generated local Markdown and JSONL conversation logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local plaintext history files are written under the configured memory directory.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact documentation and script state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
