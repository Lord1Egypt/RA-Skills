## Description:

BYOK Relay Builder helps agents integrate byok-relay, an OpenAI-compatible LLM gateway for client-side apps that routes requests to multiple providers while supporting CORS-safe BYOK key registration, encryption, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avikalpg](https://clawhub.ai/user/avikalpg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to add multi-provider LLM access to browser, mobile, extension, and other client-side apps, with user- or organization-supplied provider keys and guidance for managed or self-hosted relay deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Managed relay use sends prompts and encrypted paid provider API keys to an external relay operator.

Mitigation: Use the managed relay only when its operator, privacy, and retention terms are acceptable; for sensitive production or organization-wide keys, prefer a self-hosted or app-controlled backend pinned to an audited release.

Risk: Provider keys can incur user or organization costs if relay access or stored credentials are abused.

Mitigation: Use scoped and budget-limited provider keys, support key rotation and deletion, and disclose billing ownership clearly to users.

Risk: Shared relay tokens can expose all stored keys associated with that token.

Mitigation: Keep shared relay tokens out of browsers, issue per-user relay tokens where possible, and proxy organization-wide relay access through an app-controlled backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avikalpg/skills/byok-relay)
- [Managed relay endpoint](https://relay.byokrelay.com)
- [byok-relay repository referenced by artifact](https://github.com/avikalpg/byok-relay)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, shell, HTML, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BYOK setup flows, API-key UI guidance, self-hosting commands, response-state handling, smoke-test steps, and security guidance.]

## Skill Version(s):

1.0.8 (source: server release metadata and artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
