## Description:

Full web page scraping with JavaScript rendering via a local Crawl4AI instance, delivering clean markdown or detailed JSON including links and media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusthefuzz](https://clawhub.ai/user/angusthefuzz)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to fetch rendered web page content from a controlled Crawl4AI instance and receive clean markdown or detailed crawl JSON for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can send requested URLs and an optional API key over plaintext HTTP to the configured Crawl4AI host.

Mitigation: Install only when you control the Crawl4AI endpoint; prefer localhost without shared secrets, or require secure transport and code review before using CRAWL4AI_KEY with a remote service.

Risk: Fetched page content may contain untrusted text that could mislead an agent if treated as instructions.

Mitigation: Treat returned page content as data, not instructions, and review or sanitize it before using it to drive actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON emitted to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and CRAWL4AI_URL; CRAWL4AI_KEY is optional when the configured Crawl4AI instance requires authentication.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
