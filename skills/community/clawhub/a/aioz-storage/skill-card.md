## Description:

Deploy static websites to AIOZ Storage with built-in templates or custom sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinhbui3004](https://clawhub.ai/user/vinhbui3004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to prepare, upload, and publish static websites on AIOZ Storage using bundled templates or their own static files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIOZ account, bucket, grant, and storage credentials can leak or persist longer than users expect.

Mitigation: Use only an AIOZ account and bucket you control, avoid entering passwords or seed phrases in chat or shell history, and rotate any exposed ZKeys, grants, S3 keys, or bucket recovery phrases.

Risk: The documented /tmp config-file workflow can leave sensitive grant inputs on disk.

Mitigation: Prefer command-line or in-memory handling that avoids persistent config files; if a config file is used, delete it immediately and restrict access to the working environment.

Risk: Long-lived or overly broad grants can retain access beyond the deployment task.

Mitigation: Prefer short-lived, least-privilege grants and use the read/list-only website grant where the workflow requires it.

## Reference(s):

- [AIOZ Storage Skill on ClawHub](https://clawhub.ai/vinhbui3004/skills/aioz-storage)
- [AIOZ Storage bucket management documentation](https://aiozstorage.network/docs/tutorials/manage-buckets)
- [AIOZ Storage static website templates](https://github.com/AIOZStorage/aioz-storage-docs/tree/main/examples)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment guidance, API calls, grant-generation commands, S3 upload instructions, and website configuration steps.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
