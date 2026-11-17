## Description: <br>
Unified cloud storage manager for uploading, downloading, syncing, and estimating costs across AWS S3, Google Cloud Storage, Azure Blob, Cloudflare R2, Backblaze B2, and major drive services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and storage operators use this skill to manage cloud storage transfers, backups, downloads, one-way syncs, credential setup, and cost estimates across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags mismatched activation wording that could route broad project-management requests into a credentialed cloud file-transfer workflow. <br>
Mitigation: Use the skill only for explicit cloud-storage tasks and review the trigger wording before installation or use. <br>
Risk: Cloud storage operations can expose or misuse provider credentials. <br>
Mitigation: Provide least-privilege credentials, avoid storing secrets in shell history or repositories, and rotate credentials according to provider policy. <br>
Risk: Sync, delete, or transfer actions can write to the wrong local or remote path or create unexpected cost. <br>
Mitigation: Prefer dry-run or cost-estimation modes before writes, verify exact source and target paths, and confirm backups before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-storage-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Declared homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud-provider paths, credential setup guidance, dry-run or cost-estimation advice, transfer status, results, and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
