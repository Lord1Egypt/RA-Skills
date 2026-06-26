## Description: <br>
Routes Douyin links through download, transcription, polishing, structural analysis, and optional rewriting workflows for agents that extract assets or copy from Douyin videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyhui](https://clawhub.ai/user/anyhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content workflow operators use this skill to route Douyin links into no-watermark downloads, audio transcription, cleaned copy, content structure analysis, and optional rewrite drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Douyin session cookies and API keys. <br>
Mitigation: Use environment variables or a secret manager, avoid pasting full browser cookies into chat, and rotate credentials if they are exposed. <br>
Risk: The skill may fetch or run third-party downloader code and install dependencies. <br>
Mitigation: Review cloned code before execution, run it in an isolated workspace, and confirm system package installation steps before granting elevated permissions. <br>
Risk: Media may be sent to transcription APIs for processing. <br>
Mitigation: Confirm that the media is appropriate for external processing and avoid sending sensitive or restricted content. <br>
Risk: Account-wide, likes, favorites, or collection modes can retrieve more content than a single-link task requires. <br>
Mitigation: Prefer specific Douyin links and limit batch modes to clearly scoped tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anyhui/douyin-learning-pipeline) <br>
- [Migration guide](artifact/references/migration-guide.md) <br>
- [Subskills map](artifact/references/subskills-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with shell commands, configuration prompts, and links or paths to generated media, transcript, and draft files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request Douyin cookies, API keys, or destination document details when required configuration is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
