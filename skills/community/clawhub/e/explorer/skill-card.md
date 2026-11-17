## Description:

Search and analyze trending GitHub repositories by topics, star count, and creation date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical researchers use this skill to discover popular open-source GitHub projects by topic, language, star count, creation window, and sorting criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query GitHub over the network and optionally use a GitHub token for higher API rate limits.

Mitigation: Run without a token when possible; otherwise use a fine-grained, read-only, short-lived token scoped to the current command or shell session.

Risk: The artifact documentation suggests appending a GitHub token to a shell startup file, which can leave long-lived credentials on disk.

Mitigation: Do not append real tokens to ~/.zshrc or commit or sync shell configuration files containing tokens.

## Reference(s):

- [GitHub Search API reference](references/github_api.md)
- [Official GitHub REST Search documentation](https://docs.github.com/en/rest/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal text with repository names, descriptions, URLs, stars, forks, language, topics, and dates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query the GitHub Search API and may use GITHUB_TOKEN when the user provides it for higher rate limits.]

## Skill Version(s):

1.0.6 (source: server release metadata, created 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
