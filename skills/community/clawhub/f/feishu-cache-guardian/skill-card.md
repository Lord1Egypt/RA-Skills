## Description: <br>
Feishu Cache Guardian checks and repairs the OpenClaw Feishu plugin probe cache settings so health-check responses use a 60-minute cache and avoid rapidly consuming Feishu API quota. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhs0430-sudo](https://clawhub.ai/user/zhs0430-sudo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw Feishu integrations use this skill to check whether plugin upgrades reset probe cache timings and to reapply the intended 60-minute cache behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit a system-installed OpenClaw Feishu plugin file. <br>
Mitigation: Review the target file and keep a backup before applying repairs. <br>
Risk: The repair script can restart the OpenClaw Gateway. <br>
Mitigation: Run it manually first and schedule recurring execution only after the restart behavior is understood. <br>
Risk: Recurring automation can repeatedly reapply changes after OpenClaw upgrades. <br>
Mitigation: Use a cadence and review process that fits the deployment's change-management practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhs0430-sudo/feishu-cache-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute a local Node.js repair script that edits an OpenClaw installation file and restarts the Gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
