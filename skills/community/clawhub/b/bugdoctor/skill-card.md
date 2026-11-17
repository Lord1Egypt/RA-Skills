## Description:

Diagnoses software failures from local evidence and relevant research, recommends supported remedies, and performs scoped repairs when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redrookai](https://clawhub.ai/user/redrookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use BugDoctor to investigate software errors, regressions, and recurring failures, identify an evidence-backed cause and remedy, and verify repairs they authorize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive information in logs or errors could be exposed through public searches.

Mitigation: Remove credentials, private payloads, and personal details before searching publicly.

Risk: An incorrect repair could change project behavior or disrupt completed work.

Mitigation: Authorize only scoped edits, preserve existing work, and verify the reported failure and affected behavior.

## Reference(s):

- [BugDoctor on ClawHub](https://clawhub.ai/redrookai/skills/bugdoctor)
- [BugDoctor research and documentation references](REFERENCES.md)
- [BugDoctor runtime guidance](references/runtime.md)
- [BugDoctor timing and concurrency guidance](references/timing.md)
- [BugDoctor agent workflow guidance](references/trajectories.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Natural-language diagnosis and recommendations, with code changes or commands when authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports supporting evidence and repair verification where available.]

## Skill Version(s):

0.1.0 (source: ClawHub release and README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
