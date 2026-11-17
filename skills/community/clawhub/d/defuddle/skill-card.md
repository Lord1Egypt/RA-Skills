## Description:

Extracts clean readable article content, metadata, Markdown, or JSON from URLs, raw HTML, or web page text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extrastu](https://clawhub.ai/user/extrastu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to convert web pages, raw HTML, or page text into cleaner article content for research workflows, note taking, web scraping, Obsidian clipping, and LLM processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL inputs can cause the agent or Defuddle tooling to retrieve external pages.

Mitigation: Treat URL input as explicit permission to fetch that page, and avoid private intranet URLs, authenticated pages, or sensitive documents unless that retrieval path is acceptable.

Risk: Cleaned article output may omit page elements such as navigation, comments, sidebars, ads, social buttons, or footers.

Mitigation: Use the output for readable article extraction and verify source pages directly when omitted surrounding content could affect interpretation.

## Reference(s):

- [Defuddle usage reference](references/defuddle-usage.md)
- [ClawHub skill page](https://clawhub.ai/extrastu/skills/defuddle)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown article content with metadata, or structured JSON metadata and content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title, author, site, description, published date, domain, image, word count, parse time, content, and contentMarkdown when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
