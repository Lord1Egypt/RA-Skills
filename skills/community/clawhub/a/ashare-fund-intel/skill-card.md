## Description:

Produce scheduled A-share and fund intelligence reports with bullish and bearish signals, source-backed analysis, and position-adjustment suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warriorfan](https://clawhub.ai/user/warriorfan)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to generate timed China A-share and fund briefings, NAV or earnings confirmation reports, and source-backed portfolio adjustment suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a populated plaintext portfolio snapshot with specific holdings and amounts.

Mitigation: Remove or replace references/portfolio-current.md with an empty or synthetic template before sharing, and provide real holdings only during a controlled session or in storage the user explicitly controls.

Risk: The skill produces financial market and position-adjustment guidance that can be wrong or become stale.

Mitigation: Require current source links for major claims, separate facts from opinions, and keep the non-investment-advice disclaimer in every report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warriorfan/skills/ashare-fund-intel)
- [A-share and fund monitoring sources](references/sources.md)
- [Three-period report template](references/report-template.md)
- [Watchlist template](references/watchlist-template.md)
- [China Securities Regulatory Commission](https://www.csrc.gov.cn/)
- [People's Bank of China](https://www.pbc.gov.cn/)
- [Shanghai Stock Exchange](https://www.sse.com.cn/)
- [Shenzhen Stock Exchange](https://www.szse.cn/)
- [CNINFO disclosures](http://www.cninfo.com.cn/)
- [Eastmoney funds](https://fund.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with cited source links, bullish and bearish factors, risk highlights, and per-fund action tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes explicit allocation ranges and ends with a non-investment-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
