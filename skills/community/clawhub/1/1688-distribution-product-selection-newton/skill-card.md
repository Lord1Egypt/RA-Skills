## Description:

1688 Distribution Product Selection Newton helps distributors find 1688 products by keyword or image, evaluate candidates with distribution advisor data, and surface recommendation reasons and listing risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External distributors and ecommerce operators use this skill to search 1688 supply candidates, compare shipping and channel-support signals, and decide which products are suitable for listing or distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account keys and optional ISV tokens, which could expose credentials if used in an untrusted environment.

Mitigation: Review before installing, use only with a trusted 1688/OpenClaw account and network environment, and avoid optional ISV token commands until token output is redacted.

Risk: Transport and gateway configuration choices may weaken request security.

Mitigation: Prefer a version that restores TLS verification and validates the gateway URL before production use.

Risk: AK credentials may be persisted locally.

Mitigation: Store AK credentials with restrictive file permissions and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-distribution-product-selection-newton)
- [ClawHub Publisher Profile](https://clawhub.ai/user/1688aiinfra)
- [ClawHub AK Setup](https://clawhub.1688.com)
- [1688 AI Workbench AK Retrieval](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent)
- [Product Selection Reference](artifact/scripts/biz/product_selection/reference.md)
- [Distribution Advisor Reference](artifact/scripts/capabilities/offer_info/reference.md)
- [Test Report](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown recommendations with JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ALI_1688_AK; optional ISV token commands may cache tokens locally.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
