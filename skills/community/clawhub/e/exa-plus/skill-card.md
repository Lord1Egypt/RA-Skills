## Description:

Neural web search via Exa AI. Search people, companies, news, research, code. Supports deep search, domain filters, date ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search the web with Exa AI, retrieve targeted results across people, companies, news, research, code, and other categories, and extract text from URLs for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and submitted URLs are sent to Exa's external API.

Mitigation: Use the skill only when authorized to send the search terms, URLs, and resulting context to Exa.

Risk: Secrets, private repository details, internal-only URLs, regulated data, or confidential research targets could be exposed if submitted as inputs.

Mitigation: Do not submit those inputs unless an approved workflow permits sending them to Exa.

Risk: The skill requires an Exa API key for API access.

Mitigation: Store the key in the configured credentials file or environment variable and avoid committing it with skill artifacts.

## Reference(s):

- [Exa Search API endpoint](https://api.exa.ai/search)
- [Exa Contents API endpoint](https://api.exa.ai/contents)
- [ClawHub skill page](https://clawhub.ai/jordyvandomselaar/skills/exa-plus)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON responses and extracted text from Exa API, with shell command usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include result text, highlights, summaries, and URL content depending on the invoked script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
