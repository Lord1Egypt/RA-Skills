## Description: <br>
Package completed work for handoff to another agent or a human, with each item backed by a verified APort decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and teams use this skill to create a handoff document for completed work in multi-agent workflows, sprint handoffs, feature reviews, or onboarding. The handoff records completed items, incomplete or blocked work, and APort verification links so a recipient can check each claim. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoff documents may contain secrets, internal-only details, or unnecessary personal or project metadata if saved locally or posted externally. <br>
Mitigation: Choose the storage and delivery location deliberately, and review the generated handoff before saving or sending it to GitHub, Slack, Discord, MCP messaging, or any other destination. <br>
Risk: A handoff can be misleading if it includes work without verified ALLOW decisions or decision IDs that cannot be checked. <br>
Mitigation: Include only completed items backed by verified APort ALLOW decisions, surface DENY decisions as blockers, and verify decision IDs and the issuing passport before delivery. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/uchibeke/aport-handoff) <br>
- [APort passport setup](https://aport.id) <br>
- [APort agent skill](https://aport.id/skill) <br>
- [APort decisions API](https://aport.io/api/verify/decisions/YOUR_AGENT_ID) <br>
- [APort decision verification API](https://aport.io/api/verify/decisions/get/DECISION_ID) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown handoff document with verification links and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be saved locally and optionally delivered through available channels with user permission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
