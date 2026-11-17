## Description:

Ad creative search assistant that helps users search competitor ad creatives through AdMapix and returns results as generated H5 pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiwei199608](https://clawhub.ai/user/baiwei199608)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, growth teams, and developers use this skill to search ad creatives by keyword, creative type, region, date range, and sort order. The agent confirms parsed parameters before sending the search to AdMapix and returns a shareable results page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, regions, dates, and other filters are sent to AdMapix to generate the results page.

Mitigation: Review and confirm parsed parameters before search, and avoid submitting sensitive or confidential queries.

Risk: The skill requires an AdMapix API key for searches.

Mitigation: Configure only an API key intended for this service, use a trusted installer, and never print or expose the key value.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/baiwei199608/skills/admapix-1-0-13)
- [AdMapix Website](https://www.admapix.com)
- [AdMapix Search API](https://api.admapix.com/api/data/search)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)
- [AdMapix GitHub Link Listed In README](https://github.com/fly0pants/admapix)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with parameter summaries, setup guidance, curl commands, and generated H5 result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language, confirms parsed parameters before search, and returns generated result-page links instead of inline result lists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
