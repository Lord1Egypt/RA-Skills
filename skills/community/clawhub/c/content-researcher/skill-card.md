## Description:

Content Researcher batch-searches articles, videos, and news, optionally summarizes results, deduplicates by URL, and writes structured content research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and researchers use this skill to gather current web materials across multiple keywords and turn the results into structured Markdown or JSON research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to the configured web search tool.

Mitigation: Review keywords before running the skill and avoid submitting sensitive or confidential terms to unapproved search providers.

Risk: When summarization is enabled, result snippets are sent to the summarization provider.

Mitigation: Disable summarization for sensitive research or use only an approved summarization provider and model.

Risk: The report writer creates or overwrites the file specified by the user.

Mitigation: Review the output path before execution and avoid pointing it at important existing files unless replacement is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/content-researcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Markdown or JSON report written to a user-selected file, plus console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include search result titles, sources, links, snippets, optional AI summaries, and URL-deduplicated results.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
