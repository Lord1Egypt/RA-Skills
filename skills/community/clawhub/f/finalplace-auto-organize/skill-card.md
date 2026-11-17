## Description:

Drives the installed FinalPlace Windows desktop app's auto-rules CLI to create, preview, execute, and manage rules that organize files by extension, name, size, time, path, or content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csjfeiyang-arch](https://clawhub.ai/user/csjfeiyang-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop automation agents use this skill on Windows when a user explicitly wants FinalPlace to organize, archive, compress, unzip, rename, move, copy, or delete files through its rule engine. It is intended for workflows where the agent translates the user's request into FinalPlace rules, previews or dry-runs matches when appropriate, and requires confirmation before file-modifying actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive workflows that move, delete, rename, compress, unzip, or copy user files, and rules may persist or run on a schedule.

Mitigation: Require explicit user confirmation after reviewing the source folder, match conditions, action, destination, and whether the rule will persist or run on a schedule; use preview or dry-run before execution when possible.

Risk: Installer guidance can lead users to run a direct Windows executable.

Mitigation: Prefer the Microsoft Store installation path or independently verify the installer publisher and hash before running the direct EXE.

Risk: Feedback submission may send the title, content, account association, and diagnostic details to the developer.

Mitigation: Confirm the feedback title and content with the user and submit only when the user is comfortable sharing the associated details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/csjfeiyang-arch/skills/finalplace-auto-organize)
- [Server-resolved GitHub provenance](https://github.com/csjfeiyang-arch/finalplace-auto-organize)
- [FinalPlace website](https://www.finalplace.cn/)
- [FinalPlace English website](https://www.finalplace.cn/en/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets the installed Windows FinalPlace binary, discovered from FINALPLACE_EXE or the FinalPlace executable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
