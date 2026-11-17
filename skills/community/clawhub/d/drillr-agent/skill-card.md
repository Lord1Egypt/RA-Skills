## Description:

Drillr gives agents access to financial research, market signals, published analyst articles, and per-user watchlists through MCP, REST, and CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-grebe](https://clawhub.ai/user/little-grebe)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to onboard a Drillr API key and research equities, filings, earnings, market signals, articles, and watchlists. It is intended for agent-assisted financial research workflows that can call Drillr through MCP, REST, or a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask users to paste a live Drillr API key into chat during onboarding.

Mitigation: Prefer local secret storage or environment injection, avoid ordinary chat for live keys, mask any confirmation, and revoke any key that was exposed in chat.

Risk: The skill stores long-lived credentials for later Drillr access.

Mitigation: Store the key only in the documented local config with restrictive permissions or an equivalent secret store, and rotate or revoke the key when access is no longer needed.

Risk: The CLI setup path installs a global npm package.

Mitigation: Pin and verify the intended drillr-cli package version before installation instead of installing the latest global package blindly.

Risk: The skill depends on Drillr as an external finance-data service.

Mitigation: Use it only when the user accepts sending requests to Drillr, and treat returned financial research as decision support rather than investment advice.

## Reference(s):

- [Drillr](https://drillr.ai)
- [Drillr Developer Portal](https://drillr.ai/developer)
- [Drillr API Reference](https://drillr.ai/developer/docs)
- [Drillr API Keys](https://drillr.ai/developer/keys)
- [ClawHub Skill Listing](https://clawhub.ai/little-grebe/skills/drillr-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API call guidance and configuration snippets for MCP, REST, and CLI access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
