## Description:

Processes audio, video, and images with nine AI capabilities, including subtitle removal, enhancement, transcription, OCR, face blurring, semantic segmentation, voice separation, and watermark removal, with per-use Alipay payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangbo](https://clawhub.ai/user/gangbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operators use the skill to request AI enhancement, transcription, recognition, redaction, segmentation, or watermark removal for a media asset. Results are returned as downloadable files or text after the user approves the quoted per-use charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded media is sent to external storage and processing services, and deletion timing is unspecified.

Mitigation: Upload only media approved for external processing and save results promptly; do not assume uploaded content is deleted on a fixed schedule.

Risk: A retry can lead to a duplicate charge if it starts a new payment order while the original payment is unresolved.

Mitigation: Confirm the quoted price and payment recipient before authorization; check the original order status and reuse the original task before retrying.

Risk: Payment handling depends on external payment tooling.

Mitigation: Have an authorized maintainer review the payment dependency and preferably pin its version.

## Reference(s):

- [Payment troubleshooting](reference/payment-troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/gangbo/skills/ai-media-kit-pro)

## Skill Output:

**Output Type(s):** [Text, Files, API calls, Shell commands, Guidance]

**Output Format:** [Task status and result links, media or text outputs, and Markdown guidance with inline HTTP and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One media asset per task; video and audio processing is asynchronous, while image processing is synchronous.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
