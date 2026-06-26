## Description: <br>
Automatically monitors OpenClaw gateway status and runs OpenClaw repair commands when the RPC probe fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwcalvin](https://clawhub.ai/user/nwcalvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run OpenClaw use this skill to install or configure a recurring health check that repairs and restarts the gateway after an RPC probe failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent one-minute auto-repair job can repeatedly change OpenClaw configuration and restart the gateway without further approval. <br>
Mitigation: Review the script before enabling it, use a longer interval or add cooldown and retry limits where appropriate, and confirm the removal procedure before installation. <br>
Risk: Unattended repair can continue running after it is no longer wanted. <br>
Mitigation: Remove the scheduled job with `openclaw cron rm gateway-auto-fix` and delete `~/.openclaw-it/workspace/openclaw-auto-fix.sh` when disabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nwcalvin/gateway-auto-fix) <br>
- [Publisher profile](https://clawhub.ai/user/nwcalvin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with bash commands and shell script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a shell script, configures an OpenClaw cron job, and writes operational logs to /tmp/openclaw-auto-fix.log.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
