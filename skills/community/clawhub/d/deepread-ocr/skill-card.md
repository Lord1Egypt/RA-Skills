## Description:

AI-native OCR platform that turns documents into high-accuracy data in minutes, using multi-model consensus to extract text and structured data while flagging uncertain fields for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure agents for DeepRead document OCR workflows, including PDF and image text extraction, structured JSON extraction, webhook or polling flows, and review of uncertain fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated public preview links can expose uploaded document contents to anyone who has the URL.

Mitigation: Review DeepRead privacy, retention, BYOK, and preview-link controls before installing; avoid public previews or webhooks for sensitive documents unless the organization accepts the exposure model and has an approved data-processing arrangement.

Risk: API keys may be exposed if copied into shared files, logs, or agent configuration.

Mitigation: Store the DeepRead key in DEEPREAD_API_KEY or another approved secret manager and avoid hardcoding credentials in Clawdbot configuration or examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-ocr)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead BYOK dashboard](https://www.deepread.tech/dashboard/byok)

## Skill Output:

**Output Type(s):** [markdown, shell commands, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl, JSON, JSON5, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and describes asynchronous processing, webhooks, polling, schemas, quality flags, preview links, rate limits, and BYOK setup.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
