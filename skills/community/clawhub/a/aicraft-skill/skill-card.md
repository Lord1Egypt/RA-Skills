## Description:

爱创AI helps ecommerce users generate and manage product images, videos, detail-page images, style replications, and related AI-edited assets through the 51aic service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howerlin0329](https://clawhub.ai/user/howerlin0329)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and agents use this skill to call the 51aic service for product image generation, AI image editing, virtual try-on, product videos, detail-page image generation, style replication, credit checks, and generated asset management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a reusable 51aic account token.

Mitigation: Use only in private sessions, avoid sharing long-lived or broad account tokens, and remove the token from shared transcripts or logs.

Risk: The skill uploads selected product images to external 51aic, fzputi, and OSS service domains.

Mitigation: Confirm which files will be uploaded before API calls and avoid submitting confidential or unauthorized product images.

Risk: The skill can batch-delete platform assets.

Mitigation: Require the agent to show exact asset IDs and obtain final user confirmation before any deletion request.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/howerlin0329/skills/aicraft-skill)
- [51aic platform](https://www.51aic.com?source=agents)
- [51aic token setup](https://www.51aic.com/openclaw?source=agents)
- [Image generation modes](references/image-modes.md)
- [Video generation configuration](references/video-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and Python or PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated asset URLs, thumbnail display links, task IDs, progress/status summaries, and deletion confirmation details.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
