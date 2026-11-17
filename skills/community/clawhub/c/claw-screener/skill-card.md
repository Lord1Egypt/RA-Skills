## Description:

Stock screener combining Williams %R oversold signals with Warren Buffett-style fundamental analysis. Supports US (S&P 500) and Thai (SET) markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsoutar](https://clawhub.ai/user/rsoutar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to screen US and Thai equities, analyze individual stocks, manage watchlists, and produce stock screening results for review. It is intended to support investment research workflows, not to provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may lead users to run an unverified remote Bun installer.

Mitigation: Install Bun through a trusted package manager or a pinned, verified Bun release before running the skill.

Risk: The skill makes public market-data requests and creates local watchlist and cache files.

Mitigation: Run it in an environment where public financial-data requests are acceptable and review local files before sharing logs or outputs.

Risk: Stock rankings and screening results can be mistaken for investment advice.

Mitigation: Treat outputs as research signals only and independently verify financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsoutar/skills/claw-screener)
- [Publisher profile](https://clawhub.ai/user/rsoutar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, Telegram-formatted Markdown, and Bun shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local watchlist and SQLite cache files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
