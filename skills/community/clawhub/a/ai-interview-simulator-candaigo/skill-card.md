## Description: <br>
AI Interview Simulator is a Candaigo API guide for browsing jobs, creating and joining AI group interview rooms, sending interview messages, advancing interviews, uploading resumes, and viewing history and evaluations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hangeaiagent](https://clawhub.ai/user/hangeaiagent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to Candaigo's AI group interview simulator API. It supports job discovery, room creation and start flows, candidate speech, interview advancement, message polling, result review, history lookup, and optional resume upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interview content and resumes are sent to Candaigo when the documented API flows are used. <br>
Mitigation: Install only if Candaigo is trusted for this data, review Candaigo privacy and retention terms, redact unnecessary personal information, and explicitly approve resume uploads. <br>
Risk: Candaigo API keys can grant access to interview resources if exposed in shared chats, logs, or public code. <br>
Mitigation: Use a dedicated API key, avoid hardcoding it, keep it out of public artifacts, and rotate it if exposure is suspected. <br>
Risk: The skill documents state-changing actions such as starting rooms, sending speech, advancing interviews, and uploading files. <br>
Mitigation: Require explicit user approval before executing state-changing requests and review request payloads before sending them. <br>


## Reference(s): <br>
- [Candaigo API base URL](https://me.candaigo.com) <br>
- [ClawHub skill page](https://clawhub.ai/hangeaiagent/ai-interview-simulator-candaigo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Candaigo API key for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
