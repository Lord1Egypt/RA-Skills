## Description:

消费级云存储免费版，帮助用户按设备组合选择消费级云存储服务，并澄清存储配额、同步和重复备份等常见困惑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for basic consumer cloud-storage decisions, including choosing between iCloud, Google Drive, OneDrive, and Dropbox based on their devices. It also helps clarify common storage and sync misunderstandings such as full cloud quotas, deleted files syncing across devices, duplicate photo backups, and paying for multiple services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command and file authority that is broader than ordinary consumer cloud-storage guidance requires.

Mitigation: Review before installing; prefer a narrowed version that removes exec/write access for advisory use.

Risk: The source includes unrelated automation, API, and database language that can confuse the intended scope.

Mitigation: Use the skill only for consumer cloud-storage service selection and common storage or sync explanations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-free)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown text with tables, examples, and short recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language consumer cloud-storage guidance; normal use does not require file output.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
