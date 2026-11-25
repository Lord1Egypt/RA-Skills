## Description:

PixVerse C1 generates videos from text prompts, images, first and last frames, and reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can generate PixVerse C1 videos from text prompts, reference images, or first and last frames, with controls for duration, resolution, aspect ratio, and optional audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The medium-confidence, partial security review flagged a login behavior whose connection to the advertised video-generation purpose is unclear.

Mitigation: Before installing, confirm that the dLazy login flow and pinned CLI package are expected, and review the installation and authentication details.

Risk: Prompts and supplied local media are sent to dLazy hosted services for generation.

Mitigation: Avoid providing sensitive prompts or media unless their use with the hosted service is approved.

## Reference(s):

- [dLazy service](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video files, JSON]

**Output Format:** [JSON response containing generated video asset URLs or asynchronous task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated asset URLs are hosted by dLazy; asynchronous tasks may return a generation ID.]

## Skill Version(s):

1.2.45 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
