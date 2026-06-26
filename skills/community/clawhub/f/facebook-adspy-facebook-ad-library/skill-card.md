## Description: <br>
Research Facebook ad creatives and Meta Ad Library results using PipiAds adspy and ad library tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing researchers use this skill for one-off Facebook ad research, including finding ads, advertisers, products, creatives, landing pages, and Meta Ad Library records through PipiAds tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill globally installs and runs a third-party npm MCP server. <br>
Mitigation: Vet the npm package before deployment and consider running it in a contained environment. <br>
Risk: The MCP server receives access to the PipiAds API key for service calls. <br>
Mitigation: Use a dedicated or least-privilege API key and rotate or revoke it if usage looks abnormal. <br>
Risk: PipiAds API calls consume account credits and can affect billing. <br>
Mitigation: Ask users to narrow platform, region, keyword, and result limits before broad searches, and monitor PipiAds credit and billing usage. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fanyanggod/facebook-adspy-facebook-ad-library) <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [PipiSpy account and billing portal](https://www.pipispy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with tool-selection recommendations and PipiAds MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm and a PIPIADS_API_KEY; API calls consume PipiAds account credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
