## Description:

Use this skill to query Solana blockchain data via the Solscan Pro API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiennv3](https://clawhub.ai/user/tiennv3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to look up Solana accounts, tokens, NFTs, transactions, blocks, markets, programs, and API usage through Solscan Pro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Solana lookup targets and investigation filters may reveal sensitive activity metadata to Solscan Pro.

Mitigation: Query only addresses, transaction signatures, and filters that are authorized for disclosure to Solscan Pro.

Risk: The Solscan API key is sent with requests to Solscan Pro.

Mitigation: Store SOLSCAN_API_KEY as a secret, limit access to the runtime environment, and rotate the key if exposure is suspected.

Risk: Requests may hang because the CLI does not set an HTTP timeout.

Mitigation: Run commands in a supervised shell or add an external timeout when reliability matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiennv3/skills/exploring-solana-with-solscan)
- [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0)
- [Solscan Pro API FAQs](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLSCAN_API_KEY; CLI responses are JSON returned by Solscan Pro.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
