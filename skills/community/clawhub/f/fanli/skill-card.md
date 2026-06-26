## Description: <br>
Fanli converts shopping links or Taobao command text into coupon or promotional purchase links, compares prices across supported Chinese shopping platforms, checks price history, and gives buying guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users use this skill to evaluate shopping links, find available coupons or promotional purchase links, compare prices across Taobao, Tmall, JD, Pinduoduo, Douyin, Vipshop, and Meituan, and receive price-history-based buying guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key for a third-party shopping service. <br>
Mitigation: Use a revocable, scoped API key and rotate or revoke it if the execution environment is shared or compromised. <br>
Risk: Product links and shopping command text are sent to a third-party service for parsing and conversion. <br>
Mitigation: Avoid submitting links that contain private account, session, or tracking tokens, and use the skill only when that external data flow is approved. <br>
Risk: Converted purchase URLs may be promotional or affiliate-style links. <br>
Mitigation: Treat generated purchase links as promotional, verify the final destination and price before buying, and disclose the promotional nature when relevant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/fanli) <br>
- [feima-lab Open Platform](https://platform.feima.ai/) <br>
- [convert output template](references/convert-output.md) <br>
- [compare-price output template](references/compare-price-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown shopping summaries and recommendations, with optional JSON or table command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FX_AI_API_KEY; sends product links to a third-party service; generated purchase URLs may be promotional or affiliate-style links.] <br>

## Skill Version(s): <br>
4.2.2 (source: evidence release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
