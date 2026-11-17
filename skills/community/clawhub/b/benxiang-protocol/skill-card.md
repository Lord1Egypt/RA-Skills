## Description:

Benxiang is a persistent object representation layer for AI work that helps agents restore project state, commit semantic transactions, and trace fields through evidence-backed provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist project state across sessions, coordinate multi-agent work, and record decisions, tasks, risks, facts, and module boundaries as semantic transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install steps run unpinned external repository code that was not included in the reviewed artifact.

Mitigation: Review or sandbox the external repository before use, prefer a pinned commit with an independently verified checksum or signature, and run npm scripts in a disposable environment without secrets or broad filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/benxiang-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands and JSON transaction examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer according to package metadata.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
