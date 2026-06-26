## Description: <br>
Enable real-time AI collaboration in Feishu (Lark) documents by detecting document edits, reading the document, and responding inline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongweiii](https://clawhub.ai/user/dongweiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using Feishu and OpenClaw use this skill to turn shared documents into human-agent collaboration spaces. It helps route finished messages to an agent, append replies in the document, and optionally coordinate Bitable task records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu document or Bitable edits can automatically start local agent sessions with document read/write authority through the configured Feishu app permissions. <br>
Mitigation: Use a dedicated Feishu app with access limited to intended documents and tables, and add allowlists or confirmation gates before using it in broad workspaces. <br>
Risk: The skill applies a persistent patch to the OpenClaw Feishu extension, which can be fragile across OpenClaw or extension updates. <br>
Mitigation: Keep the generated backup, review the patch before deployment, and reapply it intentionally after OpenClaw or extension updates. <br>
Risk: The hooks token and OAuth scopes can grant broad automation authority if exposed or over-scoped. <br>
Mitigation: Protect and rotate the hooks token, and grant only the Feishu OAuth scopes required for the intended documents and Bitable tables. <br>
Risk: Frequent Feishu event delivery can create duplicate or wasteful agent sessions if debounce or anti-loop behavior is bypassed. <br>
Mitigation: Keep the debounce and bot self-edit checks enabled, monitor gateway logs after deployment, and investigate duplicate responses before widening rollout. <br>


## Reference(s): <br>
- [Doc Chat Protocol Template](assets/DOC_PROTOCOL_TEMPLATE.md) <br>
- [Bitable Task Board Protocol](references/bitable-task-protocol.md) <br>
- [Feishu App Setup Guide](references/feishu-app-setup.md) <br>
- [Manual Patching Guide](references/manual-patch.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and code patch references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu/OpenClaw credentials and local extension patching; no fixed token cap.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
