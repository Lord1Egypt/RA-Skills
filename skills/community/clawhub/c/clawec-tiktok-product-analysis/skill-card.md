## Description:

Uses the ClawEC API to analyze TikTok Shop products, including channel mix, content format, paid versus organic traffic, daily trends, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to submit TikTok Shop product IDs or links to ClawEC and receive a structured product-analysis summary for market research and product evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided product IDs or links, selected region, log IDs, and authenticated request metadata to clawec.com.

Mitigation: Install and use only when ClawEC external API processing is acceptable for the target product-analysis workflow.

Risk: The ClawEC API key could be exposed if pasted into chat or hardcoded into scripts.

Mitigation: Set CLAWEC_API_KEY as an environment variable and avoid storing credentials in prompts, transcripts, or source files.

Risk: Authenticated requests may consume ClawEC account credits.

Mitigation: Confirm the intended product, region, and AI interpretation setting before submitting analysis requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-tiktok-product-analysis)
- [ClawEC API Base](https://www.clawec.com/api)
- [TikTok Product Analysis Search API](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search)
- [TikTok Product Analysis Logs API](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search/logs)
- [TikTok Product Analysis Detail API](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search/log/detail)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summary with optional JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a Chinese structured summary; optional AI interpretation is returned as Markdown when requested and available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
