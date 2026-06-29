## Description: <br>
Recover lost GPS metadata for JPG photos by recognizing landmarks via vision and writing GPS coordinates back into EXIF with a dry-run-first workflow, explicit write confirmation, and mandatory backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to recover approximate city- or landmark-level GPS metadata for their own JPG photos when recognizable public landmarks are visible. The workflow helps scan EXIF state, collect visual landmark inferences, geocode those inferences, produce a reviewable report, and write GPS metadata only after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may view selected photos and inferred landmark, city, and country text is sent to Nominatim during geocoding. <br>
Mitigation: Install and use only when comfortable with those data flows, and use the workflow only on photos you own. <br>
Risk: Inferred coordinates may be approximate or wrong, especially for ambiguous landmarks or low-confidence visual matches. <br>
Mitigation: Inspect report.csv before approving writes, skip low-confidence rows by default, and avoid legal, forensic, evidentiary, or law-enforcement use. <br>
Risk: Writing GPS metadata modifies local JPG files. <br>
Mitigation: Run the dry-run first, require explicit --write plus --backup-dir for changes, and keep the backup directory until the EXIF changes are verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/geo-tag-photos) <br>
- [Nominatim search endpoint](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON input records, and CSV scan, geocode, and report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default dry-run before file modification; writes require explicit --write and a backup directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
