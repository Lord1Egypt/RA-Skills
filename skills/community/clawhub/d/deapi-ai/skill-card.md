## Description:

deAPI media toolkit for transcription, image generation and editing, text-to-speech, video generation, OCR, background removal, upscaling, embeddings, account balance checks, and delivery setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleglowa](https://clawhub.ai/user/aleglowa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to run media and text workflows through deAPI, including generation, transcription, OCR, image processing, embeddings, and async result delivery. It is intended for external users who can supply a deAPI API key and review proposed API calls before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, text, media, URLs, and generated-output metadata are sent to deAPI.

Mitigation: Use only content appropriate for third-party processing; avoid secrets, regulated data, private signed URLs, and sensitive local files.

Risk: The provided curl examples include shell, URL, and temporary-file patterns that may be unsafe if copied directly.

Mitigation: Serialize JSON safely, validate URLs before fetching, and use private temporary files with controlled permissions.

Risk: Webhook snippets are examples and do not implement full production verification.

Mitigation: Implement real webhook signature verification and reject unsigned or invalid callback requests before processing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aleglowa/skills/deapi-ai)
- [deAPI](https://deapi.ai)
- [deAPI webhooks documentation](https://docs.deapi.ai/execution-modes-and-integrations/webhooks)
- [deAPI WebSockets documentation](https://docs.deapi.ai/execution-modes-and-integrations/websockets)
- [Kokoro voices](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON snippets, and optional starter code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Async deAPI workflow: submit a job, poll status, then fetch the result_url.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
