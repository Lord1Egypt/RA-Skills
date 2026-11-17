## Description:

Calls the VolcEngine Seedance video generation API for text-to-video, image-to-video, and first/last-frame video creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lamuier](https://clawhub.ai/user/lamuier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate videos through VolcEngine Seedance from text prompts, image URLs, or first/last-frame inputs, then retrieve the generated video URL and optional local MP4 file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image URLs are sent to VolcEngine Seedance.

Mitigation: Avoid sensitive prompts or private image URLs unless this is permitted by your data policy.

Risk: The skill depends on VOLCENGINE_API_KEY for authenticated API access.

Mitigation: Keep the API key in environment configuration and avoid committing or exposing it in shared logs.

Risk: Generated video downloads depend on remote URLs returned by the service.

Mitigation: Consider adding request timeouts, bounded streaming, and video URL validation before shared or production use.

## Reference(s):

- [ClawHub release page for doubao-seedance-skill](https://clawhub.ai/lamuier/skills/doubao-seedance-skill)
- [VolcEngine Seedance task API endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions]

**Output Format:** [Terminal text and structured Python dictionary values with generated video URLs and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_API_KEY and may save generated MP4 files to a local output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
