## Description:

Send physical mail from CRM contacts using PostGrid by pulling contacts from GoHighLevel or Follow Up Boss, mapping contact and address fields, generating personalized mail payloads, and submitting letters or postcards through the PostGrid API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Sales, real estate, and CRM operations teams use this skill to turn GHL, FUB, or exported contact data into personalized postal mail campaigns through PostGrid. Developers and operators can dry-run payloads, send limited batches, or call PostGrid endpoints directly when maintaining mail workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles CRM contacts, customer postal addresses, and PostGrid API credentials.

Mitigation: Use least-privilege or test credentials, limit access to necessary contact data, and review generated payloads before live sending.

Risk: The included PostGrid utility exposes broad cataloged and raw API calls beyond basic letter or postcard sending.

Mitigation: Restrict use to trusted operators, avoid base URL overrides unless required, and review any direct PostGrid endpoint call before execution.

Risk: Live campaigns can send physical mail or create unintended costs if run on a large contact set.

Mitigation: Start with dry runs, inspect payload output, set small max-send limits for first live runs, and use clear campaign descriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoch/skills/crm-snail-mail-postgrid)
- [PostGrid route and header notes](artifact/references/postgrid-notes.md)
- [Example sender JSON](artifact/references/example_sender_us.json)
- [Example letter template](artifact/references/example_letter_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload or summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run PostGrid payloads, normalized contact JSON, and per-contact send summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
