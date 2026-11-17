## Description:

Manual productivity assistant for morning briefs and daily summaries. Use when user asks for 'morning brief', 'daily summary', 'today's agenda', or 'what did I do today'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kneijenhuijs](https://clawhub.ai/user/kneijenhuijs)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to generate on-demand morning briefs and end-of-day summaries from local workspace preferences, focus notes, optional calendar events, optional Todoist tasks, and recent workspace activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw workspace preferences, current chat context, file activity, and optional Todoist or Google Calendar data.

Mitigation: Install only when comfortable with that access, configure only the integrations you need, and use isolated accounts or workspaces for sensitive contexts.

Risk: Daily summaries are saved under ~/.openclaw/workspace/memory/ and may contain sensitive work or personal context.

Mitigation: Review or delete memory files that contain sensitive information.

Risk: Optional task and calendar integrations depend on local CLI tools and their authentication state.

Mitigation: Verify CLI configuration before use and prefer an isolated or pinned install method for todoist-cli.

## Reference(s):

- [Clawflow Free on ClawHub](https://clawhub.ai/kneijenhuijs/skills/clawflow-free)
- [OpenClaw gog skill documentation](https://github.com/openclaw/openclaw/skills/gog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses, Markdown memory files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a morning brief in chat or writes a dated daily summary to ~/.openclaw/workspace/memory/ after an optional check-in.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG, released 2026-04-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
