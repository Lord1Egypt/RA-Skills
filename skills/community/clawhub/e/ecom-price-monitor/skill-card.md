## Description:

Monitors cross-border ecommerce product prices, issues price-change alerts, analyzes trends, and supports pricing decisions.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[guaguaren](https://clawhub.ai/user/guaguaren)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators and developers use this skill to prototype competitor price monitoring, alert rules, trend analysis, arbitrage checks, and JSON export workflows across marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current implementation is unfinished and uses mock data, so live scraping and notification behavior may not be reliable for real operations.

Mitigation: Treat it as a demo until live scraping and notification code is completed, reviewed, and tested in a controlled environment.

Risk: Marketplace API keys, cookies, passwords, and webhook URLs may be needed for real use.

Mitigation: Keep credentials out of tracked files and provide them only through a controlled runtime environment or secret store.

Risk: Unpinned or unaudited dependencies and broad export paths can increase operational risk.

Mitigation: Pin and audit dependencies before deployment, and restrict exports to a dedicated directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaguaren/skills/ecom-price-monitor)
- [Artifact skill overview](artifact/ecom-price-monitor/SKILL.md)
- [Artifact documentation](artifact/ecom-price-monitor/docs/README.md)
- [Artifact configuration](artifact/ecom-price-monitor/config/settings.yaml)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Console text, Python examples, YAML configuration, and JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mock price data in the current implementation and can export monitored products and alerts to local JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
