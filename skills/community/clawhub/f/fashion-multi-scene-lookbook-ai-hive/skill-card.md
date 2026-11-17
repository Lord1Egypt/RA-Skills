## Description:

This skill helps fashion brands, boutiques, designers, and social content teams plan multi-scene lookbook sets for the same garment and optionally generate reviewed AI-HIVE image assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External fashion brands, boutiques, designers, and social media content teams use this skill to turn garment images, audience, season, scenes, aspect ratio, and brand constraints into a reviewed lookbook workflow, prompts, runnable commands, and delivery checklist. It is intended for authorized commercial content production where the garment remains fixed while scenes, poses, and styling vary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API client can send the user's API key to a configured API server, including a custom or untrusted base URL.

Mitigation: Review AI_HIVE_BASE_URL, ~/.ai-hive/config.json, prompts, routing, batch size, uploads, and downloads before submitting any generation task; use only an AI-HIVE key suitable for billable media generation.

Risk: Generated fashion lookbook content may overstate product facts, alter garment details, or imply unauthorized endorsement.

Mitigation: Confirm source material rights and manually review garment structure, color, logos, claims, task records, and platform-specific acceptance criteria before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/fashion-multi-scene-lookbook-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose billable AI-HIVE generation only after user review; generated assets can be downloaded to local files when API tasks complete.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
