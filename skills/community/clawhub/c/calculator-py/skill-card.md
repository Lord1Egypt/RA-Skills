## Description:

A local Python calculator skill that lets agents run numerical, matrix, statistics, arbitrary-precision, optimization, integration, and signal-processing computations with numpy, scipy, and mpmath.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an agent needs reliable local mathematical computation instead of estimating results in text. It is suited for scripted arithmetic, matrices, statistics, arbitrary precision, optimization, integration, and signal-processing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted math expressions can execute local commands.

Mitigation: Use only in a tightly isolated environment, do not pass expressions from untrusted prompts or documents, and replace unsafe eval behavior with a restricted math parser before normal agent use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardo-lb/skills/calculator-py)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with stdout results and stderr errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are grouped under a subcommand header; successful commands exit 0 and failures return nonzero exit codes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
