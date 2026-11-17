## Description:

Track FUTA Express (Phuong Trang) package delivery status using their public API when the user provides a tracking code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongtanhieu](https://clawhub.ai/user/tongtanhieu)

### License/Terms of Use:


## Use Case:

External users and support agents use this skill to look up FUTA Express shipment status, route, fees, service details, and delivery history from a tracking code. It is intended for Vietnamese-language package tracking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may display personal shipment information, including phone numbers and government ID fields, for anyone who supplies a valid tracking code.

Mitigation: Mask phone numbers and identity fields by default, and limit output to shipment status, route, timestamps, and non-sensitive service details unless the user is authorized to view more.

Risk: Tracking-code lookups can expose sender, receiver, and delivery details beyond basic shipment status.

Mitigation: Ask the user to confirm they are authorized to view the shipment before presenting sensitive sender, receiver, or delivery-recipient details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tongtanhieu/skills/futa-tracker)
- [FUTA Express public tracking endpoint](https://api.futaexpress.vn/bo-operation/f1/full-bill-by-code-public/<tracking_code>)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Vietnamese Markdown tracking summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FUTA Express tracking code; preserves Vietnamese values and formats shipment fields for readability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
