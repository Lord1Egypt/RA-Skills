## Description:

A skill for main agents that need bounded delegation, safe parallel dispatch, and independent acceptance across multiple specialists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjke84](https://clawhub.ai/user/cjke84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when to keep work local, when to delegate to sub-agents, and how to issue bounded task contracts. It helps the main agent coordinate parallel work, verify returned outputs, recover from failed delegation, and synthesize one final response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A main agent may route work to unapproved, unavailable, or poorly matched sub-agents.

Mitigation: Review the allowed sub-agent list, routing keywords, and any configured agent registry before enabling the skill in a shared workspace.

Risk: Parallel delegation can create file collisions, hidden dependencies, or difficult integration work.

Mitigation: Use parallel dispatch only for independent tasks with disjoint write scopes, explicit task contracts, and a concurrency limit that matches the local runtime.

Risk: Sub-agent results may be incomplete, out of scope, or accepted without evidence.

Mitigation: Require main-agent acceptance checks for scope, expected output, verification evidence, and cross-agent consistency before synthesis.

Risk: Persisted memory or resume state can influence future orchestration behavior in mixed-language or shared workspaces.

Mitigation: Review MEMORY.md, resume-state files, and recovery metadata before relying on replay or continuing delegated work.

## Reference(s):

- [Routing Configuration Template](references/routing-template.md)
- [OpenClaw Local Playbook](references/openclaw-playbook.md)
- [Task Contract Template](references/task-contract-template.md)
- [Task Decomposition Template](references/taREDACTED-SECRET.md)
- [Parallel Dispatch Rules](references/parallel-dispatch-rules.md)
- [Acceptance Patterns](references/acceptance-patterns.md)
- [Integration and Recovery Decisions](references/integration-and-recovery.md)
- [ClawHub Skill Page](https://clawhub.ai/cjke84/skills/agent-orchestrator-template)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Text]

**Output Format:** [Markdown guidance with text templates and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration decisions, task contracts, decomposition worksheets, acceptance checklists, and recovery notes for the main agent.]

## Skill Version(s):

0.1.1 (source: server release metadata and manifest.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
