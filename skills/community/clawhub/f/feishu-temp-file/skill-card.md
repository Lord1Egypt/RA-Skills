## Description:

Feishu File Sender helps OpenClaw users stage local files in a temporary allowed directory so they can send files through Feishu when path allowlist checks would otherwise block access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingyangdao](https://clawhub.ai/user/yingyangdao)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to configure file access permissions, copy Feishu-bound files into an allowed temporary media directory, inspect staged files, and clean them up after sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad OpenClaw filesystem permissions, including presets that allow access beyond the temporary media directory.

Mitigation: Use the narrowest allowlist that supports the workflow, avoid medium and loose presets unless explicitly required, and review the resulting OpenClaw configuration before use.

Risk: The cleanup command can delete arbitrary writable files when it is given a specific path.

Mitigation: Run cleanup only on temporary files created by this skill, verify any explicit path before deletion, and prefer cleaning the managed temporary directory when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yingyangdao/skills/feishu-temp-file)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Feishu developer documentation](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance and JSON command output with local file paths and file:// URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces temporary staged file paths and status messages; cleanup is a separate command.]

## Skill Version(s):

1.2.0 (source: server release evidence, artifact _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
