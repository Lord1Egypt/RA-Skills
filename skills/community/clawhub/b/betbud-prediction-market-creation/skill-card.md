## Description:

Automatically creates prediction markets on betbud.live by analyzing trending crypto Twitter topics with Claude AI and fetching professional images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samj12](https://clawhub.ai/user/samj12)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this agent to monitor crypto-related social media, propose debatable time-bound market questions, create Base Sepolia prediction markets, and register them with betbud.live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended operation can spend wallet funds and publish blockchain or platform records based on LLM-generated proposals.

Mitigation: Use a dedicated low-balance test wallet, require manual approval before each transaction and registration, and enforce spend and rate limits.

Risk: Generated market questions, resolution criteria, categories, or sources may be malformed, misleading, duplicative, or hard to resolve.

Mitigation: Validate LLM output against a strict schema and review each question, source list, category, and resolution rule before publication.

Risk: The agent requires sensitive API credentials and a wallet private key.

Mitigation: Store secrets only in environment variables, never reuse a primary wallet key, rotate exposed credentials, and limit wallet permissions and balance.

Risk: Scheduled execution can amplify bad proposals or transaction failures.

Mitigation: Avoid cron or 24/7 operation until a dry-run mode, review workflow, and failure monitoring are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samj12/skills/betbud-prediction-market-creation)
- [betbud.live](https://betbud.live)
- [TwitterAPI.io](https://twitterapi.io)
- [Anthropic Console](https://console.anthropic.com)
- [Unsplash Developers](https://unsplash.com/developers)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, API calls, blockchain transactions, files]

**Output Format:** [Terminal text, JSON API payloads, blockchain transaction hashes, and a local JSON cache file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API keys, an RPC URL, and a dedicated Ethereum wallet private key supplied through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
