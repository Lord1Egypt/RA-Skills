## Description:

Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matttgx](https://clawhub.ai/user/matttgx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate sustained multi-agent workflows with assigned roles, shared artifacts, task state transitions, handoffs, and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unclear permissions, schedules, timezones, or shared directory boundaries can make multi-agent workflows difficult to audit or control.

Mitigation: Define schedules, timezones, agent permissions, shared workspace boundaries, and approval rules before using the skill for real workflows.

Risk: Skipping handoffs, artifact paths, or independent review can create lost work and quality drift.

Mitigation: Require explicit output paths, handoff summaries, verification steps, known-issue notes, and at least one review before marking work done.

## Reference(s):

- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with role definitions, task templates, handoff checklists, review protocols, and example verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no code execution or API calls are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
