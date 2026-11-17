## Description:

Uploads a local image to Feishu and sends it to a group through a configured webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbing](https://clawhub.ai/user/imbing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure credentials and send a selected local image to a Feishu group from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials and webhook URLs can be exposed if config.py is shared or committed.

Mitigation: Keep config.py private, do not commit it, and rotate APP_SECRET or webhook values if exposure is suspected.

Risk: Selected local images are uploaded to Feishu and posted to the configured group.

Mitigation: Use the skill only for images intended for that Feishu group and avoid sensitive images unless group sharing is deliberate.

Risk: Overbroad Feishu app permissions can increase impact if credentials are misused.

Mitigation: Grant only the minimum image permission needed for the Feishu app.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imbing/skills/feishu-image-webhook)
- [Feishu Tenant Access Token Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Image Upload Endpoint](https://open.feishu.cn/open-apis/im/v1/images)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Feishu app credentials, webhook URL, and local image path.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
