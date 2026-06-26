## Description: <br>
Generate AI videos with Hailuo (MiniMax) via AceDataCloud API from text descriptions or source images, including image-to-video director mode for finer motion control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate Hailuo videos from prompts or animate still images through AceDataCloud's API. It is useful when an agent needs to provide request guidance, curl commands, parameter choices, or polling steps for video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, source image URLs, and callback URLs are sent to AceDataCloud/Hailuo. <br>
Mitigation: Avoid secrets, private internal URLs, proprietary images, regulated data, or unapproved callback targets unless the provider, retention, and billing terms have been reviewed. <br>
Risk: The skill requires an AceDataCloud API token for authenticated requests. <br>
Mitigation: Store ACEDATACLOUD_API_TOKEN in the runtime environment and do not place the token in prompts, generated examples, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Germey/acedatacloud-hailuo-video) <br>
- [AceDataCloud Hailuo videos API endpoint](https://api.acedata.cloud/hailuo/videos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include request parameters, model choices, authentication setup, and task polling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
