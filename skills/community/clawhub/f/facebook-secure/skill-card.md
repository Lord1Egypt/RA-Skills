## Description: <br>
OpenClaw skill for Facebook Graph API workflows focused on Pages posting, comments, and Page management using direct HTTPS requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinkom-byte](https://clawhub.ai/user/kevinkom-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan Facebook Page publishing, comment moderation, token handling, webhook validation, and safe direct HTTP Graph API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Facebook app secrets and access tokens can be exposed through logs, committed files, URLs, or shared prompts. <br>
Mitigation: Store credentials in a secure secret manager or environment manager, prefer Authorization headers over query-string tokens, avoid logging secrets, and rotate tokens after suspected exposure. <br>
Risk: Overbroad Page permissions can allow unintended publishing, editing, deletion, or comment moderation. <br>
Mitigation: Use the narrowest Page permissions required for the workflow and require explicit human approval before publishing, editing, hiding, or deleting Page content. <br>
Risk: Webhook requests can be spoofed or replayed if signatures and payload timing are not checked. <br>
Mitigation: Validate X-Hub-Signature-256 with the app secret, reject invalid signatures, and verify event timing and structure before processing. <br>
Risk: Graph API rate limits or transient failures can cause duplicate or failed Page actions. <br>
Mitigation: Use backoff and retry controls, monitor app and Page usage headers, and make handlers idempotent where possible. <br>


## Reference(s): <br>
- [Facebook Graph API Overview](references/graph-api-overview.md) <br>
- [Page Posting Guide](references/page-posting.md) <br>
- [Comments and Moderation](references/comments-moderation.md) <br>
- [Permissions and Tokens](references/permissions-and-tokens.md) <br>
- [Webhooks (Pages)](references/webhooks.md) <br>
- [HTTP Request Templates (Graph API)](references/http-request-templates.md) <br>
- [Security and Secrets Management](references/security-and-secrets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples, permissions checklists, and operational guardrails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required Facebook environment variables and direct Graph API request templates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
