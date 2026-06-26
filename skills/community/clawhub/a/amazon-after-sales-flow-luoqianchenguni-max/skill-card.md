## Description: <br>
Automates Amazon after-sales by opening orders, accessing details, running contact flow, and drafting or sending seller messages with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to automate Amazon after-sales workflows across orders, order details, contact flow, and seller message drafting or confirmed sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in Amazon browser session and read order or message page content. <br>
Mitigation: Install only when that browser access is acceptable, and avoid using it on pages containing unrelated sensitive data. <br>
Risk: The skill can send seller messages when explicit sending flags are enabled. <br>
Mitigation: Use draft-only mode by default and review message text before setting confirm_send. <br>
Risk: Browser state and captured page data may persist in local workspace directories. <br>
Mitigation: Periodically clear the local .browser-profile and artifacts directories if session or page data should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/amazon-after-sales-flow-luoqianchenguni-max) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON strings with validated inputs, status values, traces, and execution hints.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local artifact paths or browser workflow traces when actions run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
