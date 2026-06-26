## Description: <br>
Executes mobile automation tasks on Volcengine Cloud Phone using natural language commands, returning run IDs and progress in JSONL format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to start, monitor, retrieve results from, and cancel Volcengine Mobile Use Agent runs on Cloud Phone instances for mobile UI automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live Volcengine Cloud Phone sessions. <br>
Mitigation: Install it only when mobile automation on those resources is intended, and require human confirmation before purchases, messages, logins, account changes, or sensitive form submissions. <br>
Risk: The skill requires sensitive cloud or proxy credentials. <br>
Mitigation: Use least-privilege scoped credentials through environment variables, a trusted proxy, or a secrets manager, and avoid passing secrets on the command line. <br>
Risk: Screen recording can capture sensitive information. <br>
Mitigation: Enable screen recording only after confirming the object storage bucket, access controls, and retention policy are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-ai-mobileuse-agent) <br>
- [Mobile Use Agent execution setup guide](references/MUA_Agent_Instructions.md) <br>
- [Mobile Use Agent overview](references/mobile_use.md) <br>
- [Volcengine Mobile Use Agent console](https://console.volcengine.com/ACEP/Business/6) <br>
- [Volcengine publish app instructions](https://www.volcengine.com/docs/6394/1223958?lang=zh) <br>
- [Volcengine screen recording documentation](https://www.volcengine.com/docs/6394/1997312?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSONL command output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime scripts emit JSON objects for started, progress, result, and error events.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
