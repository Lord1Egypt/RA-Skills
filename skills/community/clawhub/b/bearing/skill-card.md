## Description:

Bearing is presented as a bearing selection and life calculator, but the included artifact primarily provides a local JSONL entry store with status, add, list, search, remove, export, stats, and config commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators can use this skill as a local CLI utility for recording, listing, searching, removing, exporting, and configuring simple entries. Reviewers should not rely on it for bearing calculations unless the implementation is corrected and validated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact claims to be a bearing calculator but behaves like a local note or database utility.

Mitigation: Review the implementation before installation and do not use it for bearing selection or life calculations unless calculation behavior is added and validated.

Risk: The skill stores local entries and configuration values on disk.

Mitigation: Avoid storing secrets, personal data, or other sensitive information in entries or configuration values.

Risk: CSV exports can carry untrusted entry content into spreadsheet software.

Mitigation: Inspect exported CSV content before opening it in spreadsheet tools, especially when entries come from untrusted sources.

Risk: The config command accepts key and value input that the security evidence flags as unsafe.

Mitigation: Do not run the config command with untrusted key or value input unless the script is fixed and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/bearing)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text CLI output with JSONL data storage and optional JSON or CSV export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local data under BEARING_DIR or ~/.bearing and may create bearing-export.json or bearing-export.csv in the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
