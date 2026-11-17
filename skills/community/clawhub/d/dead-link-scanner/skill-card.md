## Description:

Scan websites, markdown files, and HTML files for broken links (dead links). Use when checking a website for 404s, validating links in documentation or README files, auditing link health before a deploy, or finding broken internal/external links. Supports recursive crawling with depth limits, markdown file scanning, and output in text or JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and site operators use this skill to audit website, Markdown, and HTML links before publishing or deploying content. It helps identify unreachable links, HTTP errors, and connection failures with text or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to links it finds in crawled pages or selected local files.

Mitigation: Use it only on documentation and sites intended for audit, and prefer --internal-only when external link checks are not needed.

Risk: Scanning private files can expose confidential internal URLs or secret-bearing query strings through outbound requests or generated output.

Mitigation: Avoid scanning private files that contain confidential links, tokens, or sensitive query parameters.

Risk: Recursive crawling can generate request volume across discovered links.

Mitigation: Set conservative depth, delay, timeout, and max-urls values for large sites or shared environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Analysis]

**Output Format:** [Plain text summaries or JSON result arrays, often summarized in Markdown by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner reports each checked URL with status, source location, and broken-link state; the CLI exits nonzero when broken links are found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
