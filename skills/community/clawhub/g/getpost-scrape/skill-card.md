## Description:

Scrape any web page with a headless browser and extract text or screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the GetPost web scraping API for authorized pages, returning page text, screenshots, or content captured after waiting for a selector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scrape requests and signup details are sent to getpost.dev.

Mitigation: Use the skill only when the provider is acceptable for the workflow and avoid sending sensitive, authenticated, personal, or regulated content unless authorized.

Risk: Scraping can capture page text or screenshots from sites where access or reuse is restricted.

Mitigation: Use the API only on public pages or pages where scraping and capture are permitted.

## Reference(s):

- [GetPost Scrape API Documentation](https://getpost.dev/docs/api-reference#scrape)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API signup, authentication, scrape request examples, and option guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
