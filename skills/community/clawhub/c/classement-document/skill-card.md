## Description:

Classement document files already identified accounting records into the appropriate client folder, normalizes filenames, and reports duplicates or records that need review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and their agents use this skill as the final filing step after document analysis and client identification. It copies invoices, bank statements, and expense notes into the expected client archive structure while sending uncertain or incomplete records to review folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File handling may copy or write outside the intended archive if hostile dossier metadata is accepted.

Mitigation: Install only for trusted dossier metadata, run under a restricted account, validate slug, date, and path values, reject absolute or parent-directory paths, and enforce the approved intake and archive boundaries before creating directories or copying files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/classement-document)
- [Publisher profile](https://clawhub.ai/user/trendex)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands]

**Output Format:** [JSON object with classement status, destination, filename, and optional detail fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies the source document into an archive folder and may update a deduplication index for successfully filed records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
