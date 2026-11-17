## Description:

Recover lost GPS metadata for JPG photos by recognizing landmarks with vision, geocoding landmark text through Nominatim, and writing GPS coordinates back into JPG EXIF after explicit write confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to recover city- or landmark-level GPS metadata for their own JPG photo collections when the photos contain recognizable public landmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted or untrusted report CSV could cause the write step to alter JPG metadata outside the selected photo folder.

Mitigation: Use only reports generated during the current workflow, review planned writes before confirming, and avoid report files from other people or hand-edited sources.

Risk: Real EXIF writes modify photo files.

Mitigation: Run writes on copies or with verified backups, keep the default dry-run until the report is reviewed, and require --write with --backup-dir for modification.

Risk: Landmark, city, and country text is sent to Nominatim and cached locally during geocoding.

Mitigation: Process only trusted photo collections and avoid sending sensitive location descriptions when that disclosure is unacceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/geo-tag-photos)
- [Publisher profile](https://clawhub.ai/user/ucsdzehualiu)
- [Nominatim Search API](https://nominatim.openstreetmap.org/search)
- [README](artifact/README.md)
- [End-to-end test README](artifact/e2e/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, Metadata]

**Output Format:** [Markdown guidance with inline shell commands plus JSON and CSV workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; real writes require explicit confirmation, --write, and --backup-dir.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
