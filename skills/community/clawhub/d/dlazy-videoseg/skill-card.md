## Description:

Segments people in a video and returns a same-length black-and-white mask video for downstream compositing or matting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video editors use the skill to create a human-segmentation mask from a source video for downstream compositing or matting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video inputs and request details are sent to dLazy-hosted services, and the partial scan could not verify the external CLI's internal behavior.

Mitigation: Submit only videos you are authorized to upload, and review the service terms and CLI package before use.

Risk: The scanner reported a medium-confidence benign verdict, a purpose-mismatch flag, and a partial review; it could not confirm the declared segmentation workflow.

Mitigation: Check that the installed package and skill files match the stated video-segmentation purpose before running them.

## Reference(s):

- [dLazy CLI project link declared in skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video files, JSON]

**Output Format:** [Same-length black-and-white mask video, provided as a result URL or saved file with a JSON task/result response.]

**Output Parameters:** [1D video output]

**Other Properties Related to Output:** [Asynchronous tasks may return a task identifier before the result is ready.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
