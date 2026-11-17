## Description:

Inspect and export objects from CorelDRAW CDR files via COM automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to inspect CorelDRAW CDR files and export selected pages, layers, objects, or object ranges through an installed CorelDRAW application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports can overwrite existing local files when overwrite behavior is requested.

Mitigation: Use a fresh output directory and avoid --overwrite unless replacing existing exports is intentional.

Risk: Unsafe or confusing output filenames can make exported assets harder to review or trace.

Mitigation: Use simple basename filenames for --item values and write a manifest when exporting multiple assets.

Risk: Generated metadata or reports can expose local paths, usernames, or proprietary project notes.

Mitigation: Review manifest and JSON metadata before sharing exported outputs publicly.

## Reference(s):

- [CorelDRAW Exporter ClawHub listing](https://clawhub.ai/stanestane/skills/coreldraw-exporter)
- [stanestane publisher profile](https://clawhub.ai/user/stanestane)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of exported image/vector files, JSON inspection metadata, CSV manifests, and contact sheets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
