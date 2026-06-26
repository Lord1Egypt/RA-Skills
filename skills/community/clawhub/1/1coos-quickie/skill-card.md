## Description: <br>
Quickly saves web content as formatted Markdown from URLs including YouTube, Twitter/X, WeChat, Bilibili, Telegram, RSS, and general web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1coos](https://clawhub.ai/user/1coos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-taking users use this skill to clip URL content into local Markdown notes, optionally preserving raw extraction output or applying Obsidian-style formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external GitHub-hosted x-reader dependency through uvx at runtime. <br>
Mitigation: Install only when comfortable with that dependency path, and pin or review the external dependency when stronger supply-chain control is required. <br>
Risk: The reader makes network requests to the provided URL and platform-specific APIs. <br>
Mitigation: Avoid clipping sensitive URLs in stricter environments and use explicit clipping commands so the intended URL is clear before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1coos/1coos-quickie) <br>
- [x-reader GitHub repository](https://github.com/runesleo/x-reader) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes extracted content to a configured local directory; raw mode skips Obsidian-style formatting.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
