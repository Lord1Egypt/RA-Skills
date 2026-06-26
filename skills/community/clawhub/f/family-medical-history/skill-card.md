## Description: <br>
A local SQLite-backed skill for setting up, updating, querying, and exporting structured family medical records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silent404](https://clawhub.ai/user/silent404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or household caregivers use this skill to keep structured family medical profiles, visits, medications, allergies, vaccinations, chronic conditions, and follow-up schedules in a local database. Agents can query the records, propose updates, and export human-readable Markdown backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles and persists highly sensitive health and identity data in a local plaintext SQLite database and optional Markdown exports. <br>
Mitigation: Store the database and exports only in protected local locations; avoid shared or cloud-synced folders unless separate encryption and access controls are in place. <br>
Risk: Agent-proposed inserts or updates could add incorrect or unapproved medical-record content. <br>
Mitigation: Review every proposed insert, update, import, and export before execution, and treat the records as personal documentation rather than medical advice. <br>
Risk: The release evidence does not show clear consent, retention, deletion, or backup safeguards for household medical records. <br>
Mitigation: Define who may be recorded, how long records are kept, how backups are protected, and how records can be deleted before routine use. <br>


## Reference(s): <br>
- [Family Medical History — Schema Reference](references/schema.md) <br>
- [Family Medical History — Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite records and optional Markdown exports; no external API or credential requirement is evidenced.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
