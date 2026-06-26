## Description: <br>
Deploy static websites to AIOZ Storage with built-in templates or custom sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhbui3004](https://clawhub.ai/user/vinhbui3004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare, grant access for, upload, and publish static websites on AIOZ Storage. It supports built-in templates and custom static sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles AIOZ account passwords, bucket seed phrases, bearer tokens, storage grants, and S3 credentials. <br>
Mitigation: Use a dedicated or limited bucket, avoid sharing secrets in chat or shell history, and revoke generated credentials or grants after deployment. <br>
Risk: Long-lived grants or broad permissions can leave storage access exposed beyond the deployment task. <br>
Mitigation: Prefer per-bucket grants, avoid all-buckets and delete permissions, and use the minimum permissions required for upload and website creation. <br>
Risk: Template files are downloaded and customized before upload. <br>
Mitigation: Review downloaded templates and generated site files before uploading them to the bucket. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vinhbui3004/aioz-storage-skill) <br>
- [Publisher profile](https://clawhub.ai/user/vinhbui3004) <br>
- [AIOZ Storage bucket management documentation](https://aiozstorage.network/docs/tutorials/manage-buckets) <br>
- [AIOZ Storage template examples](https://github.com/AIOZStorage/aioz-storage-docs/tree/main/examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance and commands; grant-cli.ts can emit JSON containing grant and zkey values.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
