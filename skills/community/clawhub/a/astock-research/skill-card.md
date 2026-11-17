## Description:

Provides a Chinese A-share equity research framework covering fundamentals, capital flows, technical signals, market sentiment, and news to help agents structure stock analysis and trading plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zif10765-maker](https://clawhub.ai/user/zif10765-maker)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide agent-assisted research on Chinese A-share listed companies. It organizes market, company, technical, sentiment, and news inputs into a structured analysis and trading-plan format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an exposed market-data API key in an executable script.

Mitigation: Remove the bundled key, rotate it, and require users to provide their own credential through a secure local secret mechanism.

Risk: The optional quote script sends requested stock codes to an external market-data service.

Mitigation: Disclose the external data transfer before use and avoid submitting confidential watchlists or trading intentions.

Risk: The executable quote script has weak input handling for stock-code arguments.

Mitigation: Validate stock codes against an allowed exchange-code pattern before executing the query.

Risk: Research outputs may be mistaken for personalized financial advice.

Mitigation: Present outputs as research support only and require human review before any investment or trading decision.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis guidance with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a stock-code input when invoking the optional quote script.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
