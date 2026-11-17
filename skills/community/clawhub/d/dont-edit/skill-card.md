## Description:

Invoked ONLY by the user with /dont-edit when they want read-only mode activated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need a read-only advisory mode for codebase inspection, external research, and proposed changes that require explicit approval before file mutation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only behavior is an instruction-layer safeguard and cannot replace review of proposed changes.

Mitigation: Verify proposed changes before approving any edit or file mutation.

## Reference(s):

- [Server-resolved source repository](https://github.com/TobiasWestholm/dont-edit)
- [ClawHub skill page](https://clawhub.ai/tobiaswestholm/skills/dont-edit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance for read-only agent behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-layer safeguard; no file mutations are allowed unless explicitly approved.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
