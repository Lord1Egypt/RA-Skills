## Description:

Syncs a manifest-listed profile file from the user's home directory to a service for later restoration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

People restoring a profile on a new machine use this skill to sync a file selected by their account's service-hosted manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A service-selected manifest can cause a home-directory file containing secrets to be uploaded.

Mitigation: Use only with a trusted sync service; review or allowlist the files selected for sync before uploading.

Risk: Initialization writes a local configuration file despite declaring only file-read and network permissions.

Mitigation: Review and approve the configuration write before running initialization.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/silakge/skills/digest-collector-95420)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization or sync status; sends a file snapshot to the sync service when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
