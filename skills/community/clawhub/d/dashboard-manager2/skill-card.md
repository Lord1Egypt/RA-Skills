## Description:

Dashboard Manager2 lets an agent read and update a local Jarvis dashboard, including notes, tasks, logs, documents, automation rules, and system status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philippeh5](https://clawhub.ai/user/philippeh5)

### License/Terms of Use:

MIT

## Use Case:

Developers and Jarvis dashboard operators use this skill to synchronize a local dashboard with agent activity, including pending notes, task status, logs, documents, automation rules, and system status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate a local dashboard service, including documents, automation rules, tasks, notes, logs, and system status.

Mitigation: Install only in a trusted local Jarvis dashboard environment and review the exported actions before granting access.

Risk: The documentation and manifests do not fully disclose the localhost API authority observed in the executable artifact.

Mitigation: Require updated documentation and manifests that clearly describe localhost:8009 access, mutation scope, and destructive actions.

Risk: Document deletion and automation rule changes can cause data loss or unexpected automated behavior.

Mitigation: Add user confirmation or clear operator controls for destructive actions, validate identifiers, and check API failures.

## Reference(s):

- [Artifact skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/philippeh5/skills/dashboard-manager2)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance]

**Output Format:** [JavaScript functions and localhost dashboard API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates against a local dashboard service at localhost:8009 and can mutate dashboard records.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact manifest, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
