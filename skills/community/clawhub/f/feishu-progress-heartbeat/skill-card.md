## Description: <br>
Use in Feishu when long-running tasks should proactively report progress every 3 minutes with concise, stage-based status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using Feishu for delegated long-running work use this skill to send compact progress heartbeats, estimated stage percentages, and blocker notices while work continues in the background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic heartbeat messages may surprise users or add noise in Feishu conversations where they are not expected. <br>
Mitigation: Enable the skill only in conversations where participants expect periodic progress updates, and suppress messages when there is no meaningful state change. <br>
Risk: Stage-based percentages could be mistaken for exact completion measurements. <br>
Mitigation: Phrase percentages as approximate estimates and tie them to observable task stages rather than exact progress claims. <br>
Risk: The Chinese status wording may not match every workspace's communication norms. <br>
Mitigation: Confirm the language and tone are appropriate for the workspace before broad use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wd041216-bit/feishu-progress-heartbeat) <br>
- [Project homepage](https://github.com/wd041216-bit/openclaw-feishu-progress-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Short Feishu-friendly status lines or HEARTBEAT_OK] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stage-based percentage estimates and avoids updates when there is no meaningful task progress.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
