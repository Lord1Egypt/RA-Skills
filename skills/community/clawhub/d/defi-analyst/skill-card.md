## Description:

DeFi research and analysis via Tavily MCP, GeckoTerminal API, and DeFiLlama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-wzw](https://clawhub.ai/user/0x-wzw)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi researchers, analysts, and agent developers use this skill to investigate protocols, monitor TVL and yield data, discover token and pool activity, and compare competitive DeFi landscapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README exposes and encourages use of a real-looking Tavily API credential.

Mitigation: Do not use the included key; create a fresh Tavily key and keep secrets out of shell history, shared configs, and committed files.

Risk: Research queries and token or protocol identifiers may be sent to Tavily, DeFiLlama, GeckoTerminal, and potentially Moltbook.

Mitigation: Avoid submitting confidential strategy, wallet, customer, or unreleased token information to these external services.

## Reference(s):

- [Tavily](https://tavily.io)
- [DeFiLlama API](https://api.llama.fi)
- [GeckoTerminal API](https://api.geckoterminal.com/api/v2)
- [ClawHub Skill Page](https://clawhub.ai/0x-wzw/skills/defi-analyst)
- [Publisher Profile](https://clawhub.ai/user/0x-wzw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-shaped examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API queries and summarized DeFi metrics from external services.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
