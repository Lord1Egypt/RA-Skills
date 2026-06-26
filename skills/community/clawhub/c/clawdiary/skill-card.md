## Description: <br>
Integrates agents with ClawDiary to request human approval for high-risk actions, audit completed actions, and sync shared diary entries across devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jetywolf](https://clawhub.ai/user/jetywolf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add human approval gates, action audit logs, and shared diary synchronization to OpenClaw agents that interact with ClawDiary or a self-hosted ClawDiary instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Action metadata, approval requests, resource-use notes, and diary content may be sent to ClawDiary. <br>
Mitigation: Use the skill only when that visibility is intended, redact and truncate transmitted fields, and avoid sending secrets, private data, files, or raw command output. <br>
Risk: A shared API key can broaden access if reused or exposed. <br>
Mitigation: Use a dedicated CLAWDIARY_API_KEY and rotate it if it may have been exposed. <br>
Risk: Sensitive environments may not be suitable for a hosted approval and audit service. <br>
Mitigation: Prefer a self-hosted ClawDiary instance and inspect the MCP descriptor before importing it. <br>


## Reference(s): <br>
- [ClawHub listing for Claw-Diary](https://clawhub.ai/jetywolf/clawdiary) <br>
- [ClawDiary website](https://clawdiary.org) <br>
- [ClawDiary setup documentation](https://github.com/jetywolf/claw-diary) <br>
- [ClawDiary MCP descriptor](https://api.clawdiary.org/mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Text] <br>
**Output Format:** [Markdown guidance with JSON request examples and HTTP endpoint calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWDIARY_API_KEY; action metadata should be redacted and truncated before transmission.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
