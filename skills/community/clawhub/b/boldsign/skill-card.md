## Description:

BoldSign e-signature platform API integration with managed OAuth for sending documents for signature, managing documents, creating embedded signing links, and tracking document status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw to BoldSign through ClawLink, then list documents, send contracts for e-signature, manage brands and custom fields, create embedded signing links, and check API credit status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an unpinned third-party plugin that handles OAuth-backed document and signing actions.

Mitigation: Review the ClawLink plugin source, publisher identity, requested OAuth scopes, and installed version before using it with production BoldSign documents.

Risk: Contract workflows may expose sensitive documents when file URLs or upload flows are used.

Mitigation: Prefer private upload flows or short-lived signed URLs for contracts, and avoid making sensitive documents permanently public.

## Reference(s):

- [BoldSign API Docs](https://developers.boldsign.com/)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Dashboard for BoldSign](https://claw-link.dev/dashboard?add=boldsign)
- [ClawHub BoldSign Skill Page](https://clawhub.ai/hith3sh/skills/boldsign)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide OAuth-backed BoldSign document, brand, custom field, embedded signing, file upload, and plan-credit operations through ClawLink tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
