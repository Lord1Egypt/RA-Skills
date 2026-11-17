## Description:

Builds reproducible evaluation cases for agents, models, and skills from capability specifications and boundary examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation teams use this skill to turn capability specifications and edge cases into repeatable test cases with expected results and judging criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unspecified input specification or output path can produce an unintended benchmark file.

Mitigation: Choose the input specification and output JSONL path explicitly before running the generator.

Risk: Generated expectations or judging criteria may not reflect the intended behavior.

Mitigation: Review generated cases before using them in regression tests, and clarify ambiguous evaluation requests before creating files.

## Reference(s):

- [Eval Bench Builder on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/eval-bench-builder)
- [LGD theory reference](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSONL files]

**Output Format:** [JSONL benchmark cases with Markdown guidance and a command for local generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each case has capability, input, expected result, and judging criteria.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
