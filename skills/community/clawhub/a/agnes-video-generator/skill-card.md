## Description: <br>
Generates AI videos from text or images using Agnes-Video-V2.0 with customizable frames, resolution, and asynchronous task handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lg0219](https://clawhub.ai/user/lg0219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate videos from text prompts or source image URLs through Agnes-Video-V2.0, with controls for frame count, frame rate, resolution, seed, and negative prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, optional image URLs, and generation settings are sent to Agnes's remote service. <br>
Mitigation: Avoid private image links or sensitive prompt content unless the provider's data handling is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lg0219/skills/agnes-video-generator) <br>
- [Agnes video generation API endpoint](https://apihub.agnes-ai.com/v1/videos) <br>
- [Agnes video status API endpoint](https://apihub.agnes-ai.com/agnesapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text] <br>
**Output Format:** [JSON object containing generation success, video URL, size, duration, video ID, and status fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNES_API_KEY and polls asynchronously until the video completes or times out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
