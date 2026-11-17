## Description:

Publishes plain text posts to Binance Square and can generate a daily Web3, AI, and macro news brief for posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renyuke-cn](https://clawhub.ai/user/renyuke-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish configured text posts, market commentary, and generated daily news briefs to Binance Square under their own Binance Square identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public content under the user's Binance Square identity.

Mitigation: Install only when that publishing authority is intended, and review generated posts before publication.

Risk: The skill asks users to configure a live Binance Square OpenAPI key.

Mitigation: Use a dedicated least-privilege API key, keep it out of tracked or shared files, mask it in outputs, and rotate it if exposure is suspected.

Risk: Scheduled posting can publish unattended public posts.

Mitigation: Enable cron posting only after accepting unattended publication risk, and prefer a review step for generated news briefs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renyuke-cn/skills/binance-square-publish)
- [Binance Square OpenAPI](https://www.binance.com/zh-CN/square/openapi)
- [Binance Square content posting endpoint](https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add)
- [6551 Web3 hot news API](https://ai.6551.io/open/free_hot?category=web3)
- [6551 AI hot news API](https://ai.6551.io/open/free_hot?category=ai)
- [6551 macro hot news API](https://ai.6551.io/open/free_hot?category=macro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline JSON, YAML, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plain text Binance Square post content and post links after successful publication.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
