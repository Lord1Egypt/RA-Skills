## Description: <br>
Universal web clipper for Obsidian Vault that saves content from X/Twitter, WeChat, Douyin, Xiaohongshu, GitHub, and generic web pages into local Markdown notes with media, tags, and wikilinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgissing](https://clawhub.ai/user/zgissing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who use Claude Code with Obsidian use this skill to clip selected URLs into a vault as Markdown notes with local media, frontmatter, tags, and wikilinks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected URLs and their images or videos are fetched and saved into the configured vault folder. <br>
Mitigation: Use a narrow vault path and install only if saving selected URL content locally is acceptable. <br>
Risk: Optional Douyin support depends on third-party downloader tooling and cookie-based workflows. <br>
Mitigation: Review the downloader before enabling it and use a separate browser profile or account for cookie-based workflows. <br>
Risk: Optional CDP browser support can access a browser session when enabled. <br>
Mitigation: Keep CDP disabled unless needed and bind it only to a trusted localhost endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zgissing/clip-to-your-vault) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [douyin-downloader](https://github.com/jiji262/douyin-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, Obsidian wikilinks, and local media file references; may include shell commands for setup or fetching content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes clipped notes and downloaded media into user-configured vault directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
