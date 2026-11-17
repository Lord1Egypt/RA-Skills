## Description:

Load CSV files and ask questions in plain English with AI-powered natural language queries via Anthropic, OpenAI, or local Ollama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and data analysts use this skill to load delimited tabular data, profile columns, run structured filters or aggregates, and ask natural language questions that return plain-English answers with supporting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI query mode shares column names, statistics, the first five rows, and user questions with the configured model provider.

Mitigation: Use local Ollama or an approved provider for sensitive datasets, and avoid sending confidential data to providers that are not approved for the use case.

Risk: AI-generated analysis may be incomplete or incorrect for important business, financial, legal, or operational decisions.

Mitigation: Verify generated answers against the underlying CSV data or independent analysis before relying on them.

Risk: A custom OLLAMA_HOST can direct dataset summaries and questions to an unintended host.

Mitigation: Use trusted local or managed Ollama endpoints and review OLLAMA_HOST values before running natural language queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/csv-brain)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return plain-English AI answers, structured query objects, profile statistics, or provider setup commands depending on the user request.]

## Skill Version(s):

1.0.3 (source: server release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
