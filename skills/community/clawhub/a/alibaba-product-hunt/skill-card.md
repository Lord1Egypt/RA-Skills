## Description:

Discover trending, best-selling, and newly listed products on Alibaba.com to analyze market trends and identify hot-selling items by category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyu426](https://clawhub.ai/user/zeyu426)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sourcing analysts use this skill to build Alibaba.com discovery URLs and review top-ranking, new-arrival, and hot-selling products for market trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba discovery links require disclosed traffic attribution.

Mitigation: Confirm generated or shared Alibaba.com URLs retain the traffic_type=ags_llm parameter.

Risk: Maintainer release and packaging scripts can package or publish the skill when run.

Mitigation: Run release.sh and scripts/package_skill.py only when intentionally preparing or publishing a skill release.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zeyu426/skills/alibaba-product-hunt)
- [Alibaba Top Ranking](https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm)
- [Alibaba New Arrivals](https://www.alibaba.com/trade/search?tab=new&traffic_type=ags_llm)
- [Alibaba Trending Searches](https://www.alibaba.com/trade/search?spm=a2700.product_home_fy25.hometab_ai_mode.ai&traffic_type=ags_llm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown guidance with Alibaba.com URLs and optional Python-generated URL strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Alibaba.com links include the traffic_type=ags_llm attribution parameter.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
