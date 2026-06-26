## Description: <br>
在 OpenClaw 上搭建有记忆、能发语音/自拍/文字的 AI 陪伴 agent（完整踩坑指南） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan966890](https://clawhub.ai/user/evan966890) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill as a setup guide for a Feishu-based AI companion agent that can keep memory, send proactive text messages, generate voice messages, and send AI-generated selfies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad command and credential access for Feishu and fal.ai messaging can expose accounts or secrets if configured carelessly. <br>
Mitigation: Use a dedicated low-privilege Feishu app, grant only required messaging and file permissions, keep credentials out of shared files, and rotate any exposed secrets. <br>
Risk: Scheduled proactive messages can continue running after initial setup. <br>
Mitigation: Review every cron entry before enabling it, remove schedules that are not needed, and maintain a clear disable path for all automated messaging. <br>
Risk: The memory workflow can store sensitive personal context. <br>
Mitigation: Avoid storing sensitive personal information, review memory files regularly, and provide a documented deletion process. <br>
Risk: Identity-hiding and silent-operation behavior can make automation unclear to recipients or operators. <br>
Mitigation: Edit out identity-hiding instructions and require transparent controls before deploying the companion agent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evan966890/clawgirl) <br>
- [Publisher Profile](https://clawhub.ai/user/evan966890) <br>
- [fal.ai Grok Imagine Image Edit Endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guide with bash snippets, file templates, setup checklists, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires review of Feishu app permissions, cron schedules, local memory files, and credentials such as FAL_KEY before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
