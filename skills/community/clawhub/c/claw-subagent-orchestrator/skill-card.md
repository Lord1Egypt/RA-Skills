## Description:

Defines the collaboration protocol between main session and sub-agent sessions for executing heavy tasks (analysis, search, writing). Use when spawning sub-agents to reduce main-session context growth, managing task.md checklist workflows, coordinating multi-step delegated work with crash recovery, or optimizing skill workflows through retrospect analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slientrain-new](https://clawhub.ai/user/slientrain-new)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate large analysis, search, and writing tasks to isolated sub-agent sessions while keeping the main session focused on routing, recovery, and result handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated agents may send task results to WeChat or Telegram without final main-session review.

Mitigation: Require main-session approval before any external notification when tasks may include private messages, source code, credentials, business data, or personal information.

Risk: External notification destinations may receive sensitive content if channel permissions are too broad.

Mitigation: Use this skill only with explicitly approved notification destinations and disable direct external delivery for sensitive delegated tasks.

## Reference(s):

- [Protocol documentation](docs/protocol.md)
- [Task checklist template](templates/task.md)
- [Retrospect template](templates/task-retro.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown protocol guidance with task templates and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task.md, step records, and task-retro.md files in a delegated task workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
