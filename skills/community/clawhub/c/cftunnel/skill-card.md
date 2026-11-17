## Description:

Expose local services to the internet via Cloudflare Tunnels. CLI (npx cftunnel) and Node.js library for creating tunnels, configuring ingress routes, managing DNS records, and running cloudflared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pirumpi](https://clawhub.ai/user/pirumpi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to expose a local web app, API, TCP service, SSH endpoint, or Unix socket at a public HTTPS hostname through Cloudflare Tunnel routes and DNS records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent authority to create, modify, and delete Cloudflare tunnel, DNS, and route resources.

Mitigation: Use a narrowly scoped Cloudflare API token, limit accessible zones and accounts, and review destructive commands before execution.

Risk: Tunnel routes can expose local services, including SSH, databases, TCP services, and Unix sockets, to public hostnames.

Mitigation: Expose only intended services and protect sensitive endpoints with Cloudflare Access or equivalent authentication and network controls.

Risk: The npm package and cloudflared connector become part of the trust boundary for public ingress.

Mitigation: Pin and review the cftunnel package version before use and keep cloudflared installation provenance under change control.

Risk: Using --install-service can make the connector persist across reboots.

Mitigation: Use --install-service only when persistent operation is intentional and removal steps are documented.

## Reference(s):

- [cftunnel GitHub homepage](https://github.com/kyndlo/cftunnel)
- [ClawHub cftunnel skill page](https://clawhub.ai/pirumpi/skills/cftunnel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands produce JSON on stdout and progress or errors on stderr.]

## Skill Version(s):

1.1.0 (source: release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
