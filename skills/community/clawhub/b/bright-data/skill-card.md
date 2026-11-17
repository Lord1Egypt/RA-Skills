## Description:

Web scraping and search via Bright Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirkad](https://clawhub.ai/user/meirkad)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to search Google with structured JSON results or scrape web pages into markdown through Bright Data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search script accepts the pagination cursor in shell arithmetic without validating that it is a bounded non-negative decimal integer.

Mitigation: Validate the cursor before arithmetic use and reject non-decimal, negative, or excessive values before running scripts/search.sh.

Risk: Search queries, target URLs, and API credentials are sent to Bright Data.

Mitigation: Use a limited, rotatable Bright Data API key and avoid submitting sensitive searches or URLs unless that data sharing is acceptable.

## Reference(s):

- [Bright Data Dashboard](https://brightdata.com/cp)
- [Bright Data Request API endpoint](https://api.brightdata.com/request)
- [ClawHub Skill Page](https://clawhub.ai/meirkad/skills/bright-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown for scraped pages, JSON for search results, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRIGHTDATA_API_KEY and BRIGHTDATA_UNLOCKER_ZONE environment variables.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
