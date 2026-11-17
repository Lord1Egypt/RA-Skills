## Description:

Bosszp guides agents through scraping BOSS Zhipin job listings with Scrapy, importing the data into MySQL, and creating Flask and Highcharts visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to build a BOSS Zhipin job-market data pipeline that collects listings, cleans and imports CSV data into MySQL, and visualizes salary, company, benefit, and requirement patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk scraping a named third-party platform with cookies and custom headers can create authorization, terms-of-use, or account-risk concerns.

Mitigation: Run the crawler only against data the user is authorized to collect, avoid personal or session cookies unless necessary and permitted, and document clear rate limits.

Risk: Weak install hygiene can introduce unreviewed dependencies, including the `flash` package named in the install commands.

Mitigation: Replace ad hoc install commands with a pinned, reviewed requirements file after removing or verifying `flash`.

Risk: Collected job listing data can be retained or reused beyond the intended analysis scope.

Mitigation: Define retention rules before collection and delete intermediate CSV, database, and dashboard outputs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/skills/bosszp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, Python snippets, configuration guidance, and CSV field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated crawler, database, and dashboard guidance should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
