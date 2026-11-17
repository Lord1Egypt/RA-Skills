## Description:

Create FBA inbound plans through Amazon SP-API v2024-03-20, including identical-box packing, placement selection, carrier booking, box-label download, and square-sticker formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-school](https://clawhub.ai/user/claw-school)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and operations agents use this skill to create and manage FBA Send to Amazon inbound workflows, choose carrier options, and produce shipment records and box labels. It is intended for accounts where the user can supply SP-API credentials and confirm seller-account decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact actions in a production Amazon seller account, including creating inbound plans and confirming transportation.

Mitigation: Review the plan configuration, carrier selection, placement option, and pickup contact with the account owner before running commands that modify the seller account.

Risk: Cancellation can destroy real inbound shipment workflows, and server evidence flags an unguarded cancellation path.

Mitigation: Use the guarded void_plan.py dry-run flow with an exact shipment fingerprint and only add --yes after a human verifies the plan and shipment IDs; avoid create_inbound_plan.py --void.

Risk: Weak API endpoint validation could direct credentialed SP-API calls away from the intended Amazon host.

Mitigation: Keep SPAPI_ENDPOINT on the official Amazon SP-API endpoint for the target marketplace and review environment variables before execution.

Risk: Driving a signed-in Seller Central browser gives an agent access to a live account session.

Mitigation: Prefer user-performed browser steps for SKU prep categories, and only allow browser control when the user explicitly intends that session use.

Risk: Generated result JSON and label PDFs contain sensitive business and shipment records.

Mitigation: Store output files in an access-controlled location and avoid sharing or committing generated shipment records, credentials, or label PDFs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claw-school/skills/fba-send-to-amazon)
- [Claw School homepage](https://claw-school.com)
- [Amazon Fulfillment Inbound API v2024-03-20 use-case guide](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-use-case-guide)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; scripts can produce JSON shipment records and PDF label files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SP-API credentials from environment variables or ~/.config/sp-api/credentials.json; label splitting and square formatting require PyMuPDF and numpy.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
