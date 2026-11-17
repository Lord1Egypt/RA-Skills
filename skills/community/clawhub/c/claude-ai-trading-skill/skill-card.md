## Description:

Helps agents use the Elfa API to query crypto social intelligence, retrieve market sentiment and trending-token data, and generate integration examples for API-key or x402 access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nero-sensei](https://clawhub.ai/user/nero-sensei)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading analysts use this skill to request crypto social intelligence from Elfa, including trending tokens, mentions, narratives, smart-account stats, token news, and market-analysis chat. Developers can also use it to generate curl, Python, and JavaScript/TypeScript examples for Elfa API integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: x402 examples can spend real USDC without a clear per-call consent gate.

Mitigation: Prefer API-key mode through ELFA_API_KEY; when using x402, confirm the expected cost first and use an explicit spend limit or a low-balance wallet.

Risk: Credential exposure could occur if users paste API keys, wallet private keys, or seed phrases into chat or code.

Mitigation: Load credentials from environment variables, mask API keys in examples, and never request or store wallet private keys or seed phrases.

Risk: Network access beyond the intended API surface can increase data exposure.

Mitigation: Allow network access only to api.elfa.ai unless a reviewer approves additional domains.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nero-sensei/skills/claude-ai-trading-skill)
- [Elfa API](https://api.elfa.ai)
- [Elfa API Access](https://go.elfa.ai/claude-skills)
- [Elfa x402 Payments Documentation](https://docs.elfa.ai/x402-payments)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON summaries, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live API response summaries, curl commands, and JavaScript/TypeScript or Python snippets.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
