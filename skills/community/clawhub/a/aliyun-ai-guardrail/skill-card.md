## Description:

Installs and configures an OpenClaw hook that uses Alibaba Cloud AI Guardrail to inspect LLM request content and replace messages that trigger malicious-content rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliyun-ai-sec](https://clawhub.ai/user/aliyun-ai-sec)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to install an OpenClaw security hook that checks agent LLM request content with Alibaba Cloud AI Guardrail. It is intended for environments where agent messages may be sent to Alibaba Cloud for guardrail evaluation and blocked messages may be rewritten.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook is persistent and always enabled for OpenClaw agent sessions, so agent LLM-like request content may be sent to Alibaba Cloud and rewritten.

Mitigation: Install only in environments where this data flow is acceptable, review the hook before deployment, and document the guardrail behavior for users.

Risk: The skill asks for Alibaba Cloud AccessKey credentials and writes them into OpenClaw environment configuration.

Mitigation: Use a dedicated least-privilege Alibaba Cloud RAM credential, avoid committing openclaw.json, and restrict file permissions on configuration files.

Risk: The security scan reports insufficient scoping and safety guidance for the installed hook.

Mitigation: Prefer or require a version with endpoint allowlisting, bounded caching, sanitized logs, pinned dependencies, and a clear disable or uninstall path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aliyun-ai-sec/skills/aliyun-ai-guardrail)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [OpenClaw hook definition](artifact/assets/aliyun-ai-guardrail/hooks/aliyun-ai-guardrail/HOOK.md)
- [Hook handler](artifact/assets/aliyun-ai-guardrail/hooks/aliyun-ai-guardrail/handler.ts)
- [Hook package manifest](artifact/assets/aliyun-ai-guardrail/package.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation steps, credential configuration guidance, and restart instructions for OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
