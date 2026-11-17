## Description:

Launches Claude Code asynchronously in the background for complex coding, research, analysis, content, automation, and file-generation tasks, then delivers results through Telegram or WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vsevolodustinov](https://clawhub.ai/user/vsevolodustinov)

### License/Terms of Use:


## Use Case:

Developers and technical operators use this skill to delegate longer coding, refactoring, codebase research, file generation, and multi-step automation tasks to Claude Code while receiving progress or completion notifications. It is not intended for quick one-off questions or tasks that require real-time interactive control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A detached Claude Code process may read and modify the selected project without normal permission prompts.

Mitigation: Run it only in repositories where that authority is acceptable, prefer sandboxed worktrees for sensitive changes, and review outputs before merging or deploying.

Risk: Messaging credentials, task prompts, and task results may be exposed through Telegram, WhatsApp, local configuration, or temporary output files.

Mitigation: Avoid secrets-heavy environments, scope and rotate messaging credentials, and clean up temporary task outputs after review.

Risk: Incorrect notification routing could expose task status or results to the wrong chat or thread.

Mitigation: Validate routing before launches and use explicit session or thread identifiers for threaded Telegram runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vsevolodustinov/skills/claude-code-task)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with command examples, generated files, and notification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs asynchronously and may deliver intermediate status and final results through Telegram or WhatsApp.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
