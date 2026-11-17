## Description:

Fixes Chinese and Unicode character encoding issues when AI agents run on Windows through POSIX shells by providing UTF-8 handling guidance for Python, PowerShell, and cmd.exe output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gkd2323c](https://clawhub.ai/user/gkd2323c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to diagnose and fix garbled Chinese or Unicode output when running coding agents in Windows POSIX-style shells such as Git Bash, MSYS2, BusyBox, or WSL-like environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional helper commands invoke Windows shell tools such as powershell.exe and cmd.exe.

Mitigation: Review the visible commands before execution and run them only in the intended Windows terminal environment.

Risk: Encoding overrides can change output behavior for a shell session or process.

Mitigation: Prefer command-scoped or session-scoped settings such as PYTHONIOENCODING=utf-8, then verify output with the documented test command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gkd2323c/skills/charset-fix)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell, PowerShell, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused guidance; optional diagnostic script requires python3 and Windows shell tools.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
