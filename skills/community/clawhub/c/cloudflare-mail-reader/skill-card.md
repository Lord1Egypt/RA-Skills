## Description: <br>
Read one mailbox's messages or a paginated mail list from a Cloudflare temporary mail system through the `/admin/mails` admin API and return structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcwang502](https://clawhub.ai/user/jcwang502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent fetch, normalize, summarize, or export messages from a controlled Cloudflare temporary mail backend without opening the web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent admin-level access to mailbox contents and verification codes. <br>
Mitigation: Install only for mail systems you control, use least-privilege credentials, and treat returned messages, exported files, and verification codes as confidential. <br>
Risk: Mailbox-wide reads and large result sets can expose more messages than intended. <br>
Mitigation: Specify a mailbox address and a small limit whenever possible; avoid no-address reads unless they are required. <br>
Risk: Raw payload output can expose sensitive message metadata or full message content. <br>
Mitigation: Use raw output only for explicit debugging needs and avoid sharing raw JSON or CSV in chats, screenshots, or logs. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Example Prompts](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jcwang502/cloudflare-mail-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [JSON or CSV, with optional Markdown summaries and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized mailbox fields, message previews, extracted verification codes, and raw payloads only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
