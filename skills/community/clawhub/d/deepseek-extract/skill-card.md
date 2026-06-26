## Description: <br>
Extract full conversation content from DeepSeek shared chat links and export the conversation as Markdown or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zz0116](https://clawhub.ai/user/zz0116) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to extract authorized DeepSeek shared-chat conversations into local Markdown or JSON transcripts for review, archiving, or downstream formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Markdown or JSON transcripts may contain sensitive conversation content. <br>
Mitigation: Store outputs only in approved local paths and avoid shared or synced locations unless the content is approved for that use. <br>
Risk: The skill exports DeepSeek shared chats and could be misused on content the user is not authorized to access. <br>
Mitigation: Run it only for DeepSeek share links the user is authorized to view and export. <br>
Risk: The Playwright dependency installs and runs a local Chromium browser. <br>
Mitigation: Use a virtual environment for installation and review browser automation commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zz0116/deepseek-extract) <br>
- [Publisher profile](https://clawhub.ai/user/zz0116) <br>
- [Project homepage](https://github.com/zz0116/deepseek-extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown transcript by default, or structured JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local transcript file from an authorized DeepSeek share URL; default output path is ./deepseek_conversation.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
