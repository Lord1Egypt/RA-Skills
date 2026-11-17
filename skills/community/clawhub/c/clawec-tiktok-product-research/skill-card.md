## Description:

Uses the ClawEC API to analyze TikTok Shop category product opportunities, including recent best-seller rankings, product stage, entry-window signals, creator and video trends, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, analysts, and agents use this skill to research TikTok Shop categories, compare opportunity products, inspect competition and trend signals, and summarize AI interpretation when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends category queries, market parameters, log IDs, and authenticated requests to clawec.com.

Mitigation: Use only when ClawEC is an approved service for the research task and avoid entering sensitive business strategy details in category inputs unless the provider is trusted.

Risk: The skill requires a ClawEC API key for authenticated API calls.

Mitigation: Keep the key in the CLAWEC_API_KEY environment variable and do not hard-code it in prompts, scripts, or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-tiktok-product-research)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)
- [TikTok product opportunity search endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_opportunity/search)
- [TikTok product opportunity logs endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_opportunity/search/logs)
- [TikTok product opportunity detail endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_opportunity/search/log/detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON API responses, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include category match details, market overview metrics, top opportunity products, open entry-window products, and optional AI analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
