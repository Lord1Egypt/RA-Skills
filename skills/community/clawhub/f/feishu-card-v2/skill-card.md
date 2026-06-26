## Description: <br>
Helps agents create, send, and update Feishu Card JSON 2.0 interactive cards for forms, choices, confirmations, and structured data views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afk101](https://clawhub.ai/user/afk101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill when an agent should send Feishu interactive cards instead of plain text, including forms, selections, confirmation prompts, and structured data displays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cards may be sent to the wrong Feishu chat or user. <br>
Mitigation: Verify chat_id, open_id, union_id, or email recipients before sending or updating cards. <br>
Risk: Card fields and callback payloads can expose secrets, regulated personal data, or sensitive business details. <br>
Mitigation: Avoid including secrets or unnecessary sensitive data in card content, form fields, and actionValue payloads. <br>
Risk: Overly broad Feishu app credentials increase blast radius if misused. <br>
Mitigation: Use least-privilege Feishu app permissions and the intended configured accountId. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afk101/feishu-card-v2) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Configuration, Guidance] <br>
**Output Format:** [Feishu Card JSON 2.0 objects and tool-call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Feishu account credentials and the built-in Feishu callback handling plugin.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
