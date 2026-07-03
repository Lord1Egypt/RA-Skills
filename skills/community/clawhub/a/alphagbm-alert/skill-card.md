## Description: <br>
Set price, IV, or activity-based alerts with contextual notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External AlphaGBM users and developers use this skill to configure, list, edit, and delete alerts for price levels, IV rank changes, unusual options activity, earnings timing, and VRP signal changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert-management trigger phrases may overlap with other finance or notification skills. <br>
Mitigation: Review trigger phrases before installation in environments that already use finance or notification skills. <br>
Risk: Users can request modification or deletion of alerts. <br>
Mitigation: Require explicit confirmation before deleting or modifying alerts and limit AlphaGBM API access to alert-management operations. <br>


## Reference(s): <br>
- [AlphaGBM](https://alphagbm.com) <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-alert) <br>
- [Publisher profile](https://clawhub.ai/user/clementgu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with alert configuration summaries, contextual notifications, and API endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces alert-management guidance for one-time and recurring alerts; no executable files are bundled in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
