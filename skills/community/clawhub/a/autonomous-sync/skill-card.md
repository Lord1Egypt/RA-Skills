## Description: <br>
Helps agents set up automatic Aicoo knowledge syncs using scheduled loops, cron, hooks, file watchers, and API update workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep Aicoo knowledge current by setting up scheduled or event-driven sync workflows for decisions, preferences, project updates, meeting outcomes, and policy changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background syncs may send sensitive project or conversation data to an external service without enough scoping or review. <br>
Mitigation: Define exactly what may be synced, exclude secrets and confidential files, and prefer manual review before external writes. <br>
Risk: Cron jobs, loops, hooks, or file watchers can make persistent external updates after they are enabled. <br>
Mitigation: Enable automation only intentionally, keep trigger scope narrow, and review proposed changes before allowing unattended runs. <br>
Risk: Aicoo API credentials are required for the workflows. <br>
Mitigation: Store AICOO_API_KEY only in protected environment or secret storage, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/autonomous-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API requests] <br>
**Output Format:** [Markdown with shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICOO_API_KEY and sends selected sync content to the Aicoo API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
