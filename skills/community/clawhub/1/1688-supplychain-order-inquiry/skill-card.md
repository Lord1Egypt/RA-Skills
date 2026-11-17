## Description:

Routes 1688 order inquiry tasks and Shopify or AliExpress SKU extraction requests, sending or querying merchant inquiries and returning SKU image/query JSON for supported product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agent users use this skill to ask merchants about existing 1688 orders, query inquiry responses, configure inquiry automation, and extract SKU image/query pairs from supported Shopify or AliExpress product pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses a 1688 access key.

Mitigation: Review credential handling before deployment, prefer environment-injected credentials, avoid committing local configuration files, and rotate keys if exposure is suspected.

Risk: The skill can send merchant inquiries and change inquiry automation settings.

Mitigation: Require clear user intent before write actions, keep final JSON responses for auditability, and limit execution to existing order contexts.

Risk: The skill can upload local files and fetch external product pages.

Mitigation: Restrict uploads to intended, validated image attachments and validate product or gateway destinations before execution.

Risk: The skill can install packages during execution.

Mitigation: Disable automatic dependency installation where possible and preinstall reviewed, pinned dependencies in the runtime.

Risk: The security evidence reports hidden Unicode in agent instructions.

Mitigation: Remove hidden Unicode before release and review instruction diffs with control characters visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-supplychain-order-inquiry)
- [Skill overview](artifact/SKILL.md)
- [Order inquiry send capability](artifact/references/capabilities/inquiry_send.md)
- [Order inquiry query capability](artifact/references/capabilities/inquiry_query.md)
- [Inquiry configuration capability](artifact/references/capabilities/inquiry_config.md)
- [AK configuration capability](artifact/references/capabilities/configure.md)
- [Shopify SKU extraction capability](artifact/references/capabilities/sku_extract_shopify.md)
- [AliExpress SKU extraction capability](artifact/references/capabilities/sku_extract_aliexpress.md)
- [Structured parameters reference](artifact/references/capabilities/structured-params.md)
- [Error handling reference](artifact/references/common/error-handling.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects or JSON arrays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final agent responses are unwrapped JSON; order inquiry outputs include task or status data, and SKU extraction outputs include image and query fields only.]

## Skill Version(s):

0.57.0 (source: server release evidence; artifact frontmatter says 0.50.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
