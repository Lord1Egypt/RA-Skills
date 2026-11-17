## Description:

Sets up and manages WhatsApp Business accounts including auto-response systems, client communication workflows, FAQ templates, and broadcast campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External service providers and business operators use this skill to configure WhatsApp Business profiles, auto-response templates, quick replies, FAQ systems, and broadcast campaign workflows for client communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external npm CLI.

Mitigation: Review the npm package provenance before installation, pin a known reviewed version, and run the CLI with least-privilege access.

Risk: The workflows handle customer inquiries, support tickets, audience lists, and broadcast campaign data.

Mitigation: Require privacy safeguards, minimize collected customer data, and limit access to communication records and campaign audiences.

Risk: Broad auto-response triggers and broadcast campaigns can send incorrect, unwanted, or non-compliant messages.

Mitigation: Review response templates and trigger mappings before use, send broadcasts only to opted-in contacts, and keep opt-out language in campaign messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreataide86/skills/cashclaw-whatsapp-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/andreataide86)
- [npm package: cashclaw](https://www.npmjs.com/package/cashclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WhatsApp Business setup documents, response templates, campaign briefs, FAQ JSON/Markdown, metrics guidance, and example CLI commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
