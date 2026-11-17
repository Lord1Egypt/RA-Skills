## Description:

Fetches 36kr official 24-hour hot-list article data for users asking about 36kr hot articles, trending news, technology hot lists, startup hot lists, or today's most-read articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[36kr-com](https://clawhub.ai/user/36kr-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve, format, and optionally export 36kr 24-hour hot-list article rankings for a selected date. It supports direct API fetching and helper scripts for JSON, terminal, and CSV workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included shell helper has unsafe local script behavior when run with untrusted arguments, especially `--titles --top`.

Mitigation: Use direct API fetching or the Python helper for read-only use, and avoid the shell helper with untrusted arguments until the argument handling is fixed.

Risk: The skill adds promotional recommendations and may guide users toward installing other 36kr skills beyond the core hot-list query.

Mitigation: Review or remove the post-query recommendation behavior before deployment in environments that restrict promotion or installation guidance.

Risk: The public CDN endpoint can return missing, stale, or temporarily unavailable data for a requested date.

Mitigation: Handle 404 and transient network failures explicitly, retry where appropriate, and present the queried date and fallback behavior to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/36kr-com/skills/36kr-hotlist)
- [36kr publisher profile](https://clawhub.ai/user/36kr-com)
- [36kr hot-list catalog](https://36kr.com/hot-list/catalog?channel=skills)
- [API reference](api-reference.md)
- [Usage examples](examples.md)
- [36kr hot-list JSON API template](https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown article list, JSON, CSV, terminal text, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public hot-list data without authentication; helper scripts support date selection, top-N filtering, JSON output, and CSV export.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
