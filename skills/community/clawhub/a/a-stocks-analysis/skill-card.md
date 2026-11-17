## Description:

A Stocks Analysis helps agents query and analyze public historical China A-share and Hong Kong stock market data across market data, fundamentals, indices, and text sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn natural-language stock questions into read-only /stocks data queries and structured market analysis for research, with risk caveats and follow-up query suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires TAX_API_KEY for the tax.yyyou.top stock data service.

Mitigation: Confirm the user is comfortable configuring this credential and do not ask the user to paste the key into chat.

Risk: Stock analysis outputs may be mistaken for financial advice.

Mitigation: Treat outputs as research only, include risk caveats, and avoid trade execution, return guarantees, or investment commitments.

Risk: Generic announcement or policy requests can be ambiguous without a specific stock, issuer, exchange, or market context.

Mitigation: Ask a clarifying question before routing ambiguous requests to the stock data workflow.

## Reference(s):

- [A Stocks Analysis on ClawHub](https://clawhub.ai/roamer-remote/skills/a-stocks-analysis)
- [TAX stock data service homepage](https://tax.yyyou.top/)
- [README](artifact/README.MD)
- [Skill Reference](artifact/SKILL_REFERENCE.MD)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with structured analysis sections and inline API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAX_API_KEY for the tax.yyyou.top stock data service; outputs are read-only research analysis and do not place trades.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
