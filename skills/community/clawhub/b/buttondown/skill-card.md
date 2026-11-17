## Description:

Create, update, inspect, and send test previews of Buttondown newsletter emails through the Buttondown API, defaulting to draft-only workflows that require explicit approval before sending, scheduling, publishing, deleting, or emailing previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayhollister](https://clawhub.ai/user/rayhollister)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and newsletter operators use this skill to turn local Markdown or HTML newsletter copy into Buttondown drafts, update drafts, inspect email metadata, render previews, and send test previews after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BUTTONDOWN_API_BASE can be overridden, which may send Buttondown tokens and newsletter data to an arbitrary endpoint if the runtime environment is influenced.

Mitigation: Use the default Buttondown API endpoint, avoid setting BUTTONDOWN_API_BASE with production credentials, and prefer removing the override or enforcing HTTPS with an api.buttondown.com allowlist before deployment.

Risk: Preview sending contacts external recipients and can disclose draft newsletter content.

Mitigation: Require explicit user approval in the current conversation, show the target recipients before sending, and use least-privilege Buttondown API keys.

Risk: API keys may be exposed if pasted into chat, command history, repository files, logs, screenshots, or draft bodies.

Mitigation: Read BUTTONDOWN_API_KEY from a runtime secret store or managed environment variable and redact token values in errors or dry-run output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rayhollister/skills/buttondown)
- [Publisher Profile](https://clawhub.ai/user/rayhollister)
- [Buttondown Skill Homepage](https://forge.rayhollister.com/rayhollister/buttondown)
- [Buttondown API Reference](references/api.md)
- [Buttondown OpenAPI Specification](https://docs.buttondown.com/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BUTTONDOWN_API_KEY for authentication, optionally BUTTONDOWN_CONTEXT for multi-newsletter accounts, and supports dry-run previews for write commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
