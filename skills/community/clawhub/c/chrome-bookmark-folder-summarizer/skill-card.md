## Description:

Reads Chrome bookmarks and extracts URLs by a user-provided folder name, then generates batch webpage summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blacker521](https://clawhub.ai/user/blacker521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract URLs from a named Chrome bookmark folder and summarize the bookmarked webpages in batch. It is useful when a user wants a structured overview, comparison, and reading order for saved links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Chrome bookmark data for a named folder, which may reveal private saved links.

Mitigation: Use it only for folders intended for summarization and review the extracted URL list before fetching pages.

Risk: Bookmarked URLs may include private intranet or authenticated pages.

Mitigation: Avoid running the skill on folders containing private or authenticated links unless that access is intended.

Risk: Fetched webpage content can be stale, misleading, or adversarial.

Mitigation: Treat page content as untrusted and review summaries before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blacker521/skills/chrome-bookmark-folder-summarizer)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with JSON URL extraction output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original bookmark order and includes a cross-page comparison.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
