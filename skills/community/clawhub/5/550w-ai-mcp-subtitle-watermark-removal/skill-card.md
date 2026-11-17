## Description:

Removes text and watermarks from selected images, removes subtitles and visual watermarks from local videos, and resolves supported share links to watermark-free video URLs through 550W.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinehu](https://clawhub.ai/user/sunshinehu)

### License/Terms of Use:

MIT

## Use Case:

Creators and editors use this skill to remove unwanted text, subtitles, or watermarks from media they are authorized to edit, or to resolve supported video share links. Processing uses a 550W account via OAuth or an API key and may consume credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, share links, and necessary account credentials are sent to 550W for processing.

Mitigation: Only submit media the user explicitly selected and is authorized to edit; confirm the user accepts transmission to 550W before processing.

Risk: Stored account credentials may be exposed on shared systems.

Mitigation: Prefer OAuth or host-managed credentials and require explicit consent before saving credentials.

Risk: Processing may charge credits, and task deletion removes a selected task.

Mitigation: Review credit charges before processing and separately confirm the exact task before deletion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sunshinehu/skills/550w-ai-mcp-subtitle-watermark-removal)
- [OAuth access workflow](references/oauth-access.md)
- [API key access workflow](references/openapi-access.md)
- [550W Open API contract](references/api-contract.md)
- [Agent compatibility](references/agent-compatibility.md)
- [550W API documentation and credentials](https://eraser.550wai.com/api/)

## Skill Output:

**Output Type(s):** [Text, Result links, Guidance]

**Output Format:** [Markdown with task status and result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media processing may require credits; share-link resolution does not guarantee that the agent downloaded the video.]

## Skill Version(s):

3.1.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
