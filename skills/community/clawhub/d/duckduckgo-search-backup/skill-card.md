## Description:

Performs web searches using DuckDuckGo to retrieve real-time information from the internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macdesire](https://clawhub.ai/user/macdesire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform current web, news, image, video, instant-answer, suggestion, and map searches through DuckDuckGo without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows Python execution and package installation commands for a simple search workflow.

Mitigation: Run it in a constrained virtual environment, review commands before execution, and pin the duckduckgo-search package version.

Risk: Search workflows may retrieve current external content that is incomplete, stale, or misleading.

Mitigation: Review returned sources and corroborate important claims before using results in decisions or generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/macdesire/skills/duckduckgo-search-backup)
- [Publisher profile](https://clawhub.ai/user/macdesire)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search examples may return result titles, URLs, snippets, source metadata, dates, images, videos, map details, or JSON files depending on the requested DuckDuckGo search mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
