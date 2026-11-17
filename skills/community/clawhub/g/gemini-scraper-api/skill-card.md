## Description:

Retrieves Gemini answers, cited URLs, and recommended products through Scavio for AI visibility and brand monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and research teams use this skill to inspect Gemini answers, citations, and product recommendations for brand visibility and share-of-voice analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Scavio's external API and may expose sensitive information.

Mitigation: Do not submit secrets or private customer data unless Scavio is approved for that data.

Risk: Each answered prompt spends 5 credits, including repeated visibility checks.

Mitigation: Confirm with the user before running large prompt lists.

## Reference(s):

- [Scavio Gemini API documentation](https://scavio.dev/docs/gemini-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=gemini-scraper-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=gemini-scraper-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/gemini-scraper-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown answers with cited URLs and product recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may vary between runs; each answered prompt uses 5 credits.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
