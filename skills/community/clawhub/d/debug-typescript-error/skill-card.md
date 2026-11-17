## Description:

Translate a TypeScript compiler error into plain English, find the smallest type boundary at fault, and prefer the smallest safe fix over suppression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to explain TypeScript compiler errors, identify the smallest type boundary causing the mismatch, propose a minimal safe fix, and provide a concrete typecheck command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Ritual Cloud path asks users to install a third-party global CLI and run initialization commands.

Mitigation: Review @ritualai/cli version, provenance, permissions, and what ritual init may read or write before approving that path.

Risk: Optional knowledge-note creation can persist project facts after a debugging task.

Mitigation: Create notes only with explicit user approval and scope them to reusable, non-sensitive project knowledge.

## Reference(s):

- [Debug Typescript Error on ClawHub](https://clawhub.ai/ritual/skills/debug-typescript-error)
- [Ritual](https://ritual.work)
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an optional, user-approved OKF knowledge note when reusable non-sensitive project knowledge is discovered.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
