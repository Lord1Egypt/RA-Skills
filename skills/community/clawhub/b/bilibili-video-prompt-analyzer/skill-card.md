## Description: <br>
Analyze Bilibili AI-generated videos to extract/reverse-engineer prompts for imitation and replication, including frames, subtitles, and detailed ComfyUI/Seedance-format prompt breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jilanfang](https://clawhub.ai/user/jilanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, video creators, and prompt engineers use this skill to analyze Bilibili AI-generated videos and turn downloaded frames and subtitles into reusable keyframe prompts, scene breakdowns, master prompts, and voiceover reference text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded videos, frames, subtitles, style, or voiceover material may be copyrighted or otherwise restricted. <br>
Mitigation: Confirm permission to download, analyze, and reuse the source material before using the skill outputs. <br>
Risk: A Bilibili URL may resolve to a playlist or other broader download scope than intended. <br>
Mitigation: Verify whether the link is a single video or playlist and run downloads in a dedicated output folder. <br>
Risk: Media tooling installed from untrusted sources can introduce ordinary supply-chain risk. <br>
Mitigation: Install ffmpeg and yt-dlp only from trusted package managers or official sources. <br>
Risk: Subtitle output can be incomplete when a video has burned-in subtitles because OCR extraction is not implemented. <br>
Mitigation: Review subtitle output before relying on it and use manual or OCR extraction when subtitles are not embedded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jilanfang/bilibili-video-prompt-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands, prompt sections, scene tables, and local media or subtitle file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes technical metadata, keyframe prompts, scene sequence breakdowns, a full video master prompt, negative prompt guidance, and extracted subtitle text when available.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
