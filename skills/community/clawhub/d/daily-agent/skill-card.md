## Description:

Routes long-running and complex agent tasks by classifying requests, assessing complexity, coordinating subagents, applying Hat-system phases, and performing completion checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route complex or long-chain tasks, delegate work to subagents, manage planning and review phases, and summarize completion status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly orchestrates task routing, local script use, memory/profile writes, and commits, which can create persistent changes without enough user control or scoping.

Mitigation: Use only in a tightly controlled workspace after disabling automatic memory/profile writes, automatic commits, unbundled script execution, and always-on activation, or require explicit user approval and diff review for each persistent change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/daily-agent)
- [LEARNING.md](LEARNING.md)
- [meeting-minutes.md](templates/meeting-minutes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline plans, status updates, code blocks, shell commands, and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delegated task briefs, progress summaries, review results, and generated or modified local files when the host agent permits writes.]

## Skill Version(s):

2.18.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
