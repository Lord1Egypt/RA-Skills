## Description:

Posts content to Weibo (微博), including regular text, image, and video posts, and headline articles (头条文章) from Markdown input via Chrome CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Weibo posts and long-form Weibo headline articles from text, media files, or Markdown. The browser remains open so the user can review and publish manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated browser session, system clipboard automation, real paste keystrokes, and process control.

Mitigation: Review the skill before installing, run it with an isolated Chrome profile, and verify all browser content before publishing.

Risk: The npx fallback can download and run the Bun runtime path at execution time.

Mitigation: Prefer a locally installed trusted Bun runtime instead of the npx fallback.

Risk: Clipboard contents, authenticated Weibo session state, and the predictable temporary article file may be exposed on shared machines.

Mitigation: Avoid running the skill on shared machines or clear sensitive clipboard and temporary content after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-post-to-weibo)
- [Skill homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-weibo)
- [Weibo homepage](https://weibo.com/)
- [Weibo article editor](https://card.weibo.com/article/v3/editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser-composition guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser-filled Weibo drafts for manual user review and publishing.]

## Skill Version(s):

1.117.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
