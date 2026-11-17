## Description:

Deploy static websites to AIOZ Storage with built-in templates or custom sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinhbui3004](https://clawhub.ai/user/vinhbui3004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to prepare, customize, and deploy static websites to AIOZ Storage using built-in templates or their own static files. It guides authentication, bucket setup, grant generation, S3-compatible upload, and static website creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AIOZ account passwords, bucket seed phrases, root ZKeys, grants, and S3 keys.

Mitigation: Avoid pasting seed phrases into chat, keep secrets out of temporary files and logs, and rotate or revoke generated credentials after deployment where possible.

Risk: The documented grant flow uses duration 0, which creates non-expiring grants.

Mitigation: Prefer short-lived grants when the platform supports them and limit permissions to the documented upload or website task.

Risk: The workflow can upload all files from a selected project folder to AIOZ Storage.

Mitigation: Review the upload folder before syncing so private files, local configuration, or credentials are not published.

## Reference(s):

- [AIOZ Storage Skill on ClawHub](https://clawhub.ai/vinhbui3004/skills/aioz-storage-skill)
- [AIOZ Storage template examples](https://github.com/AIOZStorage/aioz-storage-docs/tree/main/examples)
- [AIOZ Storage bucket management tutorial](https://aiozstorage.network/docs/tutorials/manage-buckets)
- [AIOZ Storage service site](https://aiozstorage.network)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls]

**Output Format:** [Markdown with bash, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment steps, curl requests, template configuration guidance, S3 upload instructions, and JSON grant output when using the bundled CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
