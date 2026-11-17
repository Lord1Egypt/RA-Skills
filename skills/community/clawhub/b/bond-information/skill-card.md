## Description:

BondInformation helps agents query FEEDAX bond-market news and credit-risk signals by keyword, bond type, sentiment, time range, and sorting preference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance analysts use this skill to monitor bond news, issuer sentiment, default risk, rating changes, and market developments from FEEDAX data. It is suited for research workflows that need brief chat summaries plus full exported result files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends bond-search terms and a FEEDAX API key to the FEEDAX service.

Mitigation: Use protected environment-variable injection or a controlled configuration file, avoid pasting API keys into chat, and install only when FEEDAX data sharing is acceptable.

Risk: The release evidence flags API-key handling as risky because production credentials may be exposed through URL-based HTTP requests.

Mitigation: Avoid production credentials unless the endpoint is changed to HTTPS and API keys are removed from URLs.

Risk: Default CSV and Markdown exports may persist sensitive bond research or query results locally.

Mitigation: Use --no-output for sensitive lookups or set --output-dir to a controlled storage location.

## Reference(s):

- [FEEDAX](https://www.feedax.cn)
- [FEEDAX bond news API endpoint](http://221.6.15.90:18011/data-service/v1/news/bond/external/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance, terminal text summaries, CSV files, and Markdown result reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows the first five results in chat and can export full query results to timestamped CSV and Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
