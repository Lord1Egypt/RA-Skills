## Description:

Fetches the last 1 to 7 days of Egatee IM chat history with an API key and returns grouped chat summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahoyoshi](https://clawhub.ai/user/ahoyoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with authorized Egatee access use this skill to retrieve recent bound IM-account chat records and produce a compact per-peer summary for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private chat history and account credentials.

Mitigation: Install only where the Egatee API key is controlled, chat processing is authorized, and outputs are treated as private data.

Risk: Local environment loading and endpoint overrides can redirect requests or expose credentials if configuration is not controlled.

Mitigation: Use trusted, locked-down environment configuration; avoid run.sh unless .env is trusted, and set EGATEE_NOTIFY_BASE_URL only to approved HTTPS Egatee hosts.

Risk: Optional EGATEE_AUTH_TOKEN and debug behavior may increase credential or data exposure risk.

Mitigation: Avoid EGATEE_AUTH_TOKEN unless required and keep debug or request-tracing settings limited to authorized troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahoyoshi/skills/egatee-chat-summary)
- [Egatee production API host](https://api.egatee.com)
- [Egatee UAT API host](http://api.uat.egatee.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON containing meta and peer_summaries, with optional human-readable Markdown report behavior in the artifact code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EGATEE_CHAT_API_KEY and supports day, page size, max pages, timeout, and optional Egatee endpoint configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
