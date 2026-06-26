## Description: <br>
AI-powered video highlight extraction that identifies engaging moments and generates social-ready video clips with configurable export options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wayinvideo](https://clawhub.ai/user/wayinvideo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to turn online video URLs or local video files into highlight clips for social media, reels, and long-to-short repurposing. Developers and operators use it through WayinVideo API scripts that submit jobs, poll for results, and return downloadable clip links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos, source URLs, or uploaded local files may be sent to WayinVideo for processing. <br>
Mitigation: Use the skill only with content the user is authorized to send to WayinVideo, and avoid sensitive or private media unless that sharing is acceptable. <br>
Risk: Generated JSON result files and temporary export links are saved locally and may expose clip data while accessible. <br>
Mitigation: Store result files privately, avoid posting export links publicly, and refresh or regenerate links only when needed. <br>
Risk: The skill requires a WayinVideo API credential. <br>
Mitigation: Provide WAYIN_API_KEY through an environment variable or secure user context, and do not write it into prompts, files, or logs. <br>
Risk: Optional progress system events can create background notifications during long polling jobs. <br>
Mitigation: Do not enable progress events when background notifications are not desired. <br>


## Reference(s): <br>
- [WayinVideo AI Clipping API documentation](https://wayin.ai/api-docs/ai-clipping/) <br>
- [ClawHub skill page](https://clawhub.ai/wayinvideo/ai-clipping) <br>
- [Supported languages](assets/supported_languages.md) <br>
- [Platform duration guidance](assets/platform_duration.md) <br>
- [Platform aspect ratio guidance](assets/platform_ratio.md) <br>
- [Caption style templates](assets/caption_style.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown response with shell commands, result file paths, JSON artifacts, and downloadable clip links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WAYIN_API_KEY; API polling can take several minutes; exported clip links are temporary.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
