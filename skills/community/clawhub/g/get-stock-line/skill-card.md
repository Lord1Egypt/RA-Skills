## Description:

Fetches historical K-line data for mainland China A-share stocks and indexes, with adjusted-price support through AKShare and a Sina Finance fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc82465](https://clawhub.ai/user/mc82465)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve A-share stock and index history, inspect current daily change data, and calculate adjusted price changes between dates. It is a market-data helper and should not be treated as financial advice or a guaranteed real-time quote source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance data may be delayed, unavailable, provider-dependent, or unsuitable as investment advice.

Mitigation: Use the output as a market-data helper only, verify important values against authoritative sources, and avoid relying on it for trading decisions.

Risk: The skill makes outbound requests to finance data providers and uses optional third-party Python dependencies.

Mitigation: Install it in an isolated Python environment and pin or review dependencies before deployment.

Risk: When AKShare is unavailable, the Sina Finance fallback returns unadjusted data that can contain ex-dividend gaps.

Mitigation: Prefer AKShare for adjusted historical calculations and disclose when fallback data is used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mc82465/skills/get-stock-line)
- [SKILL.md](artifact/SKILL.md)
- [kline.py](artifact/kline.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python examples and returned dictionary/list data shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on outbound finance data provider availability and may fall back to unadjusted Sina Finance data when AKShare is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
