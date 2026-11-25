## Description:

Fast version of ByteDance's Seedance 2.0 for generating videos from text and multimodal references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate Seedance 2.0 Fast videos from text prompts, optional image, video, or audio references, or first and last frame images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and incomplete coverage; the reviewed login operation does not establish the advertised video-generation behavior.

Mitigation: Review the CLI behavior before installation and verify it with a small, non-sensitive generation request before relying on it.

Risk: Prompts and local reference media are sent to dLazy's hosted API and media storage.

Mitigation: Avoid submitting confidential or personally identifying content unless your organization permits sending it to these services.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dlazyai/skills/dlazy-seedance-2-0-fast)

## Skill Output:

**Output Type(s):** [Media assets, JSON result metadata, Shell commands]

**Output Format:** [Hosted media URLs or saved assets, with JSON task status and result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can run asynchronously; use the returned task ID to check status.]

## Skill Version(s):

1.3.43 (source: server-resolved release metadata; skill frontmatter states 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
