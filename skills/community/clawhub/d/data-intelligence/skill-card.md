## Description:

Data Intelligence helps agents plan and run Apify crawling, PinchTab browser automation, and content-analysis workflows for lead generation, competitor monitoring, trend research, e-commerce intelligence, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operators use this skill to guide web data collection, browser-assisted validation, data cleanup, competitor analysis, trend research, and report generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run a remote PinchTab installer with curl piped to bash.

Mitigation: Review and independently verify the installer and its exact contents before running it; prefer a pinned, auditable installation path.

Risk: The skill handles API credentials through environment variables and local .env files.

Mitigation: Store APIFY_TOKEN in a secure environment or secret manager, keep .env files out of source control, and restrict local file permissions.

Risk: The data-collection workflows can target third-party platforms and accounts.

Mitigation: Run scraping and browser automation only for data, accounts, and platforms where the user has authorization, and respect applicable platform terms and rate limits.

## Reference(s):

- [Data Intelligence skill page](https://clawhub.ai/huamu668/skills/data-intelligence)
- [Apify Documentation](https://docs.apify.com)
- [Apify Actor Store](https://apify.com/store)
- [PinchTab Documentation](https://pinchtab.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and report-template snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated reports, lead lists, CSV/JSON export commands, and browser automation workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
