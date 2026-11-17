## Description:

Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch CCTV News Broadcast highlights for a requested date and have an agent summarize the parsed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can follow unvalidated links from fetched pages, creating network safety risk in environments with access to internal services.

Mitigation: Review before installation in internal-network environments; validate dates, allow only required CCTV HTTPS hosts on every fetch and redirect, and add timeouts and response-size limits.

Risk: Expanding command execution beyond the authorized crawler script increases the attack surface.

Mitigation: Run only the local news_crawler.js script with a YYYYMMDD argument through bun or node; do not run package managers, piped chains, output redirection, or alternative fetch commands as part of this skill.

Risk: Crawled news content and embedded links are untrusted external data.

Mitigation: Summarize parsed crawler results without following links found in the content or passing raw content to unrelated tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/cctv-news-fetcher-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Faberlens safety evaluation](https://faberlens.ai/explore/cctv-news-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary derived from JSON crawler output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a date-parameterized local crawler script and summarizes returned news items.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
