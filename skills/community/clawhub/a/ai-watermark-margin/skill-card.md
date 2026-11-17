## Description:

Prepare images you generated or edited with AI for removal of the editor's visual stamp by adding a blank margin before editing and cropping it afterward; this does not remove third-party rights watermarks, and AI use should still be disclosed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Image editors and creators use this skill to keep an AI generator's visual stamp out of images they generated or edited themselves: they add a blank margin before editing, then crop that margin from the result. They remain responsible for disclosing AI use and should not use the technique to remove rights watermarks from other people's work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --fallback crop can exceed the stated --max-percent limit and remove more image content than intended.

Mitigation: Keep originals, save results under different filenames, and preview cropping with --report. Do not rely on --max-percent to constrain --fallback.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/catsmansion/skills/ai-watermark-margin)
- [Publisher profile](https://clawhub.ai/user/catsmansion)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files]

**Output Format:** [Python scripts with command-line instructions; edited image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic image padding and border cropping; output depends on the supplied image and command-line options.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
