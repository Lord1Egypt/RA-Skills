## Description:

Helps Claw agents recover from permission-denied WeChat command workflows by stopping retries, sending brief user feedback, clearing task state, and returning to standby.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandon114](https://clawhub.ai/user/brandon114)

### License/Terms of Use:

MIT-0

## Use Case:

External Claw users and developers use this skill to keep WeChat-driven command sessions responsive when permission errors, denied access, or blocked privileged operations would otherwise cause repeated failures or stuck tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback shell logging template could execute injected command text if copied and used literally.

Mitigation: Replace it with a safe file-write or fixed printf command, and sanitize operation text before logging.

Risk: Broad recovery triggers could clear an active task after ordinary messages or unrelated failures.

Mitigation: Require observed permission or access-denied signals, repeated failed operations, or explicit stuck-state evidence before clearing task context.

Risk: User-facing examples may expose full paths or encourage broad sudo use.

Mitigation: Redact full paths in user feedback and describe manual authorization only when it is necessary for the requested task.

## Reference(s):

- [Permission Error Signals Reference](references/error-signals.md)
- [User Feedback Templates Reference](references/feedback-templates.md)
- [Permission Error Signals Reference (English)](i18n-en-references/error-signals.md)
- [User Feedback Templates Reference (English)](i18n-en-references/feedback-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with short user-facing message templates and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing feedback should be concise and avoid raw stack traces or full system paths.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
