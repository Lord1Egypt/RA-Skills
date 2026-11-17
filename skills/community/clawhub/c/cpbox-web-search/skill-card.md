## Description:

Provides a paid web-search endpoint that returns ranked results with snippets, URLs, thumbnails, freshness filters, SafeSearch, custom Goggles ranking, pagination, and rich result types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a paid CPBox web-search API for search interfaces, data extraction, grounding workflows, custom-ranked search, and location-aware or rich-result queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented payment helper is installed without an exact pinned version.

Mitigation: Review the payment helper before use and prefer an exact pinned version or a lockfile-managed install.

Risk: Location-aware searches can send precise latitude and longitude.

Mitigation: Send precise coordinates only when location-specific results are necessary and the user has agreed to share that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sprintmint/skills/cpbox-web-search)
- [Publisher Profile](https://clawhub.ai/user/sprintmint)
- [x402 Payment Setup](https://github.com/springmint/cpbox-skills#prerequisites)
- [CPBox API Provider](https://www.cpbox.io)
- [CPPay Facilitator](https://www.cppay.finance)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls]

**Output Format:** [Markdown with HTTP, bash, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API returns structured JSON search results and may include web, news, video, discussion, FAQ, infobox, location, schema, and rich callback data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
