## Description:

Queries ChatGPT through Scavio to retrieve answers, cited pages, search queries, and product recommendations for AI visibility and brand monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, brand analysts, and developers use this skill to inspect ChatGPT answers, citations, search queries, and product mentions across prompts for AI visibility monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts sent through this skill are shared with Scavio's external API.

Mitigation: Use only prompts you are comfortable sharing with Scavio and keep the API key private.

Risk: Each answered prompt consumes two paid credits; large batches can increase costs.

Mitigation: Confirm with the user before running large prompt batches.

Risk: ChatGPT answers and cited sources can vary between runs.

Mitigation: Surface the returned answer and citations, and use repeated prompts to estimate mention rates rather than treating one answer as definitive.

## Reference(s):

- [Scavio ChatGPT API documentation](https://scavio.dev/docs/chatgpt-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=chatgpt-scraper-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/chatgpt-scraper-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code]

**Output Format:** [Markdown summaries with cited sources; optional Python example and structured JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can vary between runs; prompts are limited to 1,024 characters.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
