## Description:

Firecrawl Scrape helps agents extract clean, LLM-optimized markdown from static or JavaScript-rendered URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape one or more web pages into markdown or other Firecrawl-supported outputs for downstream reading, analysis, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows Firecrawl CLI execution, including an unpinned npx package path.

Mitigation: Install only in environments where Firecrawl CLI execution is acceptable; prefer a pinned, reviewed Firecrawl version or a preinstalled binary.

Risk: Scraped web content may be untrusted or adversarial.

Mitigation: Review generated .firecrawl files before reusing them in prompts, documents, or automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/firecrawl-scrape)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown or JSON files, with optional links, HTML, raw HTML, or screenshots depending on Firecrawl format options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-URL and multi-URL scraping; scraped files should be treated as untrusted web content before reuse.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
