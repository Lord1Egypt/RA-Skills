## Description:

DNS配置工具专业版 helps enterprise operations and infrastructure teams plan DNS configuration, CAA controls, Cloudflare proxy behavior, wildcard certificate workflows, migration rollback, and DNS record validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operations engineers, and infrastructure teams use this skill to generate DNS configuration guidance, shell-command examples, migration checklists, and validation steps for enterprise DNS, certificate, and Cloudflare workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS or certificate changes can affect live services.

Mitigation: Export existing records, verify the target zone, and require explicit operator confirmation before any change is applied.

Risk: Provider credentials or DNS API tokens could grant broad access.

Mitigation: Use least-privilege provider tokens supplied through environment variables and avoid embedding credentials in files or prompts.

Risk: Bulk migrations can omit records or make rollback difficult.

Mitigation: Validate all relevant record types, keep old provider records during the rollback window, and document rollback triggers before switching name servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-config-tool-pro)
- [Let's Encrypt ACME v2 directory](https://acme-v02.api.letsencrypt.org/directory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose production-impacting DNS and certificate changes that require operator review before execution.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
