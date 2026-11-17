## Description:

AI Operation Undo System. When user executes /ctrlZ or says "undo last step", automatically revert all file modifications, installations, etc. from the recent conversation round. Default keeps 1 undo unit, configurable to 3 or 5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisluo5311](https://clawhub.ai/user/chrisluo5311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use CtrlZ to record AI-created file, directory, and package-install operations by conversation round so recent changes can be listed or reverted on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undo operations can overwrite or delete user files from stored records without confirmation.

Mitigation: Review carefully before installing, use only disposable or well-backed-up workspaces, and add path scoping plus explicit confirmation before undo and clear operations.

Risk: Plaintext backups can retain sensitive file contents.

Mitigation: Protect the backup directory, avoid recording sensitive paths, and clear retained backups when they are no longer needed.

Risk: Package installations and shell command side effects may not be fully reversible.

Mitigation: Treat package removal output as manual follow-up guidance and verify the environment state after any undo.

## Reference(s):

- [CtrlZ Skill Page](https://clawhub.ai/chrisluo5311/skills/ctrlz)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [TEST_CASES.md](artifact/TEST_CASES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill records undo sessions in SQLite, stores file backups, lists manual removal commands for package installs, and cannot fully reverse external shell command side effects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
