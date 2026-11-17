## Description:

Secrets-safe encrypted OpenClaw backups to S3/R2/B2/MinIO - lean modes, opt-in cron, staged restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obuchowski](https://clawhub.ai/user/obuchowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, verify, upload, retain, and restore encrypted OpenClaw state backups to S3-compatible storage after explicit backup or restore requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence says the implementation can produce plaintext sensitive backups despite claiming forced encryption.

Mitigation: Review before installing, use least-privilege bucket keys, keep access keys and passphrases out of openclaw.json, keep the passphrase file owner-only, and avoid plaintext backup options for full or settings backups unless the encryption policy is fixed.

Risk: Restore, prune, and scheduling actions can overwrite state, delete archives, or create unattended jobs.

Mitigation: Require dry-run output and explicit approval before restore, prune, or cron changes, and prefer staged restores before any in-place restore.

Risk: Credentials stored in OpenClaw config can be copied into every backup archive.

Mitigation: Use an AWS named profile, operator-managed environment, owner-only passphrase file, or OpenClaw SecretRef, and migrate away from plaintext config credentials.

## Reference(s):

- [Project homepage](https://github.com/obuchowski/openclaw-cloud-backup)
- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/cloud-backup)
- [Credentials](references/credentials.md)
- [Setup flow](references/setup-flow.md)
- [Security](references/security.md)
- [AWS S3 provider guide](references/providers/aws-s3.md)
- [Cloudflare R2 provider guide](references/providers/cloudflare-r2.md)
- [Backblaze B2 provider guide](references/providers/backblaze-b2.md)
- [DigitalOcean Spaces provider guide](references/providers/digitalocean-spaces.md)
- [MinIO provider guide](references/providers/minio.md)
- [Custom S3-compatible provider guide](references/providers/other.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, configuration values, dry-run plans, and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce encrypted backup archives, verification reports, restore plans, and cron payloads only through user-confirmed workflows.]

## Skill Version(s):

2.0.2 (source: server release metadata and changelog, released 2026-07-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
