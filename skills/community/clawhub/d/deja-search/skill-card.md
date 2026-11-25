## Description:

Search a user's past AI coding sessions with the deja CLI to recover prior decisions, conventions, and troubleshooting context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshulcz](https://clawhub.ai/user/vshulcz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use the skill to search prior AI coding sessions for decisions, conventions, and earlier troubleshooting context while working on a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may download and run an unpinned deja package automatically.

Mitigation: Review and trust the package source, and decide whether automatic unpinned execution is acceptable before using it.

Risk: The workflow can affect broad agent activation and make persistent rule changes.

Mitigation: Review rule changes and any cross-agent synchronization before applying them.

## Reference(s):

- [Memory for OpenClaw](https://vshulcz.github.io/deja-vu/guide/memory-for-openclaw.html)
- [deja-search on ClawHub](https://clawhub.ai/vshulcz/skills/deja-search)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Text guidance with deja CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include information retrieved from the user's local AI coding session history.]

## Skill Version(s):

0.25.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
