## Description: <br>
面向 Vlog 场景的 Sparki skill 变体，帮助用户把日常、旅行和生活方式素材剪成更有节奏的创作者风格视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this Chinese-language skill to upload local Vlog footage to Sparki, request prompt-driven or style-guided edits, poll processing status, and download the finished video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video files are uploaded to Sparki for processing. <br>
Mitigation: Use this skill only for videos you are comfortable sending to Sparki, and ask for local-only editing when remote processing is not acceptable. <br>
Risk: The Sparki API key may be stored in the local OpenClaw config directory. <br>
Mitigation: Prefer the SPARKI_API_KEY environment variable on shared systems and protect access to $HOME/.openclaw/config. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-vlog-editor-zh) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI may return task IDs, asset metadata, result URLs, local output paths, and delivery hints.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
