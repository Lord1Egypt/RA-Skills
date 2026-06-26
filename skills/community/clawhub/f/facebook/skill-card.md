## Description: <br>
OpenClaw skill for Facebook Graph API workflows focused on Pages posting, comments, and Page management using direct HTTPS requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan Facebook Page publishing, comment management, Page operations, permissions, tokens, and operational guardrails for direct HTTPS Graph API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Comment deletion or moderation guidance can change public Page content. <br>
Mitigation: Require explicit confirmation before deleting comments or making other public moderation changes. <br>
Risk: Facebook access tokens and app secrets can expose Page management privileges if logged or leaked. <br>
Mitigation: Use least-privilege Page tokens, keep app secrets and tokens out of logs, store credentials securely, and rotate tokens when possible. <br>
Risk: Webhook events can be spoofed if callback signatures are not validated. <br>
Mitigation: Validate X-Hub-Signature-256 with the app secret and keep webhook handlers idempotent. <br>


## Reference(s): <br>
- [Facebook Graph API Overview](references/graph-api-overview.md) <br>
- [Page Posting Guide](references/page-posting.md) <br>
- [Comments and Moderation](references/comments-moderation.md) <br>
- [Permissions and Tokens](references/permissions-and-tokens.md) <br>
- [Webhooks (Pages)](references/webhooks.md) <br>
- [HTTP Request Templates (Graph API)](references/http-request-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Page workflow plans, permissions checklists, and operational guardrails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
