## Description: <br>
Upload a local file to DogeCloud OSS (DogeCloud 对象存储) and return a public URL + metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[white0dew](https://clawhub.ai/user/white0dew) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to upload selected local files to DogeCloud OSS and retrieve machine-readable public access metadata, including primary and candidate URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files uploaded through the skill may become publicly accessible. <br>
Mitigation: Confirm the intended bucket and object visibility before upload, and do not use the skill for secrets, private documents, personal data, or internal artifacts unless the sharing model is intended. <br>
Risk: DogeCloud credentials are required to request temporary upload tokens. <br>
Mitigation: Keep permanent credentials server-side or in local environment variables, prefer the least-privilege OSS_UPLOAD channel, and avoid exposing credentials in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/white0dew/doge-oss-skill) <br>
- [DogeCloud OSS Notes](artifact/references/dogecloud-oss.md) <br>
- [DogeCloud API access token documentation](https://docs.dogecloud.com/oss/api-access-token.md) <br>
- [DogeCloud Python SDK guide](https://docs.dogecloud.com/oss/sdk-full-python.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the uploader script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Machine-readable upload metadata includes bucket, object key, file metadata, temporary token metadata, and public URL candidates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
