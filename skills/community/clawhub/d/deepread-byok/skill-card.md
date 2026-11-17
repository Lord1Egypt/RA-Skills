## Description:

DeepRead BYOK guides users through connecting their own OpenAI, Google, or OpenRouter API key so DeepRead document processing routes through the user's provider account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external DeepRead users use this skill to configure Bring Your Own Key processing, understand provider choices, and keep existing DeepRead API workflows while billing LLM usage to their own provider account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users must provide a third-party provider API key through the DeepRead dashboard.

Mitigation: Install only if comfortable with that key flow; use scoped or revocable provider keys where possible.

Risk: Documents are sent to DeepRead's API for processing.

Mitigation: Review DeepRead's service and data-handling policies before sending sensitive documents.

Risk: Plaintext key handling can expose credentials.

Mitigation: Prefer environment variables or a secrets manager over plaintext .env storage, and avoid sharing keys in chat, screenshots, or logs.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead BYOK dashboard](https://www.deepread.tech/dashboard/byok)
- [DeepRead skill page](https://clawhub.ai/uday390/skills/deepread-byok)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only setup guidance; it does not collect, store, or transmit provider keys itself.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
