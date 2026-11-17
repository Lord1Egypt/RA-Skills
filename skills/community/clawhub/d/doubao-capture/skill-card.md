## Description:

Capture Doubao translation results with auto-scroll and auto-end detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and workflow operators use this skill to capture Doubao translated subtitles from a Windows GUI session and save captured text with run metadata for a YouTube translation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin entrypoint points to an external Python file that is not included in the reviewed package.

Mitigation: Review before installing and avoid this version unless you control and have audited the referenced /mnt/h/... script path.

Risk: Windows GUI automation requires a visible desktop session and can fail when the desktop is disconnected.

Mitigation: Run the skill only in an active Windows desktop session and confirm the Doubao window handle and output directory before capture.

## Reference(s):

- [Doubao Capture ClawHub listing](https://clawhub.ai/banner90/skills/doubao-capture)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON status object with captured subtitle text written to a text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a visible Windows desktop session and a Doubao window handle.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
