## Description: <br>
Cron 评估器 — 分析和评分 cron 任务，用于健康检查、资源使用、冲突检测和弹性改进。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to audit cron jobs, detect timing conflicts, review resource and resilience issues, and plan systemd timer migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and display cron command lines from the machine where it runs. <br>
Mitigation: Use it only where reviewing local cron content is acceptable, or run it on pasted or explicitly selected cron entries. <br>
Risk: Local model or workspace files can affect execution if untrusted files are present at expected paths. <br>
Mitigation: Review local model and workspace paths before running, and do not place untrusted files at models/cron_kan.pt or /mnt/Morgana paths. <br>


## Reference(s): <br>
- [Skill source: SKILL.md](SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/cron-evaluator-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with cron health scores, findings, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested cron jitter, logging, flock, timeout, and systemd migration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
