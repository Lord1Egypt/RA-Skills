## Description: <br>
Finds current shopping deals from SMZDM RSS, enriches selected items with Tavily price research, and generates Chinese purchase recommendations with historical-price context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Deals Hunter to collect China-market deal candidates, deduplicate recent items, enrich selected products with price context, and produce a Chinese Markdown report for review before shopping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill hard-codes local memory/report paths and Discord channel destinations, so an installation may write to user-specific locations or post to unintended channels. <br>
Mitigation: Review and configure the paths and Discord destinations before granting Tavily or Discord access, then run once in a dry-run or sandboxed environment. <br>
Risk: Deal recommendations depend on live RSS and search results, so prices, availability, coupons, and links may change quickly. <br>
Mitigation: Verify product pages, final checkout prices, coupon requirements, and regional restrictions before making purchases. <br>


## Reference(s): <br>
- [ClawHub Deals Hunter release page](https://clawhub.ai/sunnyhot/deals-hunter) <br>
- [SMZDM RSS feed](http://feed.smzdm.com) <br>
- [Manmanbuy price reference](https://cu.manmanbuy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Chinese Markdown deal report with product links, prices, recommendations, warnings, and optional manual-run commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Tavily API credentials; supports TAVILY_API_KEY and TAVILY_API_KEYS for price enrichment.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
