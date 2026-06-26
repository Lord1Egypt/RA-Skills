## Description: <br>
Generates AI videos through AceDataCloud's Kuaishou Kling API for text-to-video, image-to-video, video extension, and motion-control workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to have an agent produce practical guidance and request examples for generating Kling videos through AceDataCloud, including text-to-video, image-to-video, video extension, motion control, and task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, task data, and callback URLs are sent to AceDataCloud/Kling. <br>
Mitigation: Use only provider-approved data and avoid sensitive, regulated, private, or internal-only URLs unless the organization has approved the provider. <br>
Risk: The skill requires an ACEDATACLOUD_API_TOKEN for API access. <br>
Mitigation: Store the token in a protected environment or secrets manager and do not commit, log, or share it. <br>


## Reference(s): <br>
- [Kling Video on ClawHub](https://clawhub.ai/Germey/acedatacloud-kling-video) <br>
- [AceDataCloud Kling video API endpoint](https://api.acedata.cloud/kling/videos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN and sends generation prompts, media URLs, task data, and optional callback URLs to AceDataCloud/Kling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
