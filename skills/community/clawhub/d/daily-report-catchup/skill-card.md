## Description: <br>
Automatically detects missed daily reports, regenerates missing Markdown reports, updates the report index, checks report quality, and can generate a multi-agent dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colbertlee](https://clawhub.ai/user/colbertlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to detect missed workday daily reports, create catch-up reports, keep an INDEX.md status table current, and review daily-report completeness across one or more OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The catch-up workflow can silently modify hardcoded local workspace paths by writing reports, logs, state, and index entries. <br>
Mitigation: Review and edit the hardcoded workspace paths before running; use --detect for a read-only missed-report check and do not assume --quiet is read-only. <br>
Risk: The bundled skills.sh helper includes broad OpenClaw skill install, update, and uninstall controls. <br>
Mitigation: Avoid skills.sh unless you explicitly want this package to manage installed OpenClaw skills, and prefer naming a specific skill for updates instead of running a broad update. <br>
Risk: Automatically generated catch-up reports may contain placeholder content rather than the user's actual work history. <br>
Mitigation: Review generated reports before relying on them as an accurate record and edit placeholder sections with real daily context when available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/colbertlee/daily-report-catchup) <br>
- [Report quality checklist](artifact/REPORT_CHECKLIST.md) <br>
- [Daily report template](artifact/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, HTML] <br>
**Output Format:** [Markdown reports, terminal output, configuration notes, and generated HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Catch-up mode can write report files, index entries, logs, and state files; detect mode reports missed days without generating catch-up reports.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
