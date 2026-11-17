## Description:

Aliyun Use connects an agent to Alibaba Cloud Bailian LLMs for chat, code-oriented generation, model listing, and language translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnlangzi](https://clawhub.ai/user/cnlangzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call Aliyun Bailian models from an agent workflow for chat, code-oriented text generation, translation, and model discovery. It requires an ALIYUN_BAILIAN_API_KEY and can route requests through a configured Bailian API host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys, prompts, translation text, and generated context to a configured API host.

Mitigation: Use only trusted HTTPS Alibaba Cloud Bailian endpoints, keep ALIYUN_BAILIAN_API_HOST fixed in trusted environments, and do not allow untrusted workflows to set --base-url or the API host environment variable.

Risk: Prompts or translation inputs may contain secrets, confidential code, or sensitive business data.

Mitigation: Review inputs before use and avoid sending secrets, credentials, confidential code, or regulated data through the skill.

Risk: The server security verdict is suspicious because host configuration can redirect requests.

Mitigation: Review the skill before installing and deploy it only where outbound API destinations and environment variables are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnlangzi/skills/aliyun-use)
- [AliYun Bailian API Reference](artifact/references/API.md)
- [Available models](artifact/assets/models.json)
- [Aliyun Bailian console](https://bailian.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Code, JSON, Shell commands, Configuration]

**Output Format:** [JSON command responses and streamed or returned model text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat requests accept Anthropic-style message arrays, model selection, temperature, max token limits, streaming, and configurable API host settings.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
