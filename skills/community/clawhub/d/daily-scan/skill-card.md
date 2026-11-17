## Description:

Scan photographed documents into searchable PDFs with OCR and stable file naming for local scan creation, storage, and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimjoohyeon-wq](https://clawhub.ai/user/kimjoohyeon-wq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn document photos into local searchable PDFs, preserve originals, name files from capture date and OCR headline text, and retrieve saved scans by date, title, or keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document photos, originals, and searchable PDFs may contain sensitive information stored in local scan folders.

Mitigation: Use a private scan folder, avoid shared writable directories, and delete originals or generated PDFs when they should no longer be retained.

Risk: OCR quality for Korean and English documents can vary, which may affect generated filenames, searchable text, and retrieval results.

Mitigation: Review the extracted title line and search results before relying on them for archiving or retrieval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Concise text result with saved filename, save location, and extracted title line; helper scripts may emit JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local searchable PDF files and keeps source images with the processed result when possible.]

## Skill Version(s):

1.0.4 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
