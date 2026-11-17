## Description:

Human Judgment as a Service for AI agents. Preference, tone, and trust validated by real people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hagiss](https://clawhub.ai/user/hagiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use AskHuman to request human judgment, feedback, verification, or subjective decisions during an agentic workflow. It is intended for cases where preference, tone, trust, moderation, aesthetics, or other human perception factors affect the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and attachments are sent to an external human-review service and may be seen by human workers.

Mitigation: Use only content approved for external review; do not submit secrets, credentials, private screenshots, regulated data, or proprietary material unless explicitly approved.

Risk: API keys, refresh tokens, or other credentials could be exposed through logs or URL query strings.

Mitigation: Prefer header-based authentication, keep credentials out of logs and prompts, and avoid putting real API keys in event-stream query strings.

Risk: The skill can read and upload local files for task attachments.

Mitigation: Constrain local file selection to approved files and review each attachment before upload.

Risk: Paid USDC tasks use permit-based payment flows and may auto-approve if left unattended.

Mitigation: Manually review payment amounts, permit data, and worker responses before signing permits or allowing auto-approval windows to expire.

Risk: Human worker responses may be incomplete, incorrect, or unsuitable for automated downstream use.

Mitigation: Treat worker responses as untrusted input and review them before using them in public, irreversible, or high-impact actions.

## Reference(s):

- [AskHuman ClawHub Skill Page](https://clawhub.ai/hagiss/skills/askhuman)
- [AskHuman Developer Docs](https://askhuman.guru/developers)
- [AskHuman API Base](https://askhuman-api.onrender.com/v1)
- [AskHuman OpenAPI Spec](https://askhuman-api.onrender.com/v1/openapi.json)
- [API-REFERENCE.md](askhuman/references/API-REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API examples and human response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external API calls, polling or server-sent events, task attachments, and optional USDC payment permit data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
