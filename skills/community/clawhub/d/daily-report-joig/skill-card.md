## Description:

生成简洁的中文日报（highlights/blockers/next），并可落盘为 Markdown 文件，适合个人复盘与同步。

This skill is ready for commercial/non-commercial use.

## Publisher:

[joifg](https://clawhub.ai/user/joifg)

### License/Terms of Use:


## Use Case:

Individuals use this skill to turn daily highlights, blockers, and next steps into a concise Chinese Markdown daily report for review or status sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write the generated report to a user-supplied path, which may overwrite or create files outside the intended report location.

Mitigation: Use the default reports/{date}-daily-report.md path or another clearly safe workspace path; avoid absolute paths, ../ traversal, and existing project or configuration files unless overwrite is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joifg/skills/daily-report-joig)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured response plus a Markdown daily-report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status, summary, report path data, and a suggested next action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
