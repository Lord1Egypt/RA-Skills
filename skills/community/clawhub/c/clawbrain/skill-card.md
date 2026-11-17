## Description:

Claw Brain is a personal AI memory system for OpenClaw/ClawDBot that provides memory, personality, bonding, learning, encrypted secrets support, and automatic memory refresh on service restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawcolab](https://clawhub.ai/user/clawcolab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Claw Brain to give OpenClaw/ClawDBot agents persistent local memory, user profile context, personality state, and optional encrypted secret storage across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain conversation and profile data across sessions.

Mitigation: Install only when persistent memory is expected, use a pinned and reviewed release, and run the agent under a dedicated low-privilege user.

Risk: Startup hooks can automatically affect agent behavior when the service starts.

Mitigation: Inspect the hook before enabling it and review hook changes before updating the skill.

Risk: Most conversation and profile data is stored in plaintext by default, while only explicit secret memories are encrypted.

Mitigation: Treat the memory database and encryption key as sensitive files, restrict file permissions, and avoid storing secrets outside the secret memory type.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawcolab/skills/clawbrain)
- [Security documentation](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.15 (source: server release metadata; artifact frontmatter lists 0.1.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
