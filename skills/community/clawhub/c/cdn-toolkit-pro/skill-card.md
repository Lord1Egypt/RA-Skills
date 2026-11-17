## Description:

企业级CDN管理平台，支持多CDN智能调度、边缘计算、高级WAF与DDoS防护、实时监控及缓存管理，适合高并发与全球分发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and generate CDN configuration guidance, shell commands, code examples, and JSON reports for multi-CDN routing, edge workers, WAF/DDoS protection, monitoring, cache warmup, and cache purge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live CDN and security configuration changes that may affect production traffic.

Mitigation: Use least-privilege API tokens, test on non-production zones first, and require explicit approval before creating, patching, purging, or changing CDN or security settings.

Risk: API tokens or account secrets may be exposed if pasted directly into generated scripts or logs.

Mitigation: Store credentials in environment variables or secret managers, avoid hardcoding tokens, and review outputs for secrets before sharing.

Risk: Generated commands or code examples may be incomplete or unsuitable for a specific CDN account.

Mitigation: Review commands against provider documentation, scope them to approved domains and zones, and validate expected effects before execution.

## Reference(s):

- [详细参考 - cdn-toolkit-pro](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cdn-toolkit-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, JSON]

**Output Format:** [Markdown with inline code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CDN API command examples, configuration recommendations, execution logs, and structured status fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
