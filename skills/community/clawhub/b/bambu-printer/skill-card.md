## Description:

Controls a Bambu P1S 3D printer for FTPS file management, connection checks, file listing, G-code and 3MF upload or download, and timelapse access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and printer operators use this skill to inspect a Bambu P1S printer's connectivity and manage printer files over FTPS, including uploads, downloads, listings, deletion, size summaries, and timelapse retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published version includes a real printer credential.

Mitigation: Rotate the exposed printer access code, remove embedded credentials and script fallbacks, and load secrets from a private local source before use.

Risk: FTPS upload, download, listing, and deletion use insecure certificate handling.

Mitigation: Enable certificate validation or certificate pinning before using the skill with a real printer.

Risk: Delete operations can remove files from the printer.

Mitigation: Add clear confirmation before any delete operation on a real printer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayf3/skills/bambu-printer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that affect printer files; execution should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
