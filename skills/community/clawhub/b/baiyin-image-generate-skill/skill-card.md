## Description:

Generates images through the Baiyin open platform from text prompts or public reference-image URLs, and can check task status and return result links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure Baiyin image-generation requests, create text-to-image or reference-image tasks, poll task status, and return final image links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Baiyin/Hikoon services with a Baiyin API key and may upload reference images to that external service.

Mitigation: Install only when users intend to use Baiyin/Hikoon services, provide only approved API keys, and avoid private paths or attachments unless upload is intended.

Risk: The server security summary flags a hidden self-update behavior as the main concern.

Mitigation: Handle version updates through a trusted package manager or explicit administrator approval before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiuping520/skills/baiyin-image-generate-skill)
- [Baiyin/Hikoon Service Endpoint](https://ai.hikoon.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown or concise text with task IDs, status values, progress, and image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and uses fixed model, resolution, aspect-ratio, and reference-image URL parameters.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
