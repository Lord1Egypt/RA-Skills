## Description:

Uploads local files to Feishu (Lark) cloud storage and optionally sends them to a specified chat using Node.js or Bash scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deewooo](https://clawhub.ai/user/deewooo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to upload local files up to 30 MB to Feishu and share them into chats from an agent workflow. It is intended for environments with a configured Feishu app, appropriate message/file permissions, Node.js 18+, and network access to Feishu APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports bundled credentials, token disclosure, and insecure token storage.

Mitigation: Use only a Feishu app you control, rotate any bundled secret before use, remove token logging, and store credentials in a proper secret store.

Risk: The security evidence reports network side effects during installation, including token retrieval or upload checks.

Mitigation: Disable installation-time token retrieval and upload tests unless the user explicitly opts in.

Risk: The skill can upload local files and send them to Feishu chats.

Mitigation: Review the selected file path, destination chat ID, and Feishu app permissions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deewooo/skills/feishu-upload-skill)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message API](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output from upload scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads may create token and upload-result files in the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
