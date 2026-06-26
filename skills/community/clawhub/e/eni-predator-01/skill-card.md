## Description: <br>
Analyzes A-share limit-up market data with AkShare, filters stocks with at least two consecutive limit-up days, and returns a markdown summary of key stock attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxfc888aa](https://clawhub.ai/user/gxfc888aa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to fetch current A-share limit-up pool data and produce a compact markdown table for market review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live AkShare market-data requests. <br>
Mitigation: Confirm network access and data-provider terms before installation or use. <br>
Risk: The artifact describes randomized delay behavior in connection-stability and anti-blocking terms. <br>
Mitigation: Do not use or modify the skill for aggressive scraping, rate-limit evasion, or provider rule bypass. <br>
Risk: Dependencies are listed without pinned versions. <br>
Mitigation: Pin and review dependency versions before controlled or production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gxfc888aa/eni-predator-01) <br>
- [Publisher profile](https://clawhub.ai/user/gxfc888aa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown table or plain text status/error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live AkShare market-data requests and applies a randomized delay before fetching.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
