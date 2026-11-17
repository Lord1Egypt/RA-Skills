## Description:

Scrapes Craigslist NY service ads to find small owner-operated businesses in Staten Island, Brooklyn, and the Bronx for lead generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayjjimenez](https://clawhub.ai/user/jayjjimenez)

### License/Terms of Use:


## Use Case:

Developers, operators, or sales teams use this skill to scan Craigslist NY service listings for owner-operated businesses in target boroughs, prioritize leads with phone numbers, and optionally append results to a local markdown lead list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound Craigslist requests and can be scheduled for recurring scraping.

Mitigation: Run scheduled scans only when recurring collection is intended and keep frequency aligned with site terms and operational needs.

Risk: When --save is used, lead and contact details are appended to a local markdown file.

Mitigation: Store the lead list in an approved location and review retention, access, and privacy handling before sharing it.

Risk: The --enrich mode follows listing URLs without strong validation.

Mitigation: Use --enrich cautiously and validate or constrain listing URLs before relying on enriched contact data.

## Reference(s):

- [ClawHub Craigslist Monitor skill page](https://clawhub.ai/jayjjimenez/skills/craigslist-monitor)
- [Craigslist NY plumber search](https://newyork.craigslist.org/search/sss?query=plumber&nearby=1)
- [Craigslist NY HVAC search](https://newyork.craigslist.org/search/sss?query=hvac&nearby=1)
- [Craigslist NY auto repair search](https://newyork.craigslist.org/search/sss?query=auto+repair&nearby=1)
- [Craigslist NY dental search](https://newyork.craigslist.org/search/sss?query=dental&nearby=1)
- [Craigslist NY contractor search](https://newyork.craigslist.org/search/sss?query=contractor&nearby=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; runtime output is console text or a markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional --save appends lead/contact details to a local markdown file; optional --enrich fetches listing pages for phone numbers.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
