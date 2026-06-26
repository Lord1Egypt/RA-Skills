## Description: <br>
Daily Log guides an agent to write or consolidate local daily Markdown work logs at memory/daily/YYYY-MM/YYYY-MM-DD.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to have agents record session work, decisions, changed files, commands, command output, and errors in a structured daily journal for later memory review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated daily log files can preserve command output, file paths, errors, and other project details that may be sensitive. <br>
Mitigation: Review generated memory/daily files periodically and avoid sharing or committing logs that contain sensitive project data. <br>
Risk: Older releases used a different daily log path, which can lead to duplicate logs if agents follow stale conventions. <br>
Mitigation: Use the v1.3.0 path convention memory/daily/YYYY-MM/YYYY-MM-DD.md and check for an existing daily log before writing. <br>


## Reference(s): <br>
- [Daily log specification](artifact/references/spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/daily-log) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file at memory/daily/YYYY-MM/YYYY-MM-DD.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends or consolidates entries while preserving existing daily log content.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
