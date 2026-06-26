## Description: <br>
Finds specific moments in online or local videos from a natural-language query and can export matching clips with aspect ratio, caption, hook, and reframing options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wayinvideo](https://clawhub.ai/user/wayinvideo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to locate specific scenes, topics, or events in long videos and optionally export matched clips with captions, hooks, and platform-specific aspect ratios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local videos, online video URLs, natural-language queries, and processing settings to WayinVideo. <br>
Mitigation: Use only with media and prompts that are appropriate for WayinVideo processing, and avoid private, regulated, or confidential content unless WayinVideo handling and retention terms have been reviewed. <br>
Risk: Task metadata and API responses are stored locally in JSON result files. <br>
Mitigation: Store results in an approved workspace path, review saved files for sensitive metadata or clip links, and delete them when no longer needed. <br>
Risk: The skill depends on a WayinVideo API key and external API availability. <br>
Mitigation: Provide WAYIN_API_KEY only through the environment or approved secret handling, and expect tasks to fail or remain incomplete if the external service is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wayinvideo/find-moments-in-the-video) <br>
- [WayinVideo publisher profile](https://clawhub.ai/user/wayinvideo) <br>
- [WayinVideo Find Moments API documentation](https://wayin.ai/api-docs/find-moments/) <br>
- [WayinVideo API dashboard](https://wayin.ai/wayinvideo/api-dashboard) <br>
- [Supported languages reference](artifact/assets/supported_languages.md) <br>
- [Platform aspect ratio reference](artifact/assets/platform_ratio.md) <br>
- [Caption style reference](artifact/assets/caption_style.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON files, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets and saved JSON result files containing task metadata, API responses, matching moments, and clip links when export is enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WAYIN_API_KEY. Export links are described by the artifact as valid for 24 hours, and project results as expiring after 3 days.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
