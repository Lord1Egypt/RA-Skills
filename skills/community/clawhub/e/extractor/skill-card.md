## Description:

Extracts structured data from HTML files or URLs using CSS selectors, XPath, regular expressions, or an OpenAI-compatible LLM endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract structured fields from HTML pages, rendered URLs, or local HTML files into JSON for scraping, ingestion, QA, and data preparation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL extraction loads user-selected URLs in a headless browser.

Mitigation: Use trusted URLs or reviewed allowlists, and avoid loading private or internal pages unless that behavior has been approved.

Risk: LLM extraction can send source HTML and possibly an API key to the configured OpenAI-compatible endpoint.

Mitigation: Use only trusted local or HTTPS endpoints, avoid remote LLM mode for private pages or local files, and disclose content sharing before broad use.

Risk: The documentation and implementation differ on LLM extraction availability.

Mitigation: Review the installed artifact behavior and update user-facing documentation before enabling LLM workflows.

## Reference(s):

- [Extractor usage documentation](artifact/references/usage.md)
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/extractor)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON extraction results with Markdown guidance and inline Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs map requested field names to extracted strings, string lists, or null values when no match is found.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
