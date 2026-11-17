## Description:

Retrieves public company information by stock ticker symbol or SEC CIK number using the apipick Company Facts API, including company name, industry, sector, exchange, market capitalization, employee count, website, and SEC filings URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up public-company facts by ticker or SEC CIK and present market cap, headcount, exchange, website, and SEC filing links from the apipick API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, tickers, or CIKs requested through the skill are sent to apipick using the user's API key and may consume account credits.

Mitigation: Use the skill only when sharing the lookup target with apipick is acceptable, and avoid confidential watchlists or non-public research targets unless policy allows it.

Risk: The skill depends on an apipick API key for authenticated requests.

Mitigation: Store the key in APIPICK_API_KEY when possible and avoid exposing it in prompts, logs, or shared outputs.

## Reference(s):

- [apipick Company Facts API Reference](references/api_reference.md)
- [apipick API platform](https://www.apipick.com)
- [Company Facts product page](https://www.apipick.com/company-facts)
- [apipick API key dashboard](https://www.apipick.com/dashboard/api-keys)
- [ClawHub skill listing](https://clawhub.ai/javainthinking/skills/apipick-company-facts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summary of JSON API results with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY; successful requests cost one apipick credit.]

## Skill Version(s):

1.0.0 (source: release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
