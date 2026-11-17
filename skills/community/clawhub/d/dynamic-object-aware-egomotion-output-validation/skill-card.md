## Description:

Local self-check of instructions and mask outputs (format/range/consistency) without using GT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after generating interval instructions, masks, or similar outputs to check local file format, frame coverage, CSR structure, and value consistency before submission or hand-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference snippet reads local video, JSON, and NPZ files that may be large or sensitive.

Mitigation: Review the referenced paths before running validation and apply it only to intended local output artifacts.

Risk: The checks validate format, ranges, frame coverage, and CSR structure, but they do not establish semantic correctness against ground truth.

Mitigation: Use this as a pre-submission sanity check and pair it with task-specific review or evaluation when correctness matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/dynamic-object-aware-egomotion-output-validation)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local validation guidance for JSON interval instructions and NPZ CSR masks; no ground-truth comparison is included.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
