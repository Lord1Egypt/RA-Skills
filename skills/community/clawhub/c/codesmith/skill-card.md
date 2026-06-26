## Description: <br>
CodeSmith is a senior engineering agent configuration for OpenClaw agents that supports full-stack development automation, CI/CD work, GitHub workflows, ACP dispatch patterns, and operational coding guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawmentorai](https://clawhub.ai/user/clawmentorai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers who use OpenClaw as a coding partner use this package to configure an agent for repo work, CI/CD workflows, GitHub operations, sub-agent dispatch, memory practices, and staged cron adoption. It is intended for setups where some autonomy is earned over time and reviewed through explicit safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron jobs and ACP dispatch can increase agent autonomy before the setup has earned trust. <br>
Mitigation: Enable cron jobs one at a time, verify LOCKDOWN behavior, and require human approval for production deploys, main-branch merges, public posts, and external messages. <br>
Risk: GitHub, hosting, and delivery-channel credentials could create unnecessary exposure if they are over-permissioned. <br>
Mitigation: Keep GitHub and hosting credentials least-privilege, verify required scopes before enabling workflows, and avoid granting access that is not needed for the coding workflow. <br>
Risk: Applying the package may modify agent configuration, cron configuration, or memory files. <br>
Mitigation: Review proposed file changes, make backups before setup, approve writes explicitly, and restore from backups if the new configuration behaves unexpectedly. <br>


## Reference(s): <br>
- [CodeSmith ClawHub listing](https://clawhub.ai/clawmentorai/codesmith) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CLAW_MENTOR.md](artifact/CLAW_MENTOR.md) <br>
- [setup-guide.md](artifact/setup-guide.md) <br>
- [privacy-notes.md](artifact/privacy-notes.md) <br>
- [cron-patterns.json](artifact/cron-patterns.json) <br>
- [skills.md](artifact/skills.md) <br>
- [working-patterns.md](artifact/working-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown documentation and JSON cron configuration with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only mentor package; user approval is expected before writes, cron activation, production deploys, main-branch merges, public posts, or external messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
