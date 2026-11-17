## Description:

Helps agents recommend, configure, test, and troubleshoot a unified OpenAI-compatible gateway for domestic Chinese AI API providers such as MiMo, DeepSeek, Qwen, and GLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to compare domestic Chinese AI API providers, get API-key and provider setup guidance, and produce OpenAI-compatible examples or gateway configuration for model routing and fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the bundled gateway on a reachable network can expose provider API access to anyone who can reach it.

Mitigation: Bind the service to localhost or a protected interface, add authentication, and apply rate limits before exposing it beyond a trusted environment.

Risk: Provider API keys can leak if stored directly in committed YAML or shared configuration files.

Mitigation: Store provider keys in environment variables or a secret manager and keep shared configuration files limited to placeholders.

Risk: Fallback routing can send prompts or source code to an unintended third-party provider.

Mitigation: Disable or constrain fallback for confidential workloads and approve each configured provider before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/china-api-gateway)
- [中国AI API统一网关 - 详细内容](references/details.md)
- [中国AI平台注册与API获取指南](references/platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Python, curl, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider comparisons, API examples, gateway configuration, health-check guidance, and troubleshooting steps.]

## Skill Version(s):

1.4.3 (source: server release metadata; artifact frontmatter version is 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
