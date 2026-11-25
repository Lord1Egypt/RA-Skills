## Description:

通义千问旗舰推理模型（2.4 万亿参数 MoE），擅长复杂推理、代码工程与长上下文分析。支持文本与图片输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to send text prompts and optional images to dLazy's hosted Qwen service and receive generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between the Qwen model description and the CLI authentication or invocation steps; the CLI package and some referenced material were not fully reviewed.

Mitigation: Check the CLI's authentication and invocation instructions and review the package behavior before use.

Risk: The skill sends prompts to dLazy's hosted API and describes uploading local media to its storage service; the security guidance says service handling of prompts and media was not fully reviewed.

Mitigation: Review dLazy's service terms and data handling, and avoid sending sensitive prompts or media unless that use is appropriate.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [CLI repository linked in skill metadata (provenance unavailable)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON response envelope containing generated content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated response content; asynchronous requests may initially return a task identifier.]

## Skill Version(s):

1.2.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
