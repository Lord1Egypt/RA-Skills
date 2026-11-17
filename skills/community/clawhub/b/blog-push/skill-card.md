## Description:

blog-push helps agents publish Markdown posts, daily digests, and weekly logs into a configured Hugo blog, including front matter generation, cover image handling, draft mode, shortcode guidance, and content-based category and tag suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to move completed Markdown documents and optional cover images into a Hugo blog structure for posts, daily entries, or weekly logs. It supports configuration checks, directory selection, generated Hugo front matter, draft handling, and content-based publishing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can overwrite an existing post at the resolved destination path.

Mitigation: Use the skill on a version-controlled Hugo blog and review the destination path before running the publish command.

Risk: Generated output replaces the source document's existing front matter in the published Markdown file.

Mitigation: Review the generated front matter after publishing, especially title, date, draft status, image, libraries, categories, and tags.

Risk: Incorrect blog or content-directory configuration can write files outside the intended Hugo section.

Mitigation: Run the configuration check first and verify HUGO_BLOG_DIR plus posts, daily, weekly, and template paths before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redisread/skills/blog-push)
- [Publisher profile](https://clawhub.ai/user/redisread)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite local Markdown and cover image files in the configured Hugo blog directory when the generated commands are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
