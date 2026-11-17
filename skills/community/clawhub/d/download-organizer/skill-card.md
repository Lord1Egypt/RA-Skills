## Description:

Download Organizer helps agents organize a downloads folder by classifying files by extension, previewing the plan, and running an undo flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT License

## Use Case:

External users and developers use this skill to generate commands and guidance for organizing downloads into category folders such as documents, images, videos, audio, installers, archives, code, and others. The bundled script can preview planned copies, copy files into an organized output directory, and undo previous organization using a backup mapping file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The undo flow trusts .download-organizer-backup.json and can copy or delete unintended files if that file was modified or created by someone else.

Mitigation: Run undo only with a backup file created by this tool that has not been edited, and keep input and output paths limited to a non-sensitive downloads area.

Risk: The script can read, copy, and delete files under the user's account.

Mitigation: Use preview mode first, review the planned source and destination paths, and operate only on the intended downloads directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/download-organizer)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with shell commands; the Python script copies files into categorized folders when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports preview mode before file operations and stores undo mappings in .download-organizer-backup.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
