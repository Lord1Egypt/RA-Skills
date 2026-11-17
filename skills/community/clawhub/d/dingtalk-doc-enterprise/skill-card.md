## Description:

Operates on existing DingTalk documents that the user identifies by URL or docKey and is authorized to access, supporting read, overwrite, insert, modify, and delete-block operations while explicitly refusing document creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shyzhen](https://clawhub.ai/user/shyzhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent read and update existing DingTalk enterprise documents through user-provided document URLs. It is intended for document maintenance workflows where the current DingTalk user already has access to the target document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses DingTalk enterprise app credentials to read and change existing documents.

Mitigation: Install it only for workflows that require DingTalk document access, keep credentials scoped to the intended enterprise app, and do not expose them in prompts or logs.

Risk: Overwrite and delete-block operations can be destructive if the document or block target is wrong.

Mitigation: Confirm the document URL or docKey and inspect block structure before update, delete, or ambiguous block-level changes.

Risk: Configuring a local debug operator identity in production can bypass the expected current-user identity flow.

Mitigation: Use OPENCLAW_SENDER_ID or DINGTALK_SENDER_ID in deployed environments and avoid DINGTALK_OPERATOR_ID outside local debugging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shyzhen/skills/dingtalk-doc-enterprise)
- [DingTalk OpenClaw connector docs](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector?tab=readme-ov-file#%E9%92%89%E9%92%89%E6%96%87%E6%A1%A3docs%E4%B8%8E-mcpdocs)
- [Related DingTalk connector issue](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues/456)
- [Alternative ClawHub skill with write whitelist controls](https://clawhub.ai/shyzhen/dingtalk-doc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus DINGTALK_CLIENTID and DINGTALK_CLIENTSECRET environment variables; operations are constrained to existing DingTalk document URLs or docKeys.]

## Skill Version(s):

1.0.8 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
