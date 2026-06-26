## Description: <br>
Guidance for connecting Feishu with OpenClaw to set up enterprise AI assistants for group chat bots, customer support, and automated workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise administrators use this skill to configure Feishu applications, OpenClaw channel settings, bot message handling, scheduled notifications, file processing, and multi-agent routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise chat messages, chat history, and uploaded files may be sent to OpenClaw or downstream model providers without clearly defined privacy boundaries. <br>
Mitigation: Confirm processing locations and retention terms before deployment, and require explicit administrator approval for chat-history and file-analysis features. <br>
Risk: Feishu app credentials and broad API scopes could expose tenant data or bot controls if mishandled. <br>
Mitigation: Store FEISHU_APP_ID and FEISHU_APP_SECRET in a secrets manager, rotate them regularly, and grant only the Feishu scopes required for approved use cases. <br>
Risk: Scheduled notifications configured for ALL groups can broadcast messages more widely than intended. <br>
Mitigation: Disable broad broadcasts by default and maintain an allowlist of approved chats, groups, and notification templates. <br>
Risk: File processing can introduce sensitive or unsupported document types into the workflow. <br>
Mitigation: Restrict allowed file types, scan files before analysis, and define deletion rules for downloaded or cached file content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/feishu-openclaw-integration) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw community](https://discord.gg/clawd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with configuration snippets and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu app settings, Node.js integration examples, YAML templates, and deployment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
