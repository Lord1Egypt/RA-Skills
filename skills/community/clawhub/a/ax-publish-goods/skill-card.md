## Description:

翱象（淘宝闪购）发品接口，支持批量创建商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigmountains](https://clawhub.ai/user/bigmountains)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to publish retail product SKUs in bulk to the Aoxiang/Taobao Flash Sale platform and to generate the API signing values required for those requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch publishing can change a real merchant account at scale.

Mitigation: Test with non-production merchant and store codes first, use least-privilege credentials, and require explicit approval before any batch publish run.

Risk: API credentials are required for request signing.

Mitigation: Keep secrets in environment variables or a secret manager and avoid embedding live credentials in examples, prompts, or committed files.

Risk: Incorrect SKU, barcode, or price data could publish invalid product records.

Mitigation: Validate SKU uniqueness, barcode lists, and price units in cents before submitting batch requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigmountains/skills/ax-publish-goods)
- [Publisher profile](https://clawhub.ai/user/bigmountains)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell examples plus JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires merchant/store identifiers, SKU data, and API credentials handled outside the skill text.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
