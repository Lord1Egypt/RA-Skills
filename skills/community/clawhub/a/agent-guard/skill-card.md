## Description:

Agent Guard helps agents configure and run hard stops, trailing stops, portfolio stop rules, and heartbeat checks for Polymarket and optional Hyperliquid position protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to add exit-policy guidance, setup commands, watcher startup commands, and heartbeat checks around ClawHub Polymarket workflows. It is intended for funded trading environments where protective exits should be configured and reviewed outside the language model before live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead operators toward a long-lived external package with wallet-selling authority.

Mitigation: Use a dedicated least-privilege exit key, verify the npm artifact and launcher path, and review the exact policy before enabling live exits.

Risk: Dry-run protection can transition to live exits when an exit private key is provided.

Mitigation: Start in dry-run, require explicit human confirmation before live arming, and avoid broad agent auto-routing to live exits.

Risk: Private keys may be exposed through shell history, environment files, or compose configuration.

Mitigation: Avoid placing private keys directly in shell history or committed compose files; use secret handling appropriate for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/agent-guard)
- [Publisher profile](https://clawhub.ai/user/polyparlay)
- [NautilusTrader Polymarket documentation](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent or operator to run a long-lived watcher and MCP process after local review.]

## Skill Version(s):

1.0.25 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
