## Description: <br>
Guide for setting up an OpenClaw AI companion agent with memory, Feishu text and audio messaging, selfie-style image generation, and scheduled behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan966890](https://clawhub.ai/user/evan966890) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill as a setup guide for configuring a companion agent that keeps memory, sends scheduled Feishu text and audio messages, and creates selfie-style images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled outbound messaging with credentials can contact recipients without clear consent or an obvious stop path. <br>
Mitigation: Use only a test Feishu app and a known consenting recipient, limit app permissions, and add clear stop or disable instructions for cron jobs. <br>
Risk: Memory files may retain sensitive personal context. <br>
Mitigation: Regularly inspect or delete memory files and avoid storing secrets or highly sensitive information. <br>
Risk: FAL and Feishu secrets may be exposed through agent-readable files or local shell execution. <br>
Mitigation: Keep secrets out of agent-readable files where possible and prefer scoped credentials or environment injection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evan966890/ai-companion-setup) <br>
- [Publisher profile](https://clawhub.ai/user/evan966890) <br>
- [fal.ai Grok Imagine image edit endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu IM file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu IM message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with bash snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers OpenClaw workspace files, Feishu messaging scripts, cron setup, memory files, and dependencies such as curl, jq, ffmpeg, ffprobe, python3, edge-tts, and FAL_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
