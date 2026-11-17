## Description:

Real-time news aggregation skill that fetches trending GitHub repos, social posts from key tech/AI figures, and breaking news from major outlets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yealexchen](https://clawhub.ai/user/yealexchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other CLI users use this skill to fetch current GitHub trends, social or blog updates, and technology, AI, economics, or politics headlines without leaving an agent terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic outbound requests fetch third-party news, RSS, Google News, and GitHub API content.

Mitigation: Review network access expectations before installation and run the skill only in environments where outbound news and repository lookups are acceptable.

Risk: A GitHub token may be used for higher API rate limits.

Mitigation: Provide only a minimal read-only token through the GITHUB_TOKEN environment variable and avoid passing credentials as command-line arguments.

Risk: Third-party feed content is rendered into Markdown and may include misleading, stale, or unsafe source text.

Mitigation: Treat fetched headlines and snippets as untrusted third-party content and verify important claims against the linked source before acting on them.

Risk: The skill forces a promotional footer in non-JSON responses.

Mitigation: Review the response format before enabling the skill in user-facing or branded workflows.

## Reference(s):

- [GitHub Trending](references/github.md)
- [Breaking News](references/news.md)
- [Social Posts](references/social.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with clickable links, markdown tables for repositories, bulleted news and social updates, or JSON when requested with the script flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; can use an optional GITHUB_TOKEN environment variable for higher GitHub API rate limits; fetches third-party RSS, Google News, and GitHub API content.]

## Skill Version(s):

1.1.6 (source: server release metadata; artifact frontmatter reports 1.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
