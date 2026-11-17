## Description:

Professional assistant for 3D printing, laser engraving, and 3D modeling workflows. Supports generating visual references for sculpting (Forger/ZBrush), creating 3D models via Meshy AI, and optimizing FDM/Resin print settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaulustus](https://clawhub.ai/user/jaulustus)

### License/Terms of Use:

MIT-0

## Use Case:

External makers, developers, and fabrication teams use this skill to plan 3D modeling, Meshy-assisted asset generation, 3D printing, slicer preparation, and laser engraving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local API key storage can expose Meshy credentials if a generated .env file is shared or committed.

Mitigation: Set MESHY_API_KEY through the environment or a secret manager, avoid the set-key helper for persistent storage, and exclude any .env file from sharing and source control.

Risk: Prompts and image URLs submitted through the helper are sent to Meshy.

Mitigation: Review prompts and image URLs before submission and avoid sending confidential, proprietary, or personal data unless approved for that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaulustus/skills/3d-maker-companion)
- [Publisher profile](https://clawhub.ai/user/jaulustus)
- [Meshy API v1 endpoint](https://api.meshy.ai/openapi/v1)
- [Meshy API v2 endpoint](https://api.meshy.ai/openapi/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and JSON responses from helper API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require MESHY_API_KEY for Meshy API helper workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
