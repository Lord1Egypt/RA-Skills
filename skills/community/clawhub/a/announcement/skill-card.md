## Description:

Query BingX official announcements by module type, including latest announcements, promotions, product updates, maintenance notices, listings, delistings, funding rates, and crypto scout updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julian-l](https://clawhub.ai/user/julian-l)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and summarize public BingX announcements by module type, language, and page, and to generate compliant API calls for the announcement endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may default to Traditional Chinese when no language is specified.

Mitigation: Ask for or set an explicit supported language, such as en-us for English or zh-tw for Traditional Chinese.

Risk: Generated API calls can fail if contentType, language, or page values do not match the documented constraints.

Mitigation: Validate contentType against the documented enum, use supported language values, and keep page as an integer of 1 or greater.

Risk: The skill queries external public BingX endpoints, so responses depend on endpoint availability and returned data freshness.

Mitigation: Surface API errors or network failures clearly and use the documented fallback behavior only for network or timeout errors.

## Reference(s):

- [Bingx Announcement ClawHub page](https://clawhub.ai/julian-l/skills/announcement)
- [API Reference](artifact/api-reference.md)
- [BingX announcement endpoint](https://open-api.bingx.com/openApi/content/v1/announcement)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown responses with TypeScript and cURL snippets plus summarized announcement fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API guidance; no credentials required; supports contentType, language, and page parameters.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
