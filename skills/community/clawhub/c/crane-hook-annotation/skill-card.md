## Description:

Detect and tightly annotate tower-crane hook outlines in similar construction-site monitoring images. Use when Codex needs to batch-process `.png`, `.jpg`, or `.jpeg` images from a stable camera view, locate the hook from bright metal pixels inside a known search region, export annotated copies, and produce reusable coordinates or polygon metadata for follow-up QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genlk](https://clawhub.ai/user/genlk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site-monitoring teams use this skill to batch-process construction-site images from a stable camera view, outline crane hooks with a strict polygon, and export annotated images plus coordinate metadata for QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented annotation command references a missing PowerShell script, so the executable behavior cannot be verified from the artifact.

Mitigation: Supply the script from a trusted source and review it before installation or execution.

Risk: The quick-start commands bypass PowerShell execution policy.

Mitigation: Prefer commands that do not bypass execution policy, and run only reviewed scripts.

Risk: Batch processing could run against unintended image folders or output locations.

Mitigation: Run first on a sample image, then use explicit input and output paths for the intended image set.

## Reference(s):

- [Profile Tuning](references/profile-tuning.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with PowerShell commands; annotated image files and manifest JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include annotated images, optional debug ROI crops, and a manifest with bounding boxes, polygon points, and status records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
