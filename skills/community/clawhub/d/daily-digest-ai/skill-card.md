## Description:

Fetches RSS feeds from 92 top Hacker News blogs curated by Karpathy plus 3 Chinese tech media sources, uses AI to score and filter articles, and generates a daily digest in Markdown with Chinese-translated titles, category grouping, trend highlights, and visual statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richball876](https://clawhub.ai/user/richball876)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical readers use this skill to create a daily RSS-based technology news digest from curated engineering, AI, security, and Chinese technology media sources. The skill helps an agent collect recent articles, score and categorize them with an AI provider, and write a structured Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be persisted in plaintext configuration.

Mitigation: Avoid storing long-lived production keys, use restricted keys with quota limits, and remove saved configuration when it is no longer needed.

Risk: Article titles, descriptions, and URLs are sent to the selected AI provider for scoring and summarization.

Mitigation: Use only approved AI providers and avoid running the workflow on private or sensitive feed content.

Risk: Runtime installation through unpinned npx execution can introduce supply-chain uncertainty.

Mitigation: Verify or preinstall Bun in the execution environment before running the digest script.

Risk: Generated digest content may contain incorrect summaries or unwanted footer text.

Mitigation: Review the Markdown digest before sharing or publishing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richball876/skills/daily-digest-ai)
- [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/)
- [Bun runtime](https://bun.sh)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest file with terminal status output and setup prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes digest-YYYYMMDD.md by default or a caller-specified output path; digest language can be Chinese or English.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
