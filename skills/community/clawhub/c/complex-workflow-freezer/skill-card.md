## Description:

Freezes completed complex workflow findings, decisions, and execution paths into stable reusable skill specifications with checksum validation, threshold locking, and optional multimodal handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow engineers use this skill to preserve finalized workflow state as a reusable skill artifact. It is suited for workflows where repeatable decisions, checksums, fixed thresholds, saved execution paths, and optional image-related branches need to stay consistent across later agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling can overwrite files outside the intended output directory.

Mitigation: Use only a dedicated output directory and validate workflow_id and output_path values before execution.

Risk: Progress forwarding over webchat or Telegram can disclose workflow status or identifiers.

Mitigation: Enable webchat or Telegram progress forwarding only when that disclosure is acceptable for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/complex-workflow-freezer)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, Python API output, and generated skill specification files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a skill identifier, saved specification path, multimodal layer status, and capability check status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
