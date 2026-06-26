## Description: <br>
Generate a standup update from your APort policy decisions, showing what was shipped from signed APort decisions rather than memory or estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, teams, and AI-agent operators use this skill to generate factual daily, weekly, or team standup updates from recent APort decision records. It helps surface completed work, denied or blocked attempts, completion stats, and audit-ready decision IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external APort decision history that can reveal work history, blockers, and status details. <br>
Mitigation: Use it only in chats where those details may be disclosed, and confirm `APORT_AGENT_ID` points to the intended agent before fetching decisions. <br>
Risk: Setup instructions reference separate APort tools and external setup flows. <br>
Mitigation: Review the APort setup tools before running `npx aport-id` or following external setup instructions. <br>


## Reference(s): <br>
- [Aport Standup ClawHub page](https://clawhub.ai/uchibeke/aport-standup) <br>
- [Create an APort passport](https://aport.id) <br>
- [APort agent skill setup](https://aport.id/skill) <br>
- [APort decision history endpoint](https://aport.io/api/verify/decisions/YOUR_AGENT_ID) <br>
- [APort decision verification endpoint](https://aport.io/api/verify/decisions/get/DECISION_ID) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown standup summary with completion stats, blockers, and decision IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include APort API endpoint examples and audit trail identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
