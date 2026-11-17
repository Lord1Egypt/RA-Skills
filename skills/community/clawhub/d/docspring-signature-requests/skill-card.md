## Description:

Collects e-signatures with DocSpring signature requests. Sends a PDF template to one or more signers, whom DocSpring emails (in order and with reminders when asked) or who get links the user sends, embeds the signing form in an app with Signature Requests JS, and tracks signers, the signed PDF and the audit trail. Use when the user wants someone to sign, initial or fill in a DocSpring template, asks to send a document for signature, for signing links, e-signatures, several signers, a signing order or a signing page in their app, or works on code that sends signature_requests to DocSpring (data_requests in API v1 code), loads signature_request.v*.js or handles signature_request webhook events. Not for signing or stamping a local PDF without DocSpring, filling a template that nobody signs (docspring), or adding signature fields to a template (docspring-pdf-templates).

This skill is ready for commercial/non-commercial use.

## Publisher:

[docspring](https://clawhub.ai/user/docspring)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create and manage DocSpring signature requests, including preparing signer fields, sending signing links, embedding signing forms, and checking completion and audit details. It also helps developers work with DocSpring's MCP server, CLI, REST API, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live signature request can email signers as soon as it is created, and the emails cannot be recalled.

Mitigation: Before sending, confirm the template, signer names and email addresses, fields, signing order, and message with the user.

Risk: Anyone with a signing link can act as that signer.

Mitigation: Share each link only with its intended signer and keep it out of shared channels, tickets, logs, and commits.

Risk: The security scan had partial coverage, so its benign verdict does not cover every local reference.

Mitigation: Review the skill and unresolved references before connecting it to DocSpring or handling signature submissions.

## Reference(s):

- [DocSpring signature requests API reference](artifact/references/api.md)
- [DocSpring embedded signing forms reference](artifact/references/embedding.md)
- [DocSpring MCP documentation](https://docspring.com/docs/mcp/)
- [DocSpring CLI documentation](https://docspring.com/docs/cli/)
- [DocSpring embedded signature requests guide](https://docspring.com/docs/guides/embedded-forms/embedded-signature-requests.md)
- [DocSpring webhook events](https://docspring.com/docs/webhooks/events/)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON request examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signing request details, API examples, and embedded form guidance.]

## Skill Version(s):

1.9.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
