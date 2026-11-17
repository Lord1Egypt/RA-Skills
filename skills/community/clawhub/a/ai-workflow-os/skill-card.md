## Description:

AI Workflow OS routes multi-surface AI-assisted requests across specialist workflow skills while preserving authority, evidence, and state ownership boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to route requests that span research, project governance, implementation, session memory, and synthesis into the smallest appropriate set of specialist workflows. It helps keep one owner per state surface and produces a single coherent handoff or response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit routing can activate for broad multi-step requests and produce a route that affects stateful work.

Mitigation: Review the selected route and require explicit confirmation before any state update, upload, migration, deletion, or handoff persistence.

Risk: A routing skill can create confusion if it writes competing targets, status records, research queues, or acceptance decisions.

Mitigation: Assign one owner per state surface and let specialist skills retain their permissions, evidence rules, and acceptance boundaries.

Risk: Fallback modules have reduced fidelity compared with installed specialist skills.

Mitigation: Label unexecuted or fallback-only stages clearly and do not claim specialist actions, independent acceptance, archive success, or upload success unless they actually occurred.

## Reference(s):

- [Quickstart](QUICKSTART.md)
- [Security](SECURITY.md)
- [Shared Principles](modules/shared-principles.md)
- [Project Lifecycle Fallback](modules/project-lifecycle.md)
- [Project Memory Fallback](modules/project-memory.md)
- [Knowledge Intake Governance Fallback](modules/knowledge-intake-governance.md)
- [Cross-Source Synthesis](modules/cross-source-synthesis.md)
- [Migration From The Monolithic v1 Design](references/migration-guide.md)
- [Source Trust Levels](references/source-trust-levels.md)
- [Usage Examples](references/usage-examples.md)
- [Platform Operation Guide (Chinese)](references/platform-operation-guide-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with routing decisions, evidence notes, state-owner assignments, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fallback templates and structured project records when an authorized specialist route permits persistence.]

## Skill Version(s):

2.1.0 (source: evidence release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
