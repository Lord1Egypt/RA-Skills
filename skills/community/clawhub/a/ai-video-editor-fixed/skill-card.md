## Description: <br>
Official-core Sparki video editor listing kept under the ai-video-editor-fixed slug for compatibility, now aligned with the latest sparki-video-editor setup, API-key, upload, and command guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Sparki cloud video-editing workflows, including API-key setup, upload, style-guided or prompt-driven edits, polling, download, captions, resizing, and short-form video creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill uploads selected videos and editing prompts to Sparki's cloud video-editing service. <br>
Mitigation: Use it only with videos and prompts suitable for Sparki processing, and confirm translation, captioning, or other content-changing instructions before editing. <br>
Risk: The setup workflow can store a Sparki API key in $HOME/.openclaw/config/sparki.json. <br>
Mitigation: Protect that config file, prefer SPARKI_API_KEY for ephemeral use when appropriate, and delete the stored config if local credential persistence is not desired. <br>


## Reference(s): <br>
- [Sparki homepage](https://sparki.io) <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-video-editor-fixed) <br>
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local or Telegram Mini App uploads, remote video-editing tasks, polling, downloads, and delivery hints.] <br>

## Skill Version(s): <br>
1.0.11 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
