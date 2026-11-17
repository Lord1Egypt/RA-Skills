## Description:

Analyze error messages and logs to identify root causes of crashes, build failures, or runtime errors and suggest actionable fixes with code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze pasted errors, stack traces, build logs, and runtime failures, identify likely root causes, and receive actionable fixes with code snippets or commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted logs can contain secrets or sensitive operational details.

Mitigation: Review and redact logs before sharing them with any agent or running the local parser.

Risk: Diagnosis output can suggest an incorrect fix or command for the user's environment.

Mitigation: Review proposed changes and test them in a controlled environment before applying them to production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/error-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, shell commands, and optional JSON from the parser script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured stack trace fields such as error type, message, frames, and suggested search queries when using the parser script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
