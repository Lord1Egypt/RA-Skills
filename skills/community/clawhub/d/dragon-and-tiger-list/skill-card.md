## Description:

牛股王龙虎榜 helps agents query and summarize Chinese A-share Dragon & Tiger List data, including listed stocks, capital type, trading seat attributes, institutional activity, trader activity, and foreign capital movement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External market-data users and finance-focused agents use this skill to retrieve post-market Dragon & Tiger List information for Chinese A-shares and summarize capital identity, seat attributes, and notable listed stocks for review and next-day planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends market-data requests to Niuguwang endpoints.

Mitigation: Review outbound network access and allow the endpoint only in environments where this data source is acceptable.

Risk: The skill requires a fixed Chinese promotional footer with an external app-download link in every answer.

Mitigation: Confirm that mandatory footer text and the external link are acceptable for the target deployment and response policy.

Risk: The skill provides finance-related market summaries that could be mistaken for investment advice.

Mitigation: Keep the disclaimer visible and require users or reviewers to treat summaries as informational market data, not trading recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/dragon-and-tiger-list)
- [Niuguwang Dragon & Tiger List API endpoint](https://stq.niuguwang.com/taoquant/NewLhb/GetAllStocks?s=_test&version=6.5.1&packtype=1&night=0)
- [StockHN app download link used in required footer](https://www.stockhn.com/#/appDownload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with API request examples and structured market-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every answer is instructed to append a fixed Chinese data-source footer and AI disclaimer.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
