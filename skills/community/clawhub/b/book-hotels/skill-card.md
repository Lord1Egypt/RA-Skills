## Description: <br>
Uses the RollingGo CLI to search hotels, filter results, retrieve hotel tags, and fetch room pricing for hotel comparison and booking workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longcreat](https://clawhub.ai/user/longcreat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find candidate hotels by destination, dates, budget, star rating, tags, and distance, then compare hotel details, room prices, policies, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo API key, and command-line API key usage can expose credentials in shell history or process listings. <br>
Mitigation: Prefer setting AIGOHOTEL_API_KEY as an environment variable or secure secret instead of passing --api-key in commands. <br>
Risk: Hotel searches share travel query details with the RollingGo service. <br>
Mitigation: Install and use the skill only if the user is comfortable sharing the necessary travel details with that service. <br>
Risk: Returned booking links can lead to purchases outside the agent environment. <br>
Mitigation: Review booking links and hotel details before completing any purchase. <br>


## Reference(s): <br>
- [RollingGo NPX reference](references/rollinggo-npx.md) <br>
- [RollingGo UV reference](references/rollinggo-uv.md) <br>
- [RollingGo homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [ClawHub release page](https://clawhub.ai/longcreat/book-hotels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and parsed RollingGo CLI results, usually JSON by default.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AIGOHOTEL_API_KEY for authentication; RollingGo outputs result data on stdout and errors on stderr, and may return booking URLs or hotel detail links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
