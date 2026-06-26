## Description: <br>
Cutie lets an agent use a Cutie API key to retrieve crypto KOL signals, market news, profiles, strategy data, forum and chat content, and account-related information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fansen](https://clawhub.ai/user/fansen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to query Cutie crypto community data, compare or learn from KOL strategies, review signals, and manage selected account actions through REST and MCP calls. It is best suited for assisted information review and account-scoped Cutie workflows, not autonomous trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to account-scoped Cutie data, including account and chat information. <br>
Mitigation: Install only when the agent should use the user's Cutie API key, fetch private data only when needed, and avoid retaining account or chat details in memory. <br>
Risk: The skill can support write actions such as risk preference changes, follows, posts, and mentor subscriptions. <br>
Mitigation: Require the agent to repeat the exact requested account change and receive explicit confirmation before executing any write action. <br>
Risk: Crypto signals and KOL strategy data can be incorrect, incomplete, or unsuitable for the user's risk profile. <br>
Mitigation: Treat signals and strategy summaries as informational only and require independent human review before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fansen/cutie) <br>
- [Cutie API homepage](https://server.tokenbeep.com) <br>
- [Cutie REST API base URL](https://server.tokenbeep.com/v1/app) <br>
- [Cutie MCP endpoint](https://server.tokenbeep.com/mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CUTIE_API_KEY, curl, and jq; MCP responses contain JSON strings that should be parsed before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and CLAWHUB.md version history, released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
