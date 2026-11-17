## Description:

Transfers ownership of Feishu Drive documents, spreadsheets, bitables, mind maps, and files created by an AI bot to a specified user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators and operations users use this skill to transfer Feishu document ownership from AI-created or bot-owned files to a verified human user, either one file at a time or in a reviewed batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk transfer mode can change ownership for many Feishu files under the authenticated lark-cli account.

Mitigation: Use dry-run first, prefer explicit per-file tokens or an exact verified --ai-owner filter, and avoid --all unless every listed file has been checked.

Risk: An incorrect target user ID or member type can transfer ownership to the wrong account.

Mitigation: Verify the target open_id or selected member type before execution and review the file list before running any non-dry-run transfer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freedompixels/skills/feishu-owner-transfer)
- [Publisher Profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls]

**Output Format:** [Markdown with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated lark-cli access and a valid target user ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
