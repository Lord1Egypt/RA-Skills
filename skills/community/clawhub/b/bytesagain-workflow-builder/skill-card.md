## Description:

Create and run multi-step shell workflows with status tracking for repeatable local automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define, execute, inspect, list, and export multi-step shell workflows such as local CI, build, and deployment sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved workflow steps execute shell commands under the user's account.

Mitigation: Review every workflow step before running it and avoid workflows from untrusted sources.

Risk: Weak scoping and no clear safety gate can make accidental or unintended command execution more likely.

Mitigation: Run only in directories and environments that do not contain sensitive credentials unless workflow ID validation and execution confirmation are added.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-workflow-builder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal-oriented text and JSON workflow definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates workflow JSON files under the user's home directory and records command status and truncated command output.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
