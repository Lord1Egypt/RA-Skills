## Description:

Provides a local A-share paper-trading and backtesting workflow for agents to manage simulated accounts, paper orders, positions, fills, account snapshots, and A-share rule checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouldnotappearcalm](https://clawhub.ai/user/shouldnotappearcalm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate local simulated A-share trading accounts, place and cancel paper orders, inspect cash, positions, orders, and trades, validate A-share trading rules, and run simple backtests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a persistent local paper-trading service and optional macOS launchd startup item.

Mitigation: Keep the service bound to 127.0.0.1, avoid exposing the port to a network, and use the documented stop or uninstall-launchd commands when background operation is no longer needed.

Risk: Simulated account state is stored in a local SQLite database under the user data directory by default.

Mitigation: Use the documented db-path or runtime home controls to choose an appropriate local storage location and avoid sharing the database unintentionally.

Risk: Paper trades and backtests depend on market-data freshness and external quote/history sources.

Mitigation: Treat outputs as simulation results, review account and order state before actions, and confirm market-data freshness before relying on fills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shouldnotappearcalm/skills/a-share-paper-trading)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON responses, text]

**Output Format:** [Markdown guidance with shell commands and JSON service or CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates a local HTTP service on 127.0.0.1:18765 by default and stores paper-trading state in a user-level SQLite database.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
