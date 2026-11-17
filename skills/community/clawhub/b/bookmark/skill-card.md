## Description:

Search and browse the Shuqianlan bookmark library by keyword, recent updates, top categories, category articles, and category links in a read-only mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and browse public Shuqianlan bookmark content from an agent session. It supports keyword search, latest articles, category lists, category articles, and category links without subscription or scheduled digest behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch from arbitrary network locations when BOOKMARK_BASE_URL or --base-url is set to an alternate endpoint.

Mitigation: Use the default Shuqianlan endpoint unless the user explicitly requests an override, and avoid untrusted, local, or private-network endpoints.

Risk: Links and bookmark results from an overridden endpoint may be untrusted.

Mitigation: Treat results from non-default endpoints as untrusted and review links before opening or acting on them.

## Reference(s):

- [Shuqianlan](https://shuqianlan.com)
- [openclaw-server Bookmark Map](references/openclaw-server-bookmark-map.md)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/bookmark)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with links returned from a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only bookmark results; limit and page flags control result volume where supported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
