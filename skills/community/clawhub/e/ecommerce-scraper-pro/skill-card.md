## Description:

Extracts structured data from webpages and APIs for batch collection workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and data teams use this skill to prepare scraping workflows for ecommerce price monitoring, market research, lead collection, and API data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be sent to user-provided endpoints.

Mitigation: Use only trusted HTTPS endpoints, avoid placing valuable secrets directly on the command line, and prefer managed secret handling where available.

Risk: Local output files may contain sensitive scraped or API data.

Mitigation: Treat generated files as sensitive, restrict access, and remove data that should not be retained.

Risk: Scraping activity may conflict with site terms, robots.txt, copyright, or privacy requirements.

Mitigation: Review the target site's terms, robots.txt, and applicable privacy rules before scraping, and keep request rates controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/ecommerce-scraper-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; scraper runs can produce JSON, CSV, or Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local output files containing scraped webpage or API response data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
