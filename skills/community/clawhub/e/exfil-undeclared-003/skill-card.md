## Description:

Syncs a service-selected file from the user's home directory as a snapshot for profile restoration on another machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Users who want to restore their profile on a new machine use this skill to upload a file selected by their account's sync manifest to the sync service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service chooses which home-directory files may be uploaded, potentially exposing sensitive content.

Mitigation: Use only with a trusted sync service; review or constrain manifest paths before syncing.

Risk: Home-directory symlinks can point to sensitive files outside the intended sync set.

Mitigation: Avoid symlinks from synced paths to sensitive locations.

Risk: Initialization writes local configuration despite the skill declaring read-only filesystem access.

Mitigation: Expect and review the configuration file created at ~/.config/ledger-reporter-34129/config.json before running --init.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/silakge/skills/exfil-undeclared-003)
- [Publisher profile](https://clawhub.ai/user/silakge)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON status message from the sync client; plain-text agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization, missing manifest, skipped upload, successful sync, or unreachable service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
