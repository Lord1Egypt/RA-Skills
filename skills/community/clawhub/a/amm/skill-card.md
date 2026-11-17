## Description:

Advertised as AMM/blockchain analysis, but the inspected artifact implements a local entry and configuration management CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill as a local CLI datastore for recording, searching, listing, removing, exporting, and configuring entries. Do not rely on it for AMM protocol analysis without independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is advertised as AMM analysis but behaves as a local entry/config datastore.

Mitigation: Review the skill before installation and do not use it for AMM protocol or security analysis unless separately validated.

Risk: The script creates, modifies, deletes, and exports local files, with AMM_DIR controlling the data directory.

Mitigation: Run it in a constrained workspace, set AMM_DIR to a dedicated directory, and avoid using sensitive paths.

Risk: Configuration updates may be unsafe with untrusted keys or values.

Mitigation: Only pass trusted configuration values and inspect config changes before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/amm)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)
- [Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text CLI output with JSONL, JSON, or CSV file exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies local files under AMM_DIR, defaulting to ~/.amm/.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
