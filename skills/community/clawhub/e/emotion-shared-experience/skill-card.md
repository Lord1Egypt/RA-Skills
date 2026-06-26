## Description: <br>
Emotion detects user emotions, provides supportive responses, and saves local context and emotion history for cross-session personalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyds-xxxx](https://clawhub.ai/user/yyds-xxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to add an always-on emotional companion that detects mood, responds supportively, and keeps local memory for continuity across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on activation may capture sensitive emotional text without clear user intent. <br>
Mitigation: Disable always-on and no-prefix activation unless users have explicitly opted in. <br>
Risk: The skill may store excerpts of private or mental-health-adjacent conversations locally. <br>
Mitigation: Require explicit memory consent and provide review, export, and delete controls before use. <br>
Risk: Unused web-search access expands the skill's operational surface. <br>
Mitigation: Remove unused web-search access unless a deployment specifically needs it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yyds-xxxx/emotion-shared-experience) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Text response with JSON-compatible metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include emotion, intensity, detection status, context count, and timestamp metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
