## Description: <br>
Search Facebook Ad Library and Meta Ad Library data with PPSPY, including ads, advertiser stores, landing pages, and ad products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, ecommerce operators, and agents use this skill to search and analyze Facebook and Meta ad-library data from PPSPY, including ads, stores, products, landing pages, trends, placements, and advertiser relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external npm MCP server. <br>
Mitigation: Install only if you trust PPSPY and the ppspy-mcp-server package; use an isolated environment when limiting exposure from globally installed npm code matters. <br>
Risk: The PPSPY API key may grant paid account access and API calls can consume account credits. <br>
Mitigation: Use a PPSPY API key with only the access needed, monitor credit usage, and manage billing or recharge through PPSPY. <br>


## Reference(s): <br>
- [PPSPY](https://www.ppspy.com) <br>
- [PPSPY API](https://api.ppspy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/facebook-ad-library) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [Text responses and structured MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PPSPY_API_KEY, npm, and the ppspy-mcp-server@1.0.1 package; PPSPY search calls may consume account credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
