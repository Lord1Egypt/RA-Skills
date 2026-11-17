## Description:

Run Yandex web searches through Dataify, using documented Yandex parameters and safe defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search Yandex from an agent workflow, tune query parameters such as domain, language, page, and safe-search mode, and receive user-facing results or raw JSON/HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Dataify requests require an API token and may consume account credits.

Mitigation: Use DATAIFY_API_TOKEN instead of passing tokens in commands, never expose token values, and review cost-affecting options such as page, result count, cache bypass, and broad query scope before execution.

Risk: Raw parameter overrides can change API behavior outside the standard documented Yandex search fields.

Mitigation: Prefer the documented command-line fields and safe defaults; use params-json only after reviewing the API field documentation.

Risk: Search results may include untrusted third-party web content.

Mitigation: Preserve source links, distinguish missing fields from empty values, and review returned results before relying on them for decisions.

## Reference(s):

- [Dataify Yandex Search API Fields](references/api_fields.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-yandex-search)
- [Dataify Scraper API Endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text search results, with raw JSON or HTML only when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview tables, setup guidance for DATAIFY_API_TOKEN, source links, truncation notes, and optional raw response output.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
