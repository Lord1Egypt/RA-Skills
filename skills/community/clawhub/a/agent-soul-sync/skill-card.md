## Description:

Sync local OpenClaw skills to a remote NanoClaw agent on Mysta by listing agents and uploading selected local SKILL.md file contents through the Mysta MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongyegong](https://clawhub.ai/user/hongyegong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make local OpenClaw skills available on a Mysta-hosted NanoClaw agent. It helps them authenticate, choose a target agent, select local skills, and upload those skills for remote use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable Mysta MCP server URL can receive the user's Mysta API key and selected skill files.

Mitigation: Keep MYSTA_MCP_URL unset unless intentionally using a trusted Mysta environment, and use a limited API key that can be revoked.

Risk: Uploaded SKILL.md files may contain secrets, private prompts, or other sensitive content and synced skills persist remotely.

Mitigation: Review selected skill files before syncing and confirm that the remote copy should persist before upload.

Risk: Uploading a skill with the same name overwrites the remote copy.

Mitigation: Confirm the selected agent and skill names before syncing, especially when using batch upload.

## Reference(s):

- [Agent Soul Sync on ClawHub](https://clawhub.ai/hongyegong/skills/agent-soul-sync)
- [Mysta application](https://app.staging.mysta.tech)
- [Mysta API keys](https://app.staging.mysta.tech/en/profile#api-keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, MYSTA_API_KEY, and user consent before browser opening, API connection, or uploads.]

## Skill Version(s):

0.3.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
