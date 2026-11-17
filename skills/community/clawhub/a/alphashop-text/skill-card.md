## Description:

AlphaShop text processing API toolset for text translation, multilingual product selling-point generation, and multilingual product title generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce developers use this skill to translate product text and generate multilingual listing copy for AlphaShop-supported marketplaces through the AlphaShop API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for translation or product-copy generation is sent to AlphaShop's remote API.

Mitigation: Use the skill only for text approved for AlphaShop processing, and avoid submitting secrets, customer data, or sensitive business text unless authorized.

Risk: The skill requires AlphaShop API credentials.

Mitigation: Use dedicated API keys, keep them out of source control, and provide them through environment configuration.

Risk: Dependency ranges are not pinned exactly.

Mitigation: Pin dependency versions before reproducible or controlled deployments.

## Reference(s):

- [AlphaShop Text API Reference](references/api-docs.md)
- [AlphaShop API Base URL](https://api.alphashop.cn)
- [AlphaShop API Key Management](https://www.alphashop.cn/seller-center/apikey-management)
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/alphashop-text)
- [Publisher Profile](https://clawhub.ai/user/1688aiinfra)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AlphaShop API credentials in ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
