## Description:

List and inspect local Codex session history by reading `~/.codex/session_index.jsonl`, `~/.codex/sessions/`, and `~/.codex/archived_sessions/`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sube-py](https://clawhub.ai/user/sube-py)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to enumerate local Codex sessions, identify session ids and titles, map sessions to projects and workspace paths, and filter sessions by project, session id, source, or local time window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private Codex conversation history, project names, usernames, repository paths, and session file locations.

Mitigation: Use it only in trusted local workflows and avoid placing details or JSON output in shared logs, tickets, or untrusted automation.

Risk: The skill reads local Codex history from active and archived session stores.

Mitigation: Run it only when the user intends to inspect local Codex session history and limit filters or output rows to the minimum needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sube-py/skills/codex-session-history)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-friendly terminal output or JSON, depending on command flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local session ids, project names, workspace paths, timestamps, session file locations, and first user message summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
