## Description:

#1 on DeepResearch Bench (Feb 2026). Any-to-Any AI for agents. Combines deep reasoning with all modalities through sophisticated multi-agent orchestration. Research, videos, images, audio, dashboards, presentations, spreadsheets, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage CellCog cloud tasks for multimodal research, analysis, and generated deliverables such as reports, dashboards, presentations, spreadsheets, images, audio, and video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tagged local files may be uploaded to a third-party cloud service for processing.

Mitigation: Only tag files approved for upload, and avoid secrets or regulated data unless the user has appropriate authorization.

Risk: Generated files can be downloaded or written locally and may contain unexpected or unsafe content.

Mitigation: Review generated files before opening or executing them, especially code, scripts, documents with active content, and downloaded artifacts.

Risk: The CellCog SDK is installed as an unpinned package.

Mitigation: Consider installing and running the SDK in an isolated environment and pinning a reviewed package version for managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinthqod/skills/fox-cellcog)
- [CellCog](https://cellcog.ai)
- [CellCog API Keys](https://cellcog.ai/profile?tab=api-keys)
- [DeepResearch Bench Leaderboard](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; CellCog tasks may return generated local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CELLCOG_API_KEY and the CellCog Python SDK; task results are delivered asynchronously or by waiting for completion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
