## Description: <br>
Runs local bash scripts on schedules through an OpenClaw gateway startup hook without LLM involvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdxbsv](https://clawhub.ai/user/gdxbsv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install a gateway hook that schedules trusted local bash scripts for routine jobs such as health checks, cleanup, backups, and fixed notifications without invoking an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent hook that can run local shell scripts unattended with the gateway user's privileges and environment. <br>
Mitigation: Install it only when automatic local script execution is intended, and run the gateway under a low-privilege account where possible. <br>
Risk: Scripts in ~/.openclaw/cron-scripts can access the gateway user's files, network, and environment variables. <br>
Mitigation: Treat ~/.openclaw/cron-scripts as a trusted-code directory, lock down its permissions, and review every script before adding it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdxbsv/cron-scripts) <br>
- [OpenClaw issue #80793: Support script target type in openclaw cron](https://github.com/openclaw/openclaw/issues/80793) <br>
- [OpenClaw issue #18160: Direct Exec Mode for Cron Jobs](https://github.com/openclaw/openclaw/issues/18160) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with TypeScript and bash files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a persistent gateway startup hook that watches a trusted local scripts directory and runs matching shell scripts on cron schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
