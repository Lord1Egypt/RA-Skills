## Description:

Generates a professional invoice, presents a confirmation summary, and sends the confirmed invoice data to Make.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cimes19](https://clawhub.ai/user/cimes19)

### License/Terms of Use:


## Use Case:

Agents use this skill when a user wants to create an invoice, calculate invoice fields, request human confirmation, and send the confirmed invoice data to a Make.com workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends client and invoice details to an external Make.com workflow.

Mitigation: Install only when the Make.com workflow is controlled and trusted, and review data-handling expectations before production use.

Risk: The send workflow can report confirmation even when delivery fails.

Mitigation: Validate and surface the real send result before relying on the skill for production invoicing.

Risk: The Make.com webhook is embedded in the artifact.

Mitigation: Move the webhook to protected configuration before production deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cimes19/skills/facture-make)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [JSON payloads and concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before sending invoice data to the configured Make.com workflow.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
