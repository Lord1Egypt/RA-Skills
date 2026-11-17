## Description:

AlphaShop Image helps agents call AlphaShop image-processing APIs for image translation, upscaling, object extraction, element detection and removal, cropping, virtual try-on, and model replacement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit product and model image URLs to AlphaShop for ecommerce image translation, enhancement, cleanup, cropping, virtual try-on, and model replacement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs and related processing parameters to AlphaShop's remote service.

Mitigation: Use only images approved for sharing with AlphaShop, avoid sensitive or regulated image content unless your organization has approved that use, and prefer short-lived public URLs.

Risk: AlphaShop API credentials are required for all calls.

Mitigation: Store access and secret keys in the agent configuration or secret manager, avoid logging them, and rotate or revoke them if exposed.

Risk: The Python runtime depends on external packages for HTTP requests and JWT signing.

Mitigation: Pin, audit, and update the Python dependencies before production deployment.

Risk: Calls can fail when the AlphaShop account has insufficient credits.

Mitigation: Stop the workflow on insufficient-balance errors and ask the user to replenish AlphaShop credits before retrying.

## Reference(s):

- [AlphaShop image-processing API reference](references/api-docs.md)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)
- [AlphaShop API usage and credits](https://www.alphashop.cn/seller-center/home/api-list)
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/alphashop-image)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AlphaShop access and secret keys; asynchronous try-on and model replacement tasks return task IDs that must be queried separately.]

## Skill Version(s):

1.0.1 (source: server evidence release version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
