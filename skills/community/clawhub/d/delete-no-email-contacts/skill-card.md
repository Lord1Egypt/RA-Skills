## Description:

Delete contacts with no email address from a HubSpot CRM instance using the HubSpot CRM Search and Batch Archive APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM administrators use this skill to identify HubSpot contacts without email addresses, export audit CSVs, delete those contacts in batches after confirmation, and verify the cleanup result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deletes HubSpot CRM contacts that lack email addresses.

Mitigation: Review the before-state count and CSV, confirm the safety threshold matches the expected cleanup size, and type DELETE only when the deletion is intended.

Risk: Generated CSV audit files may contain contact identifiers and CRM metadata.

Mitigation: Keep CSV outputs out of source control, backups, and shared folders unless they are protected.

Risk: A broad HubSpot token could expose more CRM access than the skill needs.

Mitigation: Use a least-privileged HubSpot private app token limited to contact read and write scopes.

## Reference(s):

- [Delete No Email Contacts on ClawHub](https://clawhub.ai/tomgranot/skills/delete-no-email-contacts)
- [HubSpot API endpoint used by the skill](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code, shell commands, environment configuration, console summaries, and CSV audit files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HubSpot private app token with contact read/write scopes and writes local CSV audit logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
