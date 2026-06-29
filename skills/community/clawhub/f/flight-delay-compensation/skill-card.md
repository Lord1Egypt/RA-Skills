## Description: <br>
零配置即装即用，输入航班号自动查延误并计算赔偿金额，覆盖6大法域含索赔信生成，基于飞常准实时数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-assistance agents use this skill to check flight delay status, estimate compensation eligibility across supported jurisdictions, compare rules, and draft claim letters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight numbers, dates, and passenger names can be sensitive travel information when sent through the publisher's Tencent SCF proxy to the flight-data provider. <br>
Mitigation: Only enter the minimum flight details needed for the task, avoid unnecessary personal details, and review generated claim letters before adding contact or identity information. <br>
Risk: Compensation estimates and claim text may not match the final airline decision or current legal interpretation. <br>
Mitigation: Treat outputs as drafting and triage assistance, verify eligibility against the airline or regulator, and preserve boarding passes, delay notices, and other evidence. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/travel-skills/flight-delay-compensation) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown and JSON error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces flight delay assessments, compensation rule summaries, and claim-letter drafts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release, artifact/VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
