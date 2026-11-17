## Description:

FairScale Solana helps agents check Solana wallet reputation, assess transaction risk, apply custom scoring rules, and evaluate wallet lists through the FairScale API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[risheea](https://clawhub.ai/user/risheea)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to evaluate Solana wallet trustworthiness before trades, swaps, airdrops, whitelist decisions, or agent-to-agent transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, transaction amounts, custom rules, and wallet lists may be sent to FairScale.

Mitigation: Use the skill only when sharing that data with FairScale is acceptable for the user, organization, and transaction context.

Risk: x402 payments or paid API usage can create spend exposure if an agent acts automatically.

Mitigation: Require explicit confirmation or configured spend limits before enabling automatic wallet payments or high-volume requests.

Risk: Passing a real API key as a command-line argument can expose the secret through shell history or process listings.

Mitigation: Store API keys in protected environment variables or a secret manager instead of passing them directly to helper scripts.

## Reference(s):

- [FairScale API Reference](references/API.md)
- [FairScale Docs](https://docs.fairscale.xyz)
- [FairScale API Docs](https://api2.fairscale.xyz/docs)
- [FairScale Skill Page](https://clawhub.ai/risheea/skills/fairscale-solana)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with API examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference FairScale wallet scores, tiers, risk levels, recommendations, and API rate limits.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
