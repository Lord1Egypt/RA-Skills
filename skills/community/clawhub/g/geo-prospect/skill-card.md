## Description:

CRM-lite for managing GEO agency prospects and clients across lead tracking, audits, notes, deal values, and pipeline summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage GEO service prospects and clients through a lightweight sales pipeline, including prospect records, audit history, notes, deal values, and revenue summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores contact details, notes, audit details, and deal values in a local plaintext CRM directory.

Mitigation: Use it only on trusted machines, protect or exclude the storage directory from shared backups, and delete or relocate stored CRM data when it is no longer needed.

Risk: Domain values are used to save audit and proposal files, which can make file locations easy to overlook.

Mitigation: Use normal domain values and review generated paths before saving audits or proposals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-prospect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-style text with JSON-backed local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists CRM records, audit snapshots, and proposal paths under ~/.geo-prospects by default; SEOGEO_CRM_FILE can relocate the main state file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
