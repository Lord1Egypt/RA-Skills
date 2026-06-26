## Description: <br>
AI-powered video generator using XLXAI Sora2 API. Create professional videos from text prompts or images in seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yefl2064](https://clawhub.ai/user/yefl2064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and automation developers use this skill to generate short videos from text prompts or image inputs through the XLXAI Sora2 API. It returns task and result JSON, including a video URL when generation completes, without publishing to social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and generated video outputs are sent to XLXAI or its hosting/CDN. <br>
Mitigation: Use the skill only when external processing is acceptable, avoid sensitive or regulated images, and review generated outputs before use. <br>
Risk: The skill requires an XLXAI API key. <br>
Mitigation: Provide the key through the XLXAI_API_KEY environment variable and prefer a dedicated key with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yefl2064/auto-video-creator) <br>
- [XLXAI API endpoint](https://api.xlxai.store) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Guidance] <br>
**Output Format:** [JSON task/result data with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XLXAI_API_KEY; can return immediately with a task ID or poll until a generated video URL is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
