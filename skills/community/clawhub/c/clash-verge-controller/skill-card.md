## Description:

Guides an agent through Clash Verge external controller setup and mihomo REST API operations, including proxy switching, connection monitoring, rule management, configuration changes, delay testing, and kernel restart examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyaoshi](https://clawhub.ai/user/gyaoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and administer a Clash Verge or mihomo controller through REST API calls. It helps agents provide setup guidance, API examples, sample client code, and operational commands for local or remote proxy management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact proxy administration, including restart, configuration changes, cache flushing, rule changes, upgrades, and closing connections.

Mitigation: Require explicit user confirmation before performing disruptive controller actions.

Risk: Controller exposure or unsafe network defaults can disclose or alter proxy administration state.

Mitigation: Keep the controller bound to 127.0.0.1 where possible, avoid wildcard CORS, and restrict remote access with firewall controls.

Risk: API secrets can be mishandled when included in commands or plaintext requests.

Mitigation: Avoid passing secrets on the command line and use HTTPS for sensitive remote controller access.

## Reference(s):

- [Clash Verge / mihomo API Reference](references/api_reference.md)
- [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)
- [mihomo API Documentation](https://wiki.metacubex.one/api/)
- [ClawHub Skill Page](https://clawhub.ai/gyaoshi/skills/clash-verge-controller)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with YAML, bash, Python, and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST API endpoints, Authorization header examples, and local controller configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
