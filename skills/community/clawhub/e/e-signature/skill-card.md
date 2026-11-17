## Description:

Send PDFs for e-signature from OpenClaw and track signer status, with reusable templates and reminders for up to 10 signers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conecto](https://clawhub.ai/user/conecto)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to send contracts and other PDFs for signature, check signer progress, and issue reminders. It returns signed PDFs and signature status through Conecto.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signature requests and reminders email people outside the business, use Conecto to process documents, and incur service charges.

Mitigation: Confirm the recipients, document title, and expected charge with the user before sending or reminding, and make sure they are comfortable with Conecto's data handling.

Risk: The skill does not determine whether a drawn or typed signature meets the legal requirements for a particular document.

Mitigation: Ask the user to confirm the required signature type and seek legal review when validity requirements matter.

## Reference(s):

- [E-signature tool guide](https://conecto.chat/tools/esign.md)
- [Conecto error codes](https://conecto.chat/docs/errors.md)
- [Conecto pricing](https://conecto.chat/pricing.md)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Signed PDF files and text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports requests with up to 10 signers; signed PDFs include a signing certificate.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
