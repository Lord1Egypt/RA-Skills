## Description:

Use when an agent needs a short crypto market brief or a perp signal: what changed overnight in BTC, ETH, SOL and HYPE with the one level to watch, which Hyperliquid perps moved unusually, whether funding, liquidations or open interest are abnormal right now, or the signal board and coin signals. Calls AgentFeed over HTTP. Scheduled or unattended runs send one flat signals pass (or a prepaid key) from the AGENTFEED_KEY environment variable, so no payment prompt is needed; attended runs can pay per call with x402. Describes what moved, never what to trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekdaseek](https://clawhub.ai/user/seekdaseek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve concise crypto market briefs and Hyperliquid perpetual-futures signals, then summarize what changed and which market levels or conditions are notable. Its output describes market data and is not a trade instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary marks the release suspicious because it flags an unpinned installation command and behavior outside the stated market-brief purpose; the scan covered only part of the artifact.

Mitigation: Review the full package and installation target before use, and wait until package and repository versions are pinned and reviewed.

## Reference(s):

- [AgentFeed service](https://x402.ochinimus.app)
- [Route and pricing reference](references/ROUTES.md)
- [Scheduling reference](references/SCHEDULING.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Market analysis]

**Output Format:** [JSON market data summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefs and signal responses include source timestamps and may identify stale or missing inputs; output is descriptive, not a trade recommendation.]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
