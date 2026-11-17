## Description:

Scans Base-chain token, holder, smart-money, and narrative signals to help identify high-conviction memecoin and mainstream asset alert candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a4205586](https://clawhub.ai/user/a4205586)

### License/Terms of Use:


## Use Case:

Developers and crypto analysts use this skill to run Base-chain market scans, inspect token holder concentration, review narrative platforms, and generate concise alert candidates for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token addresses and search terms may be sent to external crypto data APIs and related web pages.

Mitigation: Use the skill only when those queries are acceptable to share with DexScreener, Basescan, GMGN, Clanker, Bankr, Virtuals, and related services.

Risk: A Basescan API key may be exposed if entered directly in shared shells, logs, or CI output.

Mitigation: Use a dedicated low-privilege Basescan key and avoid placing it in shell history or shared logs.

Risk: Generated alerts can be mistaken for trading advice.

Mitigation: Treat scanner output as market research and require human review before any trading decision.

Risk: Some data sources may be rate limited, unavailable, or require browser-like sessions.

Mitigation: Confirm important signals manually when APIs fail or return incomplete data.

## Reference(s):

- [Alert Rules & Filtering Logic](references/alert-rules.md)
- [Base Alpha Scanner API & Endpoint Reference](references/api-endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/a4205586/skills/base-alpha-scanner)
- [DexScreener API](https://api.dexscreener.com)
- [Basescan API](https://api.basescan.org/api)
- [GMGN API](https://gmgn.ai/defi/quotation/v1)
- [VIRTUAL Protocol API](https://api.virtuals.io/api/virtuals)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and terminal text output with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market-scan summaries, token links, conviction scores, and alert candidates for human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
