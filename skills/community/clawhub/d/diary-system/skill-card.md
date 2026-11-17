## Description:

Configure an AI diary system for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adolescen-he](https://clawhub.ai/user/adolescen-he)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to set up a persistent AI diary feature, including workspace diary storage, diary templates, and configuration snippets for SOUL.md, USER.md, and AGENTS.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists diary entries and changes SOUL.md, USER.md, and AGENTS.md, which can alter core agent behavior across sessions.

Mitigation: Install only with explicit user approval, review each appended configuration block before use, and keep a rollback copy of the affected files.

Risk: Diary content can retain user observations, sensitive context, or private agent state and can later be shown in full.

Mitigation: Avoid storing sensitive data, require confirmation before writing or displaying diary contents, and periodically review or delete retained diary files.

Risk: The included easter egg and delayed-task behavior can lead to unsolicited actions outside the immediate user request.

Mitigation: Remove those rules or gate them behind explicit confirmation before enabling the skill in normal use.

## Reference(s):

- [Skill README](artifact/README.md)
- [SOUL.md diary module](artifact/references/soul-module.md)
- [USER.md diary tracking state](artifact/references/user-module.md)
- [AGENTS.md startup check](artifact/references/agents-module.md)
- [Automation rules](artifact/references/automation-rules.md)
- [Diary template](artifact/assets/diary-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update diary files and append configuration blocks when the user chooses to install it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
