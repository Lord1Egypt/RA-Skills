## Description: <br>
Automatically monitor and claim ClawPI red packets without manual intervention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation operators use this skill to periodically check ClawPI red packets, claim eligible packets, notify a Discord channel, and maintain local claim history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended use of wallet identity can create payment links and claim red packets without interactive review. <br>
Mitigation: Run only when automatic claiming is intentional, and use an account and wallet configuration scoped to this purpose. <br>
Risk: The skill can post public celebration moments and send claim details to a Discord channel. <br>
Mitigation: Confirm posting and notification destinations before enabling scheduled runs, and disable public posting where disclosure is not desired. <br>
Risk: Security evidence recommends safer API calls instead of shell interpolation. <br>
Mitigation: Review the script before deployment and prefer a version that avoids shell-interpolated requests for user-controlled values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/clawpi-redpacket-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/sunnyhot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Files, Notifications] <br>
**Output Format:** [Node.js script execution with JSON configuration, local status JSON, Discord notifications, and ClawPI API side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates payment links, claims red packets, can post celebration moments, and records local claim state when run with configured credentials.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
