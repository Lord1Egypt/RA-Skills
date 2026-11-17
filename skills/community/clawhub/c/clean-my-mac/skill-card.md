## Description:

cleanMyMacSkill helps agents analyze disk usage across macOS, Windows, and Linux, classify cleanup candidates, generate shell cleanup guidance, and build an interactive HTML storage report with optional local cleanup actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peizhou](https://clawhub.ai/user/peizhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and support engineers use this skill to inspect local disk usage, identify large files and directories, and produce prioritized cleanup guidance. It can generate a static report for analysis-only use or launch a local web dashboard for reviewed trash/delete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes optional local server actions that can move files to trash or permanently delete allowlisted paths.

Mitigation: Use static report mode for analysis-only workflows; only launch server mode after reviewing the generated cleanup targets.

Risk: Permanent deletion is irreversible and the security evidence flags hard-delete path validation as too broad for a low-risk cleanup tool.

Mitigation: Prefer trash actions, keep backups, and manually verify every target path before using permanent delete.

Risk: Documentation describes the scanner as read-only, but the full skill also supports interactive cleanup actions.

Mitigation: Communicate the distinction between scan/report generation and server cleanup mode before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peizhou/skills/clean-my-mac)
- [English README](artifact/README.en.md)
- [macOS Storage Layout & Classification Reference Guide](artifact/references/macos.md)
- [Windows Storage Layout & Classification Reference Guide](artifact/references/windows.md)
- [Linux Storage Layout & Classification Reference Guide](artifact/references/linux.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell command snippets, JSON scan data, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library scripts to produce scan JSON and either a static HTML dashboard or a local interactive dashboard.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence, released 2026-06-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
