## Description:

Helps agents create, maintain, query, and export bilingual family medical history records using a local SQLite database as the source of truth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent404](https://clawhub.ai/user/silent404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage family health profiles, visits, medications, allergies, vaccinations, chronic conditions, vitals, and follow-up schedules. It supports structured local recordkeeping and optional Markdown export for human review or backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Family medical and identity information may be stored locally in plaintext.

Mitigation: Keep the workspace private, avoid cloud-synced or shared folders, do not commit generated databases or Markdown exports, and apply local access controls appropriate for sensitive health records.

Risk: Markdown export behavior may overwrite files outside the intended records folder if identifiers or paths are not contained.

Mitigation: Treat export operations as risky until identifiers are validated and export paths are constrained to the records directory; review paths before running sync_db.py.

Risk: Incomplete or inaccurate medical entries could mislead later record review.

Mitigation: Use explicit unknown placeholders for missing facts and verify entries against source documents or qualified medical guidance before relying on them.

## Reference(s):

- [Schema Reference](references/schema.md)
- [Markdown Export Templates](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/silent404/skills/family-medical-history)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local SQLite-backed family medical record workflows and optional Markdown exports.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
