## Description:

Generates videos with Seedance 2.0 from text prompts, multimodal references, or first and last frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to generate short videos from text prompts, reference images, video or audio, or specified opening and closing frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial: the CLI package and some referenced paths were not inspected, and a possible hidden-text warning remains unresolved.

Mitigation: Review the pinned CLI package and relevant references before installing; the scan did not conclusively clear the disputed warning.

Risk: Prompts and supplied local image, video, or audio files are sent to dLazy-hosted services for generation.

Mitigation: Avoid submitting sensitive media or prompts unless you are authorized to share them with the service.

## Reference(s):

- [dLazy service homepage](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [JSON response with generated video URL(s)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is hosted by the dLazy service.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata; artifact frontmatter lists 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
