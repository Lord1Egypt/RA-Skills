## Description:

Save and organize web articles as bookmarks with AI summaries and auto-tagging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chliny](https://clawhub.ai/user/chliny)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to bookmark web articles or pasted text into a structured Markdown collection with generated summaries and tags. It can also help delete saved articles after user confirmation and keep a tag index current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit and push every Markdown file in the configured bookmark directory to GitHub, which may expose unrelated notes.

Mitigation: Use a dedicated bookmark directory or private dedicated repository, avoid pointing ARTICLE_BOOKMARK_DIR at existing projects or notes vaults, and verify the destination repository and exact files before enabling ARTICLE_BOOKMARK_GITHUB.

## Reference(s):

- [Article Bookmarker Skill](https://clawhub.ai/chliny/skills/article-bookmarker)
- [bookmark.sh Script Guide](references/bookmark-script.md)
- [Article Bookmarker - File Structure](references/file-structure.md)
- [Article Bookmarker - Usage Examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with article content, summaries, tags, tag indexes, and inline shell commands for git synchronization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARTICLE_BOOKMARK_DIR; optional ARTICLE_BOOKMARK_GITHUB enables GitHub synchronization using git and gh.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
