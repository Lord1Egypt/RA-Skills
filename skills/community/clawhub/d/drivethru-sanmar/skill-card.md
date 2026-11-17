## Description:

drivethru-sanmar provides typed CLI tools for SanMar product search, pricing, inventory, purchase orders, tracking, invoicing, PO PDF parsing, color-code resolution, and portal return preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, purchasing agents, and accounts-payable operators use this skill to read from and write to SanMar systems for apparel sourcing, pricing, ordering, fulfillment tracking, returns preparation, and invoice reconciliation. Side-effecting purchase-order and return flows require explicit confirmation and should be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and credential-bearing payloads may be exposed through inline inputs, logs, or output surfaces.

Mitigation: Prefer environment-managed secrets, redact credentials and raw payloads from outputs, and avoid pasting secrets into user-visible responses.

Risk: Purchase-order submission is an external write that can create real vendor orders.

Mitigation: Require explicit human approval, validate the cart first, and preserve idempotency or reference keys before running a confirmed submission.

Risk: SFTP and portal access can be redirected or broadened if hosts, paths, or uploaded files are not constrained.

Mitigation: Restrict SFTP and portal destinations to approved SanMar endpoints and folders, validate SFTP host keys, and confine uploaded return images to approved user attachments.

Risk: The portal return flow is browser-driven and the final return submission path is not fully implemented in this artifact.

Mitigation: Treat return output as a dry-run preview unless the final submission path has been reviewed, captured, and explicitly approved for a real return.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-sanmar)
- [SanMar](https://www.sanmar.com)
- [Examples](references/examples.md)
- [Authentication and patterns](references/auth_and_patterns.md)
- [Web services](references/web_services.md)
- [Purchase orders](references/purchase_orders.md)
- [Invoicing](references/invoicing.md)
- [Shipment status](references/shipment_status.md)
- [FTP feeds](references/ftp_feeds.md)
- [Returns flow notes](references/returns_flow_notes.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from CLI tools, with Markdown guidance and shell command examples for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls read JSON from stdin and emit a single JSON object on stdout; failures return structured error objects.]

## Skill Version(s):

0.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
