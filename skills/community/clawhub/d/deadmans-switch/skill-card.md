## Description: <br>
Self-healing infrastructure guardian. Monitors services, diagnoses failures, executes recovery playbooks, and learns from incidents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peres84](https://clawhub.ai/user/peres84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check Linux infrastructure health, diagnose outages in a fixed order, run recovery playbooks for Tailscale, nginx, disk, and process failures, and summarize what was checked or repaired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can restart services, prune Docker artifacts, delete logs or temporary files, create cron jobs, and edit playbooks while repairing Linux infrastructure. <br>
Mitigation: Require explicit confirmation before service restarts, process killing, Docker prune, log or temporary-file deletion, cron creation, and playbook edits. <br>
Risk: The skill may send operational details to external services when Tavily-derived fixes or ElevenLabs voice alerts are configured. <br>
Mitigation: Review what infrastructure details may be shared before enabling those integrations, and avoid including secrets or sensitive operational data. <br>
Risk: The authoritative security verdict is suspicious because the skill performs powerful automatic system changes, even though it appears to be a legitimate infrastructure repair skill. <br>
Mitigation: Install only when automatic repair is intended, review each recovery playbook, and run the skill with least-privilege access appropriate to the target host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peres84/deadmans-switch) <br>
- [Publisher profile](https://clawhub.ai/user/peres84) <br>
- [Disk Space Recovery Playbook](playbooks/disk.md) <br>
- [Nginx + Website Monitoring Playbook](playbooks/nginx.md) <br>
- [Generic Crashed Process Recovery Playbook](playbooks/process.md) <br>
- [Tailscale Funnel Recovery Playbook](playbooks/tailscale.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown health reports with inline shell commands and JSONL logging examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational summaries, recovery actions taken, cron-monitoring commands, and fix-log entries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
