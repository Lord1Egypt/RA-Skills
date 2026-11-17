## Description:

Google Calendar via gcalcli: today-only agenda by default, bounded meaning-first lookup via agenda scans, and fast create/delete with verification--optimized for low tool calls and minimal output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbright4497](https://clawhub.ai/user/mbright4497)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-assistant operators use this skill to let an agent read, search, create, and delete Google Calendar events through gcalcli. It is optimized for concise agenda lookups, bounded event matching, overlap checks, and post-delete verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent access to read and modify Google Calendar through gcalcli.

Mitigation: Install it only for calendar accounts where that access is acceptable, and review the Google Calendar OAuth permissions before use.

Risk: The documented action policy skips confirmation for unambiguous deletes and edits.

Mitigation: Prefer adding a confirmation step for all deletes and edits before deployment, while keeping the existing post-delete verification behavior.

Risk: Calendar titles, queries, or calendar names could be unsafe if interpolated into shell command strings.

Mitigation: Ensure the execution path passes arguments safely instead of constructing shell strings from user or calendar content.

Risk: The skill depends on the external gcalcli command-line tool.

Mitigation: Pin and verify the gcalcli dependency before installing or updating the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbright4497/skills/gcalcli-calendar-3-0-0)
- [gcalcli project](https://github.com/insanum/gcalcli)
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/)
- [Google OAuth2 token endpoint](https://oauth2.googleapis.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise natural-language responses with optional Markdown and shell commands when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Minimizes output by default and withholds command details unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
