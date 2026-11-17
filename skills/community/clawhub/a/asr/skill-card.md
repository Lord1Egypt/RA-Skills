## Description:

Transcribe audio and video for agents through Speech is Cheap using an API key or x402 USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speechischeap](https://clawhub.ai/user/speechischeap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to submit audio or video from a URL or local file to Speech is Cheap and retrieve transcripts with optional speaker labels, word timestamps, and sound labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings are sent to Speech is Cheap for transcription, and ordinary transcripts may remain available indefinitely.

Mitigation: Send only media the caller requested and suggest --private for sensitive recordings.

Risk: Wallet mode spends native USDC from the caller's wallet and keeps purchase state on disk.

Mitigation: Use a trusted signer, approve a spending ceiling for each purchase, and keep payment state files confidential.

## Reference(s):

- [ClawHub release](https://clawhub.ai/speechischeap/skills/asr)
- [Speech is Cheap security](https://speechischeap.com/company/security/)
- [Errors](https://docs.speechischeap.com/errors/)
- [x402 Payments and Refunds](https://docs.speechischeap.com/x402-v2/payments/)
- [x402 Webhooks](https://docs.speechischeap.com/x402-v2/webhooks/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON, SRT, or VTT transcript results; shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous jobs can include speaker labels, word timestamps, or sound labels; results are retrieved by job ID or webhook.]

## Skill Version(s):

1.5.1 (source: server-resolved release, CHANGELOG, package.json; released 2026-11-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
