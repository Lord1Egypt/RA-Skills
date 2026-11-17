## Description:

FT AI market-data skill collection for A-share stock lists, real-time quotes, IPO information, block trades, margin trading details, and individual security valuation metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query FT AI A-share market-data endpoints and turn the returned JSON into concise tables or summaries for stock lists, quotes, IPOs, block trades, margin trading, and individual securities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dispatcher can be steered to execute local Python handlers outside the intended bundled sub-skills.

Mitigation: Allow only the named bundled sub-skills before trusting the skill in an agent environment where prompts or model decisions can influence command arguments.

Risk: Full-result pagination can request large market-data result sets.

Mitigation: Prefer bounded page and page_size values for routine use, and reserve all-page collection for cases where the full dataset is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftai-market-data)
- [FT market data API base](https://market.ft.tech)
- [A-share quotes endpoint](https://market.ft.tech/app/api/v2/stocks)
- [FT AI security info endpoint](https://ftai.chat/api/v1/market/security/{symbol}/info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls]

**Output Format:** [JSON from handler scripts, usually summarized as Markdown tables or bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paginated or full-result market data; no credential environment variables were detected in discovery.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
