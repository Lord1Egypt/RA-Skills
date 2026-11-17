## Description:

Baiyin Music Generate helps an agent create, adapt, and track AI music generation tasks through the Baiyin Open Platform, including reference-audio workflows, result retrieval, and quota checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting music creators or application users can use this skill to turn natural-language song requests into Baiyin music generation, reference-audio generation, or cover/adaptation tasks. It also supports checking task status, returning generated media links, and checking account quota when a Baiyin API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact instructs silent, unverified self-updates before normal use, which could change reviewed behavior without user approval.

Mitigation: Remove or disable the self-update behavior, or replace it with an explicit user-approved update flow that verifies integrity and requires rescanning before deployment.

Risk: The skill contacts Baiyin services and uses a Baiyin API key for music generation and account checks.

Mitigation: Use scoped and rotated API keys where possible, approve external network access before use, and avoid sending sensitive or private audio unless the deployment policy permits it.

## Reference(s):

- [Baiyin Open Platform](https://ai.hikoon.com)
- [ClawHub Skill Page](https://clawhub.ai/jiuping520/skills/baiyin-music-generate)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown responses with JSON request bodies, API status summaries, and result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated audio, video, and cover-image links returned by Baiyin; requires a Baiyin API key for live API use.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
