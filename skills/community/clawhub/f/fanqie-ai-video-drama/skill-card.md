## Description: <br>
Batch generates AI video drama episodes from multi-chapter novel text, including scripts, voiceover, subtitles, covers, titles, tags, and local episode outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to turn serialized novel chapters into short-form video drama episode packages for TikTok, Douyin, Kuaishou, or similar publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Novel text, prompts, and narration may be sent to third-party AI video, image, and TTS services. <br>
Mitigation: Use only content that is approved for those providers, and avoid confidential, unpublished, regulated, or rights-restricted text unless provider terms and permissions are acceptable. <br>
Risk: The skill writes generated media locally and depends on ffmpeg and node-fetch being available. <br>
Mitigation: Run it in a controlled workspace, confirm required dependencies before use, and review generated files before publishing or redistributing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghwyever/fanqie-ai-video-drama) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Video, Images, Audio] <br>
**Output Format:** [Local episode folders containing MP4 video, JPG cover image, JSON metadata, SRT subtitles, MP3 voiceover, and Markdown script files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated per detected chapter or episode and written to local batch output directories.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
