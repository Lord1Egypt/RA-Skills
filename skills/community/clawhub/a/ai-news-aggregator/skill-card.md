## Description:

AI/technology news aggregation engine that fetches 100+ RSS sources concurrently, scores relevance, deduplicates across days, and uses unified prefetching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to retrieve AI and technology news, recent papers, GitHub trends, and AI company updates. It is intended for Chinese-language news workflows that summarize and filter public web and RSS sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact contains only the instruction file while the skill directs agents to run helper scripts.

Mitigation: Verify the installed package includes the referenced Python scripts before using the skill.

Risk: The workflow fetches public web and RSS sources, so results may be incomplete, unavailable, stale, or affected by upstream source changes.

Mitigation: Confirm important news items against the original sources before relying on or redistributing summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/ai-news-aggregator)
- [Project homepage](https://github.com/lanyasheng/ai-news-aggregator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on package-provided Python scripts and public web or RSS source availability.]

## Skill Version(s):

2.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
