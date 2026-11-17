## Description:

Happy Horse 1.0 generates videos from text prompts, first frames, or reference media, and supports video editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams can use the skill to request generated or edited videos through the Happy Horse 1.0 service, including text-to-video, first-frame-to-video, and reference-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a mismatch between the stated video-generation purpose and login-focused instructions, with medium review confidence.

Mitigation: Review the install steps and API-key setup against the intended video-generation workflow before running the CLI.

Risk: The scanner could not inspect some referenced package or local-path details, leaving the evidence incomplete.

Mitigation: Confirm the pinned @dlazy/cli package details and how input media is handled before use.

## Reference(s):

- [dLazy service website](https://dlazy.com)
- [dLazy CLI project page (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package listing](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [Generated video assets returned as hosted URLs, with JSON result and task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration, resolution, aspect ratio, and generation mode are configurable; results can optionally be saved locally.]

## Skill Version(s):

1.3.42 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
