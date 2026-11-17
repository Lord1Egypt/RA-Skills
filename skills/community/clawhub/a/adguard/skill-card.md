## Description:

Control AdGuard Home DNS filtering via HTTP API. Use when managing blocklists/allowlists, checking domain filtering status, toggling protection, or clearing DNS cache. Supports blocking/allowing domains, viewing statistics, and protecting/disabling DNS filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rowbotik](https://clawhub.ai/user/rowbotik)

### License/Terms of Use:

MIT

## Use Case:

Developers and administrators use this skill to manage an AdGuard Home DNS filtering instance from an agent-assisted command-line workflow. It supports checking domain filtering status, changing allowlist or blocklist rules, viewing statistics, toggling protection, and clearing DNS cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator access could expose sensitive DNS or admin data if used over an unprotected channel.

Mitigation: Use the skill only against an AdGuard instance you administer and prefer HTTPS or a protected local-only channel.

Risk: Storing the AdGuard admin password in shell startup files could expose credentials.

Mitigation: Do not store the admin password in shell startup files; provide it through a safer secret-handling workflow.

Risk: Protection toggles and rule changes can immediately affect DNS filtering for all clients using the server.

Mitigation: Review requested DNS filtering changes before execution and confirm the target AdGuard instance.

Risk: The allow/block implementation may overwrite existing custom rules.

Mitigation: Fix or carefully test allow/block behavior before relying on it in an active AdGuard deployment.

## Reference(s):

- [AdGuard Home API Reference](references/api.md)
- [Official AdGuard Home API Documentation](https://github.com/AdguardTeam/AdGuardHome/wiki/API)
- [ClawHub skill page](https://clawhub.ai/rowbotik/skills/adguard)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command output summaries, DNS filtering status, rule-change instructions, and troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
