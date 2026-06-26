## Description: <br>
Query and create field observations and AI-processed captures. Photos, voice notes, and text notes from the field. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm operators, agronomists, and field teams use this skill to query, summarize, and log FarmOS field observations from text, voice notes, and photos, including pests, disease, weeds, crop condition, weather damage, soil issues, and equipment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use manager-level authentication to create FarmOS records, upload photos, and send urgent alerts. <br>
Mitigation: Use a least-privileged token, confirm the action details with the user before writes or alerts, and avoid silent record creation. <br>
Risk: The skill relies on a hard-coded internal FarmOS backend that may be unavailable or unintended for the user's environment. <br>
Mitigation: Confirm the endpoint belongs to the deployment environment and report service failures plainly instead of treating empty or failed responses as no observations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianppetty/farmos-observations) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/brianppetty) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline API and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create FarmOS observation records, upload photos, or escalate urgent alerts after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
