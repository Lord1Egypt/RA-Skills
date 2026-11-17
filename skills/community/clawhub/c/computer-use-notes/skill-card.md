## Description:

Record and classify user observations about what computer use can do, partially do, and cannot do.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to keep a categorized notebook of computer-use capability observations, test results, limitations, and workarounds. It is intended for users who want concise notes sorted into can-do, partial, and cannot-do categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided note text is passed through a shell command invocation.

Mitigation: Change invocation to pass arguments directly without a shell, and review generated notes before relying on them.

Risk: Capability notes are retained persistently in local memory files.

Mitigation: Use only when persistent retention is acceptable, clearly delimit stored note text as untrusted, and provide a way to view and delete saved notes.

## Reference(s):

- [Computer Use Notes ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/computer-use-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Short text confirmation plus JSONL log entries and a Markdown board]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores notes persistently under memory/computer-use-notes.jsonl and memory/computer-use-notes.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
