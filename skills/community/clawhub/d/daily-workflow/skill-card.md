## Description:

Daily Workflow helps agents create evidence-backed project checkpoints, wrap-ups, and handoffs so work can resume without re-reading the whole project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve concise project memory at start, checkpoint, wrap-up, and handoff moments. It writes project-local Markdown notes that capture current state, verification evidence, blockers, risks, and exact next actions without replacing existing governance records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint or handoff notes can contain sensitive project context if shared outside the project.

Mitigation: Review generated Docs/ notes before sharing and avoid recording secrets, credentials, full confidential data, or large private logs.

Risk: Project memory files can conflict with existing governance or acceptance records.

Mitigation: Read existing project authority first, preserve dirty worktrees and governance evidence, and summarize externally owned fields instead of overwriting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/englandtong/skills/daily-workflow)
- [Quickstart](artifact/QUICKSTART.md)
- [Security Guide](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files and concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project-local workflow notes, normally under Docs/, when persistence is clearly authorized.]

## Skill Version(s):

4.1.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
