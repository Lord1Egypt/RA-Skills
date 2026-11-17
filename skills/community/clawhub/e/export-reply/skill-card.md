## Description:

Save any agent reply or full conversation to a local file, with support for MD, TXT, HTML, PDF, DOCX, raw export, condensed bilingual summaries, and remembered export settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-owo](https://clawhub.ai/user/ryan-owo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save an agent reply or full conversation as a local document for review, sharing, archiving, or follow-up work. It can preserve the original conversation or produce a condensed bilingual summary before export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML and PDF export can carry extra risk when used on untrusted or attacker-supplied conversation content.

Mitigation: Prefer MD or TXT for sensitive or untrusted content, and avoid HTML/PDF exports unless the content source is trusted.

Risk: Full-conversation exports can save sensitive chat content to a local path selected by the user or recalled from preferences.

Mitigation: Use explicit export requests, inspect the destination path before saving, and choose current-reply scope when a full conversation is not needed.

Risk: Preference memory stores the last export scope, mode, format, and path in ~/.export_reply_prefs.json.

Mitigation: Clear ~/.export_reply_prefs.json when remembered export paths or settings should not persist.

## Reference(s):

- [Format Reference](references/formats.md)
- [ClawHub Skill Page](https://clawhub.ai/ryan-owo/skills/export-reply)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and local files in MD, TXT, HTML, PDF, or DOCX format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports current-reply or full-conversation scope, raw or condensed bilingual summary mode, and optional preference memory for repeat exports.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
