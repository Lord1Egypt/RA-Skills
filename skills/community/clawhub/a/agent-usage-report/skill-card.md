## Description:

Generates weekly OpenClaw Agent usage reports by reading local session logs and memory files, then summarizing task volume, tool calls, costs, frequent features, and memory notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[56xiaoli123](https://clawhub.ai/user/56xiaoli123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw Agent users use this skill to summarize recent agent activity into a weekly operational report covering sessions, messages, tool usage, costs, and memory notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session history and memory files, which may contain private conversation notes, tool data, or secrets.

Mitigation: Install and run it only in workspaces where reading those local files is acceptable, and review the generated report before sharing or saving it.

Risk: The implementation uses hard-coded OpenClaw paths and does not fully honor the documented workspace option.

Mitigation: Confirm the local paths before running the script, and do not rely on the workspace option to isolate all data sources.

## Reference(s):

- [Agent Usage Report on ClawHub](https://clawhub.ai/56xiaoli123/skills/agent-usage-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text report with Markdown-style sections and optional saved text file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report summarizes the selected date range and may include excerpts from local memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
