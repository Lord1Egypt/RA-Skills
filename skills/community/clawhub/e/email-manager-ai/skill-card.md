## Description:

Email Manager helps users draft, revise, template, compare, and track emails while keeping templates, follow-ups, settings, and history in local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this skill to compose professional emails, draft replies, generate subject lines, build reusable templates, track follow-ups, and improve tone without granting inbox access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email drafts, templates, follow-up reminders, signatures, settings, and history may contain sensitive personal or business information stored in local files.

Mitigation: Review the local ~/.openclaw/email-manager/ files for retention needs, avoid entering secrets or regulated data unless appropriate, and delete saved history or templates when they are no longer needed.

Risk: The artifact includes example signature content with the author's identity and a promotional link that could be copied into user emails.

Mitigation: Review generated signatures before use and replace example identity, contact, and promotional content with the user's intended signature.

Risk: Generated email text may be inaccurate, inappropriate for the recipient, or inconsistent with the user's intent.

Mitigation: Review and edit drafts manually before sending; the skill does not access an inbox or send messages on the user's behalf.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/email-manager-ai)
- [Publisher profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown/plain text email drafts, subject lines, templates, follow-up lists, and local JSON state descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local JSON files under ~/.openclaw/email-manager/ through the host agent's read/write tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
