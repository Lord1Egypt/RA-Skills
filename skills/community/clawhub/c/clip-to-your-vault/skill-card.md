## Description:

Universal web clipper for Obsidian Vault that saves content from X/Twitter, WeChat, Douyin, Xiaohongshu, GitHub, and generic web pages when a user asks to clip or save a URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgissing](https://clawhub.ai/user/zgissing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill in Claude Code to turn web URLs into organized Obsidian notes with frontmatter, local media, tags, and cross-platform wikilinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full URLs to third-party services while fetching or parsing clipped content.

Mitigation: Review URLs before clipping and avoid private, tokenized, or sensitive links unless sharing them with those services is acceptable.

Risk: Setup and optional handlers may use curl-to-bash, git clone, npm, pip, Playwright, or unpinned dependency installation paths.

Mitigation: Inspect setup scripts and dependency manifests before execution, then pin or vendor dependencies for managed environments.

Risk: The skill writes downloaded media and generated notes to the local Obsidian vault.

Mitigation: Configure the vault and attachments paths carefully, keep overwrite confirmation enabled, and review generated files before syncing or publishing.

## Reference(s):

- [Clip to Your Vault on ClawHub](https://clawhub.ai/zgissing/skills/clip-to-your-vault)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [douyin-downloader](https://github.com/jiji262/douyin-downloader)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter, Obsidian wikilinks, local media files, and setup/configuration commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite files under the configured vault path after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
