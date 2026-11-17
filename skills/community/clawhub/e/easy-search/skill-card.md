## Description:

Simple web search using multiple search engines with no API key required. Supports Google, Bing, DuckDuckGo, Baidu, Sogou, 360, Brave, Yandex. Features time filtering, interactive mode, snippet extraction, and network diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkall](https://clawhub.ai/user/hkall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Easy Search to run web searches from the command line without API keys, retrieve snippets, apply time filters, and switch among supported public search engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to third-party search services and may expose secrets, sensitive internal terms, or confidential topics.

Mitigation: Avoid searching for secrets or sensitive internal terms, and use an appropriate network or proxy environment for the data being searched.

Risk: Search queries and results may be cached locally in plaintext.

Mitigation: Use --no-cache for sensitive searches and --clear-cache to remove saved results.

Risk: Optional dependencies and public search interfaces can affect result availability, reliability, and privacy posture.

Mitigation: Install dependencies in a normal user environment, preferably a virtual environment, and review returned URLs before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hkall/skills/easy-search)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, CSV, or simple text search results with titles, URLs, snippets, engine metadata, and optional diagnostics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be cached locally for faster repeated searches; users can disable or clear the cache.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
