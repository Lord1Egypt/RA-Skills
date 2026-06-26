## Description: <br>
Helps agents manage construction schedules, materials, safety checks, daily and weekly reports, quantity calculations, and cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuawang658-gif](https://clawhub.ai/user/jinhuawang658-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Construction project teams and external users can use this skill through an agent to draft schedules, update progress, summarize material needs, record safety checks, generate site logs and reports, and estimate quantities. Outputs should be reviewed before use as project records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated safety, quality, daily log, and weekly report outputs may read like final project records even when they are incomplete or misleading. <br>
Mitigation: Treat these outputs as drafts and require review by qualified project staff before they are used as official construction records. <br>
Risk: Date-sensitive progress, material, safety, and report outputs may be wrong if the schedule, reference date, or generated 'no issue' statements are not checked. <br>
Mitigation: Verify all dates, schedule status, material quantities, and any 'no issue' statements against current site records before acting on the output. <br>
Risk: The progress update workflow can modify schedule files. <br>
Mitigation: Keep backups or use version control before allowing the progress script to update project schedule data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinhuawang658-gif/construction-assistant) <br>
- [Quantity formulas](references/quantity_formulas.md) <br>
- [Report templates](references/report_templates.md) <br>
- [Safety checklist](references/safety_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON schedule and record files, and shell commands for local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update local project files such as schedule JSON and report Markdown when the user supplies output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
