## Description:

Provides a hosted runtime for generating and editing images, video, audio, and 3D assets through a single agent-facing workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or edit image, video, audio, and 3D media through Luxin, then retrieve hosted results and job details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting feedback may expose private prompts, URLs, paths, or secrets if submitted without review.

Mitigation: Require user approval before submitting feedback and remove private prompts, URLs, paths, and secrets.

Risk: The external executable and hosted service implementations were not audited, and media inputs and results use Luxin hosting.

Mitigation: Review the executable and hosted service before sending sensitive content; consider pinned dependency versions and workspace-scoped installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielgwilson/skills/creative-media)
- [Luxin homepage](https://luxin.sh)
- [Luxin LLM contract](https://luxin.sh/llms.txt)
- [Luxin skill guide](https://luxin.sh/skill.md)
- [Luxin hosted API](https://api.luxin.sh)

## Skill Output:

**Output Type(s):** [Images, Video, Audio, 3D assets, JSON, Shell commands]

**Output Format:** [Hosted media URLs with structured job and cost metadata, plus CLI commands and Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include recoverable job IDs and cost receipts; inputs and results use Luxin hosting.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
