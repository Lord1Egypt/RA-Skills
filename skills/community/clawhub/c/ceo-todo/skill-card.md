## Description:

CEO To-Do maintains a canonical markdown to-do file for a CEO, captures and clarifies commitments into prioritized next actions, applies GTD status transitions, and validates every mutating run with a bundled deterministic checker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillsandagentsco](https://clawhub.ai/user/skillsandagentsco)

### License/Terms of Use:

MIT-0

## Use Case:

CEOs, executive operators, and their supporting agents use this skill to keep one markdown file as the source of truth for open commitments, waiting items, stale work, archived completions, and weekly review. The companion daily agent can read Gmail and Slack through authorized connectors to capture commitments without sending messages or posting replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell backup and validation flow can fail in ways that affect local command execution or task integrity, especially when document paths contain shell metacharacters.

Mitigation: Use the skill only with an explicit target to-do file, avoid document paths containing shell metacharacters, and prefer hosts or revised versions that perform backups through filesystem APIs rather than shell strings.

Risk: The daily Gmail and Slack agent reads sensitive business communications while identifying commitments.

Mitigation: Run the daily agent only in authorized workspaces with the intended connectors enabled, keep connector use read-only, and require human review for any outbound communication.

Risk: Skipping or losing validator execution can allow commitments to be lost, duplicated, or silently changed.

Mitigation: Run the bundled validator before and after every mutating write, stop on any non-zero result, and restore from the snapshot if the written document fails validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillsandagentsco/skills/ceo-todo)
- [Skills and Agents Co catalog page](https://skillsandagents.co/skills/ceo-todo/)
- [CEO To-Do Daily agent runbook](https://skillsandagents.co/agents/ceo-todo-daily/)
- [Brian Halligan source post](https://x.com/bhalligan/status/2054689082857730097)
- [Brian Halligan follow-up thread](https://x.com/bhalligan/status/2054691150175584330)
- [Sample canonical to-do document](references/sample-todo.md)
- [Validator script](references/validate.mjs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and a structured postcondition report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating updates are snapshot-backed and gated by validator execution before and after writes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
