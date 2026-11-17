## Description:

Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tbeard602](https://clawhub.ai/user/tbeard602)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to choose Cloudflare products and deploy, host, publish, or configure applications and infrastructure on Cloudflare Workers, Pages, and related platform services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Cloudflare infrastructure guidance can change hosted applications, secrets, routes, tunnels, or other public resources.

Mitigation: Use least-privilege Cloudflare tokens and require explicit approval before destructive API calls, secret changes, public port exposure, or persistent tunnel installation.

Risk: Deployment workflows may run project code or depend on local Wrangler behavior.

Mitigation: Pin Wrangler locally, review generated commands and configuration, and approve sandbox code execution before running deployment steps.

## Reference(s):

- [Cloudflare Deploy on ClawHub](https://clawhub.ai/tbeard602/skills/cloudflare-deploy)
- [Cloudflare Deploy Skill Source](SKILL.md)
- [Cloudflare Workers Reference](references/workers/README.md)
- [Cloudflare Pages Reference](references/pages/README.md)
- [Wrangler Authentication Reference](references/wrangler/auth.md)
- [Cloudflare R2 Reference](references/r2/README.md)
- [Cloudflare D1 Reference](references/d1/README.md)
- [Cloudflare AI Gateway Reference](references/ai-gateway/README.md)
- [Terraform for Cloudflare Reference](references/terraform/README.md)
- [Cloudflare API Reference](references/api/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose deployment steps, environment variables, Cloudflare configuration, and verification commands for user review before execution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
