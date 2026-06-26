## Description: <br>
Analyzes Douyin videos by collecting basic metrics, extracting frames and audio locally, and generating a structured content, visual, transcript, and copywriting report with Zhipu AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, and developers use this skill to analyze Douyin links or local video files and produce structured reports about engagement metrics, visual style, speech content, hooks, and reusable creative elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video frames and audio clips are sent to Zhipu AI for recognition and analysis. <br>
Mitigation: Use only videos approved for external AI processing and disclose this data flow to users before running analysis. <br>
Risk: Crafted links or local file names could trigger local shell command execution paths reported by the security evidence. <br>
Mitigation: Avoid untrusted URLs and oddly named local files, run the skill in a constrained workspace, and update when the maintainer replaces shell-string execution with argument-array execution. <br>
Risk: Temporary media files may remain on disk after errors or interrupted runs. <br>
Mitigation: Run in a workspace with appropriate storage controls and remove temp downloads, frames, and audio files after failed or interrupted analyses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/franklu0819-lang/douyin-video-analyzer) <br>
- [Zhipu AI Chat Completions Endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Console text and Markdown-style analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg, yt-dlp, node, Playwright Chromium, and ZHIPU_API_KEY; sends selected video frames and audio clips to Zhipu AI.] <br>

## Skill Version(s): <br>
3.7.4 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
