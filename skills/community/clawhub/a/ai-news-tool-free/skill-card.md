## Description:

The skill helps an agent retrieve daily Chinese news, hot rankings, category-filtered lists, and article details from an external news API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal agent users use this skill to query daily Chinese news, inspect hot stories, filter by category, and read article details. The skill is best scoped to news retrieval and presentation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions broaden beyond news retrieval into database, analytics, file-processing, and command-execution use cases without clear limits.

Mitigation: Constrain activation and review to the news-list, hot-ranking, category-filter, and article-detail workflows before installation.

Risk: The skill can prompt an agent to run shell commands and write local cache or summary files.

Mitigation: Require explicit user approval for shell execution and file writes, and restrict commands to reviewed API calls and JSON/text processing.

Risk: The skill depends on an external news API and may return network errors, unavailable dates, or untrusted remote content.

Mitigation: Validate date and article parameters, handle non-200 API responses, preserve source dates, and avoid treating returned news content as authoritative without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-news-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include date parameters, article identifiers, category filters, and optional local cache or summary file paths when the agent follows command examples.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
