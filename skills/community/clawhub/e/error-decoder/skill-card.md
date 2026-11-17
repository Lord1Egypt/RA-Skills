## Description:

Decode an error message or stack trace into a plain-English cause, the exact fix, and how to prevent it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn error messages, stack traces, and crash output into a structured diagnosis with the meaning, likely cause, concrete fix, and prevention step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnoses based on partial traces or isolated error strings may be incomplete or wrong.

Mitigation: Treat the diagnosis as a hypothesis, label assumptions, and confirm against the relevant code, runtime, and full stack trace when available.

Risk: Applying suggested fixes directly to important code could introduce regressions.

Mitigation: Review proposed changes and verify them with tests or a safe reproduction before applying them to production code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/error-decoder)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/error-decoder.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown structured diagnosis with optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumptions about missing language or runtime context should be labeled for user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
