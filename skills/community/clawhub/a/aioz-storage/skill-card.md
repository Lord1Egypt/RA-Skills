## Description: <br>
Deploy static websites to AIOZ Storage with built-in templates or custom sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhbui3004](https://clawhub.ai/user/vinhbui3004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare, configure, and deploy static websites to AIOZ Storage using bundled templates or their own static site files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may involve account passwords, bucket seed phrases, root keys, S3 credentials, and grants. <br>
Mitigation: Handle login, seed phrase, and key entry yourself where possible; avoid placing secrets in chat, shell history, process arguments, or temporary files. <br>
Risk: Non-expiring, all-bucket, write, or delete grants can create high-impact access to AIOZ Storage resources. <br>
Mitigation: Use short-lived per-bucket grants and grant only the permissions needed for the current task; avoid all-bucket and delete permissions unless explicitly required. <br>
Risk: Website creation requires a read/list grant, while uploads require a separate read/write/list grant. <br>
Mitigation: Use separate grants for upload and website creation, and review permissions before registering credentials or calling the website API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vinhbui3004/aioz-storage) <br>
- [AIOZ Storage bucket management documentation](https://aiozstorage.network/docs/tutorials/manage-buckets) <br>
- [AIOZ Storage website template examples](https://github.com/AIOZStorage/aioz-storage-docs/tree/main/examples) <br>
- [AIOZ Storage service](https://aiozstorage.network) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps, template customization guidance, grant generation commands, and S3/API usage instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
