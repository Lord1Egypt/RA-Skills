## Description: <br>
Use when creating complete AI-generated short videos, social videos, promotional videos, narration videos, or script-to-video outputs from a topic, brief, product, article, or approved script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darknoah](https://clawhub.ai/user/darknoah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to guide an agent through a confirmed short-video production workflow, including format selection, script confirmation, storyboard planning, asset sourcing, narration, editing, subtitles, music, rendering, and final output checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled media helper scripts can fetch arbitrary URLs and write files to user-chosen local paths. <br>
Mitigation: Review generated download commands before running them, use a dedicated project output directory, and avoid broad or sensitive filesystem paths. <br>
Risk: The workflow requires provider API credentials for media search and download helpers. <br>
Mitigation: Keep API keys in local config files or environment variables and do not paste raw credentials into chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/darknoah/ai-short-video-workflow) <br>
- [Pexels API](https://api.pexels.com/v1) <br>
- [Pixabay API](https://pixabay.com/api/) <br>
- [Pixabay Video API](https://pixabay.com/api/videos/) <br>
- [Jamendo API](https://api.jamendo.com/v3.0) <br>
- [Freesound API](https://freesound.org/apiv2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media workflow artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce video scripts, storyboard tables, asset-search commands, configuration guidance, subtitle files, ffmpeg commands, and final-output verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
