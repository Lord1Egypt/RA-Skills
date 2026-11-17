## Description:

Cremonix BTC/ETH Regime Intelligence + Trading Signals provides constraint-filtered BTC/ETH regime classifications and setup status from a production ML ensemble as a delayed free intelligence feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cremonix](https://clawhub.ai/user/cremonix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch a public BTC/ETH market-regime feed, summarize current regime states, and explain whether any setup passed the provider's filters. The skill is informational and should not be used to execute trades or make payment decisions without explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence financial decisions through BTC/ETH regime and setup summaries.

Mitigation: Present outputs as informational market context only, avoid trading instructions or fund-allocation recommendations, and preserve the not-financial-advice framing.

Risk: The skill includes paid subscription, wallet payment, and renewal behavior.

Mitigation: Require explicit user confirmation for each payment or renewal with visible amount, recipient, term, and invoice details; do not grant wallet, payment, billing, or API-key tool access by default.

Risk: The free feed is delayed and may be stale for fast-moving markets.

Mitigation: State the feed timestamp and delay when available, and encourage independent verification before the user makes any trading decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cremonix/skills/cremonix-signals)
- [Cremonix website](https://cremonix.com)
- [Public Cremonix free JSON feed](https://blog.cremonix.com/feeds/cremonix-free.json)
- [Cremonix OpenClaw documentation](https://docs.cremonix.com/openclaw)
- [Cremonix subscription page](https://app.cremonix.com/api-subscribe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with optional shell commands and parsed JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq to fetch and parse a public read-only feed; paid real-time access requires separate explicit payment confirmation.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
