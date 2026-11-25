## Description:

Generates high-quality videos with Kling v3 from text prompts or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short Kling v3 videos from text prompts or reference images through the dLazy CLI and hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security review is benign with medium confidence but flags a purpose mismatch, is partial, and does not demonstrate video-generation behavior.

Mitigation: Review the skill content and any unresolved references before relying on its video-generation claims.

Risk: Prompts and local media supplied to the skill are sent to dLazy hosted services; local media is uploaded for processing.

Mitigation: Avoid submitting confidential prompts or media unless use of the dLazy service is approved.

Risk: The server-resolved release is version 1.3.44, while the supplied artifact frontmatter says 1.3.5.

Mitigation: Confirm the packaged artifact matches the intended release before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-kling-v3)
- [dLazy CLI project repository (project link; release provenance unavailable)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video assets, JSON, Shell commands, Guidance]

**Output Format:** [JSON result with hosted output URLs; optionally saved media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation may return a completed result or an asynchronous task identifier; supports an optional local save path.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
