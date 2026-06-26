## Description: <br>
Downloads Feishu file, image, and audio message attachments to a local file using Feishu message resource APIs and OpenClaw-stored Feishu app credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a Feishu group message contains a file, image, or audio attachment that must be downloaded locally for processing, conversion, forwarding, or inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Feishu app credentials from the local OpenClaw config and uses them to request tenant access tokens. <br>
Mitigation: Install it only for agents that should download Feishu message attachments, keep the config file access-limited, grant only necessary Feishu scopes such as im:resource, and rotate appSecret if the host is compromised. <br>
Risk: Default image filenames can include a partial resource key, which may appear in logs or downstream output paths. <br>
Mitigation: Pass a specific --output path when downloading images or when output paths may be logged. <br>
Risk: The --print-key debugging option can expose Feishu resource keys. <br>
Mitigation: Use --print-key only for interactive troubleshooting and do not record its output in logs or user-facing responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/feishu-fetch) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message resource endpoint](https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{resource_key}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain-text stdout path to the downloaded local file; stderr contains warnings or errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, bash, and Feishu app credentials in $HOME/.openclaw/openclaw.json; downloads only user-specified message resources.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
