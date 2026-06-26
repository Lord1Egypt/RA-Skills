## Description: <br>
Cron Evaluator analyzes cron jobs for health, resource usage, timing collision risk, resilience, and improvement opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to audit cron schedules, identify collision and resource risks, assess resilience practices such as logging and locking, and plan cron or systemd timer improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and display local cron command lines, which may expose operational details. <br>
Mitigation: Run it only in environments where cron contents may be inspected, and review outputs before sharing them. <br>
Risk: Some scripts include hard-coded local paths and local module imports. <br>
Mitigation: Review or remove the /mnt, /home/axioma, and /run/media paths and avoid importing unreviewed local modules before execution. <br>
Risk: The v3 script loads a local PyTorch model file. <br>
Mitigation: Use a verified safe model artifact or safe PyTorch loading settings before running model-backed evaluation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/cron-evaluator) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown-oriented guidance with command examples and cron health findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report cron command lines and local schedule details when run against a system crontab.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
