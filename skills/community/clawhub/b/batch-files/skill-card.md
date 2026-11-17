## Description:

Expert-level Windows batch file skill for writing, debugging, and maintaining .bat and .cmd scripts for cmd.exe automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and automation engineers use this skill to create, troubleshoot, and maintain Windows cmd.exe batch scripts for file operations, scheduled tasks, CLI utilities, and integration with external tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe administrator-access or persistence guidance could be applied without authorization.

Mitigation: Review generated commands before use, and avoid recovery-account, SYSTEM-shell, AutoRun/startup, or similar patterns unless explicitly authorized with a rollback plan.

Risk: Starter batch templates may be unsafe when adapted to untrusted inputs.

Mitigation: Add input validation, quote paths and variables carefully, and test scripts in a non-production environment before deployment.

Risk: Plaintext FTP patterns can expose credentials or sensitive data.

Mitigation: Avoid plaintext FTP for sensitive workflows and prefer authenticated secure transfer tools or managed credential storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/batch-files)
- [Batch Files, Scripts, and Functions](artifact/references/batch-files-and-functions.md)
- [Windows Commands Reference](artifact/references/windows-commands.md)
- [Tools and Resources](artifact/references/tools-and-resources.md)
- [Cygwin Reference](artifact/references/cygwin.md)
- [MSYS2 Reference](artifact/references/msys2.md)
- [Windows Subsystem for Linux Reference](artifact/references/windows-subsystem-on-linux.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Windows batch code blocks and reusable .bat/.cmd templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows cmd.exe focused; generated commands and templates should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
