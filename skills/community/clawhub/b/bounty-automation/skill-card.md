## Description: <br>
Multi-platform bounty automation for scanning, filtering, claiming, and submitting pull requests across GitHub, Opire, Algora, and OpenTask. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkcash](https://clawhub.ai/user/mkcash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to configure an agent workflow that periodically scans bounty sources, filters likely tasks, and runs claim-to-PR automation with status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended bounty automation can use connected GitHub and OpenTask accounts to bid, claim work, modify code, push branches, open pull requests, post payment details, and send QQ notifications. <br>
Mitigation: Use this only when that automation is intended, restrict token scopes, protect credential files, and require manual approval before bids, claims, pushes, pull requests, or payment comments. <br>
Risk: The installer writes recurring OpenClaw cron jobs and can replace existing cron configuration. <br>
Mitigation: Back up existing OpenClaw cron jobs before running the installer and review the generated schedules, targets, and notification destination. <br>
Risk: Artifact evidence includes default QQ and payment/contact values that may not match the deploying user. <br>
Mitigation: Replace QQ chat identifiers and payment or contact values before enabling the scheduled workflows. <br>


## Reference(s): <br>
- [Deployment Guide](references/DEPLOY_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron setup guidance and agent workflow instructions; generated actions should be reviewed before account operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
