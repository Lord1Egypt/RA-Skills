## Description:

Provides OpenClaw agents with persona templates, memory and security conventions, optional briefings, and in-chat commands; requires OpenClaw 2026.8.1 or later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use the skill to create a customized agent persona and organize a workspace for memory, workflows, and security practices. Optional features provide pulse checks, scheduled briefings, and Discord routing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-audit output may expose sensitive matches.

Mitigation: Redact credential-audit output and parse selected configuration fields rather than displaying whole matching lines.

Risk: Scheduled briefings may share private summaries with unintended audiences.

Mitigation: Keep scheduled tasks disabled until permitted source channels and recipients are selected; use --no-deliver for internal processing.

Risk: Automatic cleanup or upgrade steps may remove saved information.

Mitigation: Back up the workspace and require approval before memory removal or persona replacement.

## Reference(s):

- [AI Persona OS on ClawHub](https://clawhub.ai/jeffjhunter/skills/ai-persona-os)
- [AI Persona OS homepage](https://os.aipersonamethod.com)
- [Automation guide](artifact/references/automations.md)
- [Security patterns](artifact/references/security-patterns.md)
- [Never-Forget Protocol](artifact/references/never-forget-protocol.md)
- [SOUL.md Maker guide](artifact/references/soul-md-maker.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration files, Shell commands, Guidance]

**Output Format:** [Markdown workspace files, configuration guidance, and optional shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates files in the configured OpenClaw workspace; optional automations and routing configuration are user-controlled.]

## Skill Version(s):

2.1.0 (source: frontmatter, changelog, released 2026-11-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
