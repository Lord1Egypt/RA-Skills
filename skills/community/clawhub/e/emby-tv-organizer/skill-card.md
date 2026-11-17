## Description:

Emby TV Organizer helps an agent scan a TV series folder, preview Emby-compatible season and episode organization, preserve episode titles where detected, handle specials, and generate an Excel rename mapping after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[851032763](https://clawhub.ai/user/851032763)

### License/Terms of Use:

MIT-0

## Use Case:

External users and media library maintainers use this skill to organize TV series folders for Emby by reviewing proposed renames, moves, season folders, subtitle matches, and special-episode handling before applying changes. After confirmation, the agent can generate an Excel mapping report for audit and manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rename or move media files after confirmation.

Mitigation: Review the full proposed mapping before execution, keep backups of media folders, and rely on the documented no-overwrite conflict behavior.

Risk: The Excel generation script can install an unpinned openpyxl dependency at runtime.

Mitigation: Preinstall a pinned openpyxl version in the execution environment or disable runtime package installation before use.

Risk: Generated spreadsheets may contain local paths and filenames from untrusted sources.

Mitigation: Review generated Excel files before sharing them and treat filename-derived spreadsheet content as untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/851032763/skills/emby-tv-organizer)
- [README.md](README.md)
- [Episode pattern reference](references/episode_patterns.md)
- [Excel generation script](scripts/generate_excel.py)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown plans and tables, JSON input for spreadsheet generation, shell commands, and generated .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed to preview changes first and generate the Excel report through the bundled Python script after user confirmation.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
