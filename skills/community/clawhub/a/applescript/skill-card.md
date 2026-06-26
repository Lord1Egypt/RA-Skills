## Description: <br>
Write and run safe AppleScript automation on macOS with dictionary discovery, robust quoting, and deterministic read-first workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to design, run, and troubleshoot macOS AppleScript workflows for app control, data extraction, and scripted UI actions while applying read-first and confirmation-based safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AppleScript can automate local macOS apps and may affect app data if a proposed script is run without review. <br>
Mitigation: Review proposed scripts before execution, grant Automation permissions only for intended apps, and require explicit confirmation for writes or destructive actions. <br>
Risk: Automation memory in ~/applescript/ may contain sensitive app details or workflow notes. <br>
Mitigation: Review the local ~/applescript/ directory before sharing logs or files, and store only reusable automation context needed for future tasks. <br>
Risk: Incorrect app dictionary terms or unescaped user input can cause runtime failures or target the wrong object. <br>
Mitigation: Inspect the target app dictionary first, use deterministic quoting patterns, run read-only probes, and verify state after writes. <br>


## Reference(s): <br>
- [ClawHub AppleScript Skill](https://clawhub.ai/ivangdavila/applescript) <br>
- [AppleScript Skill Homepage](https://clawic.com/skills/applescript) <br>
- [Setup](artifact/setup.md) <br>
- [App Dictionary Workflow](artifact/app-dictionary-workflow.md) <br>
- [Script Patterns](artifact/script-patterns.md) <br>
- [Safety Checklist](artifact/safety-checklist.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with AppleScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise structured command output, read-back verification results, and local configuration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
