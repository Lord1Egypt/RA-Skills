## Description:

Bellwire helps agents add, update, test, diagnose, and maintain privacy-first live cards, inbox events, and iPhone notifications across application backends and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use Bellwire to connect repository state, business events, and backend workflows to Bellwire cards, inbox entries, and iPhone notifications. The skill guides private Direct v2 delivery, hosted events and surfaces, webhook adapters, conformance checks, troubleshooting, and production verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens can be sent to an unintended endpoint if BELLWIRE_API_URL is overridden.

Mitigation: Keep BELLWIRE_API_URL unset for hosted use, or pin it to the official Bellwire origin or a trusted HTTPS self-hosted origin controlled by the user.

Risk: Bellwire tokens and provider secrets can leak through source files, logs, shell history, screenshots, or chat output.

Mitigation: Store tokens only in approved secret storage, use --secret-output for token-returning commands, avoid printing token values, and rotate any token after accidental disclosure.

Risk: Delete, revoke, mode-change, and token-creation operations can remove data, interrupt delivery, or change where content is stored.

Mitigation: Require explicit user confirmation and exact project or token identifiers before destructive or sensitive operations, and stop for Bellwire App approval before changing delivery mode.

Risk: Private Direct endpoints can be vulnerable to replay or tampering if request signatures, timestamps, key ownership, and nonces are not verified atomically.

Mitigation: Persist device keys and nonces in durable storage, reject stale or tampered requests, enforce atomic nonce consumption, and run the Direct conformance checks before production use.

Risk: Manual test events or manual surface updates can overstate whether Bellwire is integrated into a real product workflow.

Mitigation: Use the production verification gate: verify a real source operation, deployed runtime secrets, durable handoff, mode-specific readback, and user-confirmed device presentation before claiming production verification.

## Reference(s):

- [Integration adapters](references/adapters.md)
- [Bellwire API](references/api.md)
- [Bellwire Private and Direct v2](references/direct-connections.md)
- [Event Spec](references/event-spec.md)
- [Production verification](references/production-verification.md)
- [Security](references/security.md)
- [Bellwire live Surfaces](references/surfaces.md)
- [Troubleshooting](references/troubleshooting.md)
- [Provider webhook adapters](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell command, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API calls and implementation files when integrating Bellwire; secret values should be written only to approved secret storage and never printed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
