## Description:

Posts text, media, quote tweets, and long-form Markdown articles to X (Twitter) through Chrome-based workflows while keeping final publishing under user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, creators, and developer agents use this skill to prepare X posts, quote tweets, media posts, and long-form X Articles from user-provided content. The skill is suited for workflows where the agent drafts or stages content in Chrome and the user reviews before any public publishing action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare externally visible X posts and articles in a real account session.

Mitigation: Review every prepared post or article and require explicit final user confirmation before clicking Post, Publish, or using a submit path.

Risk: The skill may control Chrome, clipboard contents, file picker actions, and paste keystrokes.

Mitigation: Install and run it only in trusted environments where the user accepts those permissions and can observe the browser session.

Risk: Markdown articles with remote images can introduce untrusted external content into the workflow.

Mitigation: Avoid processing untrusted Markdown with remote images; review article content and image sources before staging in X.

Risk: The npx fallback can execute runtime tooling that is not already installed locally.

Mitigation: Prefer a preinstalled trusted Bun runtime and review dependency updates before use.

Risk: Troubleshooting can include broad Chrome process-kill recovery for CDP sessions.

Mitigation: Use caution before process recovery steps and preserve important browser work before allowing Chrome session cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-post-to-x)
- [Baoyu Skills Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-x)
- [Regular Posts Guide](references/regular-posts.md)
- [X Articles Guide](references/articles.md)
- [Codex Chrome Extension File Upload Guidance](https://developers.openai.com/codex/app/chrome-extension#upload-files)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and prepared browser draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stage content in a real Chrome/X session; final public posting requires explicit user confirmation.]

## Skill Version(s):

1.58.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
