## Description: <br>
Closeli Device Event Query API supports natural language queries for device events and returns an AI summary and event list, including event types, time ranges, and image or video URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[closeli-open](https://clawhub.ai/user/closeli-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Closeli device events with natural language questions and receive summarized event results with timestamps, recognized tags, scene descriptions, and thumbnail links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive API credentials and device-event data. <br>
Mitigation: Use a least-privilege API key and install the skill only in a trusted OpenClaw environment. <br>
Risk: The shared configuration file can expose credentials to other skills running as the same user. <br>
Mitigation: Restrict permissions on ~/.openclaw/.env and limit access to the OpenClaw service user. <br>
Risk: Disabling TLS verification or using an unexpected gateway host can expose credentials and device data. <br>
Mitigation: Keep TLS verification enabled and confirm AI_GATEWAY_HOST points to the expected trusted service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/closeli-open/api-event-query) <br>
- [Publisher Profile](https://clawhub.ai/user/closeli-open) <br>
- [Default AI Gateway Host](https://ai-open.icloseli.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance for running a Python command and formatting JSON API results for users.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script returns JSON for agent-side formatting; event output is trimmed before display and may include thumbnail links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
