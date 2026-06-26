## Description: <br>
Rapid development with Cloudflare Workers to build and deploy serverless applications on Cloudflare's global network for APIs, full-stack web apps, edge functions, background jobs, and real-time applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, observe, and deploy Cloudflare Workers applications with Wrangler, bindings, storage, queues, Workers AI, and related Cloudflare platform features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable deployment, rollback, delete, and remote-binding examples can affect live Cloudflare resources if run without review. <br>
Mitigation: Require explicit approval before deploy, delete, rollback, or remote production binding actions; prefer staging environments, dry runs, and least-privilege Cloudflare tokens. <br>
Risk: Credential and logging examples can expose Cloudflare tokens, platform secrets, authorization headers, cookies, query strings, raw email contents, stack traces, or telemetry. <br>
Mitigation: Store secrets in Wrangler or another secret manager, use scoped tokens, and redact sensitive headers, cookies, query strings, raw message contents, platform secrets, and stack traces before logging or exporting telemetry. <br>
Risk: External log sink examples can send operational data to third-party observability services. <br>
Mitigation: Review log sink destinations and data retention, limit exported fields, and verify Datadog, Honeycomb, and other observability tokens are scoped for the intended environment. <br>


## Reference(s): <br>
- [Skill Homepage](https://github.com/tenequm/skills/tree/main/skills/cloudflare-workers) <br>
- [Complete Bindings Guide](references/bindings-complete-guide.md) <br>
- [Wrangler and Deployment Guide](references/wrangler-and-deployment.md) <br>
- [Development Best Practices](references/development-patterns.md) <br>
- [Advanced Features](references/advanced-features.md) <br>
- [Observability](references/observability.md) <br>
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/) <br>
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler/) <br>
- [Cloudflare Workers Runtime APIs](https://developers.cloudflare.com/workers/runtime-apis/) <br>
- [Cloudflare Workers Examples](https://developers.cloudflare.com/workers/examples/) <br>
- [Cloudflare Workflows Documentation](https://developers.cloudflare.com/workflows/) <br>
- [Cloudflare Containers Documentation](https://developers.cloudflare.com/containers/) <br>
- [Cloudflare Workers Quickstarts](https://developers.cloudflare.com/workers/get-started/quickstarts/) <br>
- [Cloudflare Workers Framework Guides](https://developers.cloudflare.com/workers/framework-guides/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, TOML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
