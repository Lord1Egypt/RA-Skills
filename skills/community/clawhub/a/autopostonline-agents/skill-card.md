## Description: <br>
Enables autonomous AI agents to draft, schedule, publish, and analyze social media content through AutoPostOnline's unified publishing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autopostonline](https://clawhub.ai/user/autopostonline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and automation operators use this skill to let agents operate connected social channels through AutoPostOnline for drafts, scheduling, publishing, media uploads, analytics, and recurring campaigns within owner-approved rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can operate connected social channels and publish externally visible content. <br>
Mitigation: Start in safe mode or with low-risk accounts, confirm target integrations before posting, and require owner approval until campaign boundaries are clear. <br>
Risk: The skill requires an AutoPostOnline API key and connected account permissions. <br>
Mitigation: Store the API key in a secret manager or protected environment variable, avoid logging credentials, and rotate the key if exposure is suspected. <br>
Risk: Autonomous mode can post at scale outside the owner's intent if scope is vague. <br>
Mitigation: Define allowed channels, topics, posting frequency, approval boundaries, and an emergency stop process before enabling autonomous publishing. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/autopostonline/autopostonline-agents) <br>
- [AutoPostOnline agent page](https://autopostonline.com/agents/) <br>
- [AutoPostOnline agent documentation](https://autopostonline.com/docs/agents/) <br>
- [AutoPostOnline API endpoint](https://app.autopostonline.com/api) <br>
- [AutoPostOnline MCP endpoint](https://app.autopostonline.com/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with environment variables, API examples, and operating-mode instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Docs-only skill; requires an AutoPostOnline API key and owner-connected social channels.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
