## Description:

Use Futu Trade Bot Skills to run account, quote, and trade workflows with real HK market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and agent builders use this skill to connect an agent to Futu OpenD for HK market quotes, account lookup, simulated trading, confirmed live order workflows, and user-approved trading strategy scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real-money trades through a local Futu OpenD session.

Mitigation: Keep REAL trading disabled unless the user confirms the exact order parameters; prefer SIMULATE and require explicit confirmation for live orders, trade unlocks, order changes, and cancellations.

Risk: Reusable trading credentials may be stored in json/config.json.

Mitigation: Treat json/config.json as a secret, prefer trade_password_md5, use restrictive file permissions, and avoid committing real credentials.

Risk: The skill requires local network access to Futu OpenD and may need broader host access in restricted sandboxes.

Mitigation: Avoid host or elevated mode unless necessary; explain the access need to the user before rerunning with broader permissions.

Risk: User-approved background strategies can place repeated orders if configured incorrectly.

Mitigation: Review generated strategy scripts before starting them, use fixed parameters, prefer simulated accounts, and record PID and log paths for monitoring and shutdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersonling1217-png/skills/futu-trading-bot)
- [Publisher profile](https://clawhub.ai/user/jeffersonling1217-png)
- [README](README.md)
- [Account Manager docs](docs/account.md)
- [Config Manager docs](docs/config.md)
- [Quote Service docs](docs/quote.md)
- [Strategy Helpers docs](docs/strategy.md)
- [Trade Service docs](docs/trade.md)
- [Configuration example](json/config_example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or run user-approved strategy scripts and local configuration files when the user explicitly requests them.]

## Skill Version(s):

1.0.9 (source: release evidence, _meta.json, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
