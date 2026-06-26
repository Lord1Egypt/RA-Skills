## Description: <br>
Secrets-safe encrypted OpenClaw backups to S3/R2/B2/MinIO - lean modes, opt-in cron, staged restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obuchowski](https://clawhub.ai/user/obuchowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, run, verify, prune, schedule, and restore encrypted OpenClaw state backups to S3-compatible storage after explicit backup or restore intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive bucket credentials and a backup encryption passphrase. <br>
Mitigation: Use a dedicated least-privilege bucket key, keep secrets out of openclaw.json, and store the GPG passphrase in a mode-600 file or OpenClaw SecretRef. <br>
Risk: Backup, restore, prune, and schedule operations can change local state or remote backup storage. <br>
Mitigation: Run dry-run commands before first backup, restore, and prune actions, and require explicit user confirmation for state-changing operations. <br>
Risk: Restoring a backup in place can overwrite existing OpenClaw state. <br>
Mitigation: Prefer staged restores, review the dry-run file list, and confirm overwritten paths before any in-place restore. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/obuchowski/cloud-backup) <br>
- [Project Homepage](https://github.com/obuchowski/openclaw-cloud-backup) <br>
- [Credentials](references/credentials.md) <br>
- [Setup Flow](references/setup-flow.md) <br>
- [Security](references/security.md) <br>
- [AWS S3 Provider](references/providers/aws-s3.md) <br>
- [Backblaze B2 Provider](references/providers/backblaze-b2.md) <br>
- [Cloudflare R2 Provider](references/providers/cloudflare-r2.md) <br>
- [DigitalOcean Spaces Provider](references/providers/digitalocean-spaces.md) <br>
- [MinIO Provider](references/providers/minio.md) <br>
- [Other S3-Compatible Providers](references/providers/other.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run plans, backup or restore status, exit-code explanations, and confirmation prompts for state-changing actions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and changelog, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
