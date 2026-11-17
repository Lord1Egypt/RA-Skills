## Description:

Generate and work with Fibonacci sequences and related number sequences. Use when users need Fibonacci numbers, calculate Fibonacci sequences, find nth Fibonacci numbers, check Fibonacci properties, or work with golden ratios and related mathematical sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and external users use this skill to generate Fibonacci sequences, calculate nth Fibonacci numbers, check Fibonacci properties, and explain related concepts such as golden ratio approximations, Lucas numbers, Tribonacci, and Fibonacci sums.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause an agent to select the skill for nearby math topics outside Fibonacci and closely related sequences.

Mitigation: Confirm that the user is asking for Fibonacci, golden-ratio, Lucas, Tribonacci, or directly related sequence work before applying the skill.

Risk: Very large requested sequence sizes can consume time or memory because Fibonacci values grow quickly.

Mitigation: Ask for a bounded count or provide an algorithm/formula summary instead of generating excessively long full sequences.

Risk: Generated mathematical explanations or code may be misleading if adapted beyond the simple sequence operations covered by the artifact.

Mitigation: Review formulas and generated code before using them in production, grading, or other high-reliability contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/fibonacci-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Fibonacci sequences, individual values, property checks, formulas, and concise Python examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
