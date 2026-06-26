## Description: <br>
Calls the RawUGC API to generate AI videos, images, and music, manage creative assets, schedule social media posts, research TikTok content, and analyze viral videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tfcbot](https://clawhub.ai/user/tfcbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call RawUGC endpoints for media generation, content management, TikTok research, viral video analysis, and social post scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that publish or schedule social media posts, disconnect social accounts, delete resources, spend credits, or upload media that may become publicly accessible. <br>
Mitigation: Use a dedicated RawUGC API key when possible, avoid sensitive uploads unless public access is acceptable, and require explicit confirmation before destructive, publishing, account, or credit-spending actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tfcbot/ai-ugc) <br>
- [Project homepage](https://github.com/tfcbot/rawugc-skills) <br>
- [RawUGC API base URL](https://rawugc.com/api/v1) <br>
- [Request/response reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAWUGC_API_KEY and uses RawUGC-Version 2026-03-06.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
