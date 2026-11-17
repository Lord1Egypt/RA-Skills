## Description:

Tests OpenClaw performance across 205 real-world scenarios and compares results against the ClawBrain v1.0 orchestration engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to benchmark agent behavior across file operations, search, terminal work, messaging, multi-step tasks, error recovery, ambiguous instructions, and vision understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is described as a benchmark that may involve terminal commands, file edits, web fetching, and messaging tests.

Mitigation: Review the skill before installing and run benchmark activity only in a disposable or clearly bounded environment.

Risk: Messaging and file-operation tests could affect external recipients or local workspace content if executed with broad permissions.

Mitigation: Limit credentials, confirm outbound messaging targets, and restrict file-system access before running tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelfeng/skills/clawbrain-pro-benchmark)
- [OpenClaw model comparison report](https://clawbrain.dev/blog/openclaw-model-comparison)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text benchmark guidance and results, potentially with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl according to ClawHub metadata.]

## Skill Version(s):

1.0.2 (source: server release evidence; target metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
