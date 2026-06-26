## Description: <br>
Syncs user-selected local OpenClaw skills to a remote NanoClaw agent on Mysta over HTTPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongyegong](https://clawhub.ai/user/hongyegong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to select local skills and upload their SKILL.md contents to a Mysta NanoClaw cloud agent so those skills are available remotely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local SKILL.md files may contain private instructions, credentials, or other sensitive content before upload. <br>
Mitigation: Review the selected SKILL.md files before syncing and avoid choosing all when any local skill may contain sensitive data. <br>
Risk: The workflow uses a Mysta API key and sends requests to a remote MCP endpoint. <br>
Mitigation: Use a revocable scoped API key when available, keep it in MYSTA_API_KEY, and verify the MCP URL is a Mysta endpoint before connecting. <br>
Risk: Uploading to the wrong agent can make skills available in an unintended remote environment. <br>
Mitigation: Confirm the target agent with the user before upload and require explicit consent before opening a browser, connecting to Mysta, or uploading files. <br>


## Reference(s): <br>
- [Agent Soul Sync on ClawHub](https://clawhub.ai/hongyegong/agent-soul-sync) <br>
- [Mysta app](https://app.staging.mysta.tech) <br>
- [Mysta API keys](https://app.staging.mysta.tech/en/profile#api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, MYSTA_API_KEY, a selected Mysta agent, and user-selected local SKILL.md files.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
