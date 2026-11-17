## Description:

Guides agents through systematic root-cause analysis for tool errors, unexpected results, repeated failures, and explicit debugging requests using a catalog of RCA methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maochen1980](https://clawhub.ai/user/maochen1980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure debugging work, select root-cause analysis methods, record a focused investigation plan, and verify whether a reported error or unexpected behavior has been resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic plans and findings may be written to a predictable temporary file in shared or sensitive environments.

Mitigation: Avoid writing secrets or sensitive data into debugging notes, review the temporary file contents, and clear the file after the investigation when appropriate.

Risk: Unresolved investigations may direct the agent toward loading an external skill manager for self-updates.

Mitigation: Require explicit user approval before invoking any external manager or modifying installed skills.

## Reference(s):

- [RCA Methods Reference](references/rca-methods.md)
- [Debug Root Cause on ClawHub](https://clawhub.ai/maochen1980/skills/debug-root-cause)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with investigation steps and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the problem definition, selected method, plan, and findings to a temporary Markdown file during use.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
