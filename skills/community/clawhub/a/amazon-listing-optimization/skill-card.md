## Description: <br>
Amazon listing builder and optimizer for sellers that creates keyword-optimized listing copy, audits existing listings, checks keyword coverage, and compares listings against competitors across 12 Amazon marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and marketplace operators use this skill to create Amazon-ready listing copy from product attributes, keyword lists, and competitor ASINs, or to audit and rewrite existing listings for stronger keyword coverage and conversion signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Amazon and web-search requests may expose ASINs, URLs, keywords, marketplaces, product plans, or competitor targets entered by the user. <br>
Mitigation: Use only public or non-confidential listing inputs, and avoid entering product plans or competitor targets that should remain private. <br>
Risk: Generated listing copy or audit recommendations may be inaccurate, incomplete, or unsuitable for Seller Central policy requirements. <br>
Mitigation: Review and edit all generated titles, bullets, descriptions, backend search terms, and recommendations before publishing them in Seller Central. <br>
Risk: Release provenance is unavailable, so the upstream source cannot be confirmed from server-resolved import metadata. <br>
Mitigation: Verify the source and release terms before installing or relying on the skill in a production seller workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/amazon-listing-optimization) <br>
- [Amazon Keyword Research companion skill](https://github.com/nexscope-ai/Amazon-Skills/tree/main/amazon-keyword-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with ready-to-use listing copy, keyword coverage tables, audit scores, recommendations, and occasional shell commands for fetching public Amazon listing data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include titles, bullet points, descriptions, backend search terms, before-and-after rewrites, competitor comparisons, and marketplace-specific language guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
