## Description:

AlphaShop新品选品SKILL generates market analysis and new-product recommendation reports from keywords and product filters for Amazon and TikTok cross-border commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, product researchers, and developers use this skill to search validated product keywords and generate AlphaShop market reports with opportunity scoring, competition analysis, and new-product recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and output-file handling need review before installation.

Mitigation: Install only when the AlphaShop service is trusted, configure API keys through trusted environment or OpenClaw settings, and avoid sourcing untrusted .env files.

Risk: Generated keyword and product report files may contain sensitive business data.

Mitigation: Store generated report JSON in access-controlled locations and review the contents before sharing.

Risk: Market recommendations depend on external AlphaShop API responses and may be incomplete, stale, or unavailable.

Mitigation: Review recommendations before business use and retry or adjust filters when the API returns timeout, empty recall, or keyword-risk errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/alphashop-sel-newproduct)
- [AlphaShop API reference](artifact/references/api.md)
- [AlphaShop API service](https://api.alphashop.cn)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Console summaries and saved JSON keyword or new-product report files, with Markdown-formatted analysis returned inside API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AlphaShop API credentials and writes results under output/alphashop-sel-newproduct/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog text mention 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
