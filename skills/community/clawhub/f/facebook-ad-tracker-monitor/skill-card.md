## Description: <br>
Monitor Facebook advertisers, campaigns, products, landing pages, and copy changes using PipiAds monitoring tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and review ongoing Facebook advertiser monitoring tasks, including campaign, ad, product, landing page, copy, group, and notification tracking in PipiAds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PIPIADS_API_KEY for a PipiAds account. <br>
Mitigation: Install only when PipiAds access is intended, store the API key in the environment, and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Creating tasks, changing groups, saving notifications, and repeated API calls can affect account monitoring state and credit usage. <br>
Mitigation: Confirm the advertiser, monitoring scope, notification changes, and expected credit use before asking an agent to perform account-changing actions. <br>


## Reference(s): <br>
- [PipiAds](https://www.pipiads.com) <br>
- [PipiSpy account and API key portal](https://www.pipispy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/facebook-ad-tracker-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API Calls] <br>
**Output Format:** [Markdown with setup steps, workflow guidance, and tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm and PIPIADS_API_KEY for the PipiAds MCP server.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
