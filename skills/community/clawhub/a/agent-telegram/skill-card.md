## Description: <br>
Defines how agents send Telegram status messages, including account IDs, message format, reporting moments, and common delivery errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangchuanqiytu-ui](https://clawhub.ai/user/shangchuanqiytu-ui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent operators and developers use this skill to standardize Telegram work updates from multiple agent roles to an intended chat. It covers which account ID each role should use, when to report, and what message templates to follow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to send work updates and file paths to one fixed Telegram user ID. <br>
Mitigation: Install only when that Telegram ID is the intended destination; otherwise change the target to an approved chat before use. <br>
Risk: Status messages may include secrets, private project details, or local file paths. <br>
Mitigation: Avoid sending sensitive information and require confirmation before messages include private details or file paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shangchuanqiytu-ui/agent-telegram) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Code] <br>
**Output Format:** [Markdown with JavaScript message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed Telegram target ID and role-specific account IDs documented in the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
