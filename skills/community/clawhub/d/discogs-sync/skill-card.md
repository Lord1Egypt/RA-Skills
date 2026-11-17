## Description:

Helps manage Discogs wantlists and collections and look up marketplace prices for music releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

Discogs users and their assistants can add, remove, list, or bulk-sync wantlist and collection entries and compare marketplace prices for records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding, removing, or bulk-syncing entries can change Discogs account data or remove the wrong pressing.

Mitigation: Preview removals and bulk changes with --dry-run or the command's preview output, and obtain user approval before confirming changes.

Risk: The auth command stores a long-lived Discogs token in local plaintext configuration.

Mitigation: Prefer DISCOGS_USER_TOKEN over stored auth, and revoke the token if the machine is shared or compromised.

Risk: Pinned dependencies were flagged as vulnerable by the release security review.

Mitigation: Audit or update pinned dependencies before installation.

## Reference(s):

- [Discogs Sync on ClawHub](https://clawhub.ai/khaney64/skills/discogs-sync)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON command results, with suggested CLI commands and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CSV or JSON batch input; marketplace prices may reflect cached results.]

## Skill Version(s):

0.1.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
