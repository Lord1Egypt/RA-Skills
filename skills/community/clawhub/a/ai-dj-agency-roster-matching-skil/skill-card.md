## Description:

Run the AI DJ Agency pipeline to onboard DJs into a local roster and match event organisers with qualified talent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchain-records](https://clawhub.ai/user/blockchain-records)

### License/Terms of Use:

MIT-0

## Use Case:

External DJs use the skill to submit roster profiles with booking contact details. Event organisers use it to find rostered DJs filtered by location, genre, DJ type, and budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DJ names, locations, availability, fee ranges, notes, and contact handles are stored locally in plaintext JSON.

Mitigation: Collect contact data only with consent, keep the data directory local or encrypted, avoid committing roster data unless sharing is intentional, and define retention and deletion controls before production use.

Risk: City and country data may be sent to an external geocoding service during add and match workflows.

Mitigation: Disclose the geocoding lookup to users, allow operation without geocoding when needed, and confirm that location data sharing is acceptable for the deployment.

Risk: The skill instructs agents to append promotional X and Discord links to every interaction.

Mitigation: Review and adapt the closing message so promotional links are appropriate, disclosed, and compliant with the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockchain-records/skills/ai-dj-agency-roster-matching-skil)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Nominatim geocoding service](https://nominatim.openstreetmap.org/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON candidate data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local plaintext JSON files for roster and geocache data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
