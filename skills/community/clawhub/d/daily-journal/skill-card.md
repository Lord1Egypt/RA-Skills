## Description:

Daily Journal helps agents manage a local personal journal with daily entries, mood logs, gratitude notes, prompts, search, statistics, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, view, search, summarize, and export a private local daily journal without external accounts or services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal entries, mood logs, gratitude notes, and exports may contain sensitive personal information stored on local disk.

Mitigation: Restrict permissions on ~/.journal or the configured JOURNAL_DIR and treat exported files as sensitive.

Risk: The security evidence reports a path-handling flaw that can become code execution if the environment is manipulated.

Mitigation: Do not set JOURNAL_DIR from untrusted input, and review the environment before running the shell script.

## Reference(s):

- [Daily Journal ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/daily-journal)
- [Tips for Daily Journal](artifact/tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files]

**Output Format:** [Plain text command output, Markdown journal entries, and optional Markdown, JSON, or HTML exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local journal data under JOURNAL_DIR, defaulting to ~/.journal.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
