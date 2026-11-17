## Description:

Cloud Storage Manager helps agents manage multi-cloud storage operations across AWS S3, Aliyun OSS, Tencent COS, and Azure Blob Storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to generate guidance, code, commands, and configuration for upload, download, bucket management, sync, multipart upload, CDN URL, and cross-provider copy workflows across supported cloud storage services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud storage actions can affect real buckets, containers, paths, and objects, including deletion or sync operations that may be irreversible.

Mitigation: Use least-privilege credentials limited to the intended buckets or containers, verify source and destination paths before running actions, and treat delete_remote=True or delete() as destructive.

Risk: Credential handling is required for supported cloud providers, and hardcoded secrets can expose cloud accounts.

Mitigation: Load credentials from environment variables or a secret manager, avoid committing real secrets, and rotate any credential exposed during testing or examples.

Risk: Dependencies are specified with lower bounds rather than pinned versions, which can change install behavior over time.

Mitigation: Pin dependencies or install from a reviewed lockfile for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/cloud-storage-manager)
- [Publisher profile](https://clawhub.ai/user/kaiyuelv)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud-provider environment variables, API examples, path selections, and sync options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
