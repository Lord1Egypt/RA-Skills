## Description:

Search the web via the Bright Data CLI using `bdata search` for Google, Bing, or Yandex SERP results and `bdata discover` for intent-ranked semantic results with optional page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and run Bright Data CLI web search or discovery commands, collect SERP or semantic result URLs, and verify JSON result quality before downstream scraping or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, target URLs, and optional fetched page content may be sent through Bright Data.

Mitigation: Install only when Bright Data web search is intended, and avoid `--include-content` unless full page bodies are needed.

Risk: Search and discovery results can be empty, mislocalized, or contain block-page content when page bodies are included.

Mitigation: Validate JSON parsing, result counts, expected fields, country and language fit, and block-page signatures before using the output.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/meirk-brd/skills/brightdata-search)
- [flags.md](references/flags.md)
- [patterns.md](references/patterns.md)
- [examples.md](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and JSON verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that write JSON search or discovery outputs to local files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
