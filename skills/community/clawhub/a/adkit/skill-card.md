## Description: <br>
AdKit lets agents manage Google Ads and Meta Ads through the AdKit CLI or MCP, including creating and publishing campaigns, ad sets, ad groups, ads, drafts, media, keywords, audiences, ad library research, and AI-generated ads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeannen](https://clawhub.ai/user/jeannen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and advertising operators use this skill to execute Google Ads and Meta Ads account operations through AdKit after campaign strategy is already decided. The skill supports draft creation, human review, and publishing workflows for connected ad accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate connected Google Ads and Meta Ads accounts, including actions that may affect live campaigns and budgets. <br>
Mitigation: Install it only for intended ad-account operations and require explicit review of account, budget, targeting, creative, and draft IDs before publishing. <br>
Risk: The skill requires sensitive credentials or connected advertising account access. <br>
Mitigation: Use only approved AdKit authentication paths, protect ADKIT_API_KEY values, and confirm account connection status before issuing commands or tool calls. <br>
Risk: Raw platform API requests or platform overrides can perform native operations beyond the normalized AdKit workflows. <br>
Mitigation: Avoid raw platform API requests unless the exact native operation is understood, and use parameter discovery before mutations that have not been performed in the current session. <br>


## Reference(s): <br>
- [AdKit homepage](https://adkit.so) <br>
- [ClawHub skill listing](https://clawhub.ai/jeannen/adkit) <br>
- [Publisher profile](https://clawhub.ai/user/jeannen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with CLI commands, MCP tool calls, JSON parameter examples, and review links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or tool calls that create, mutate, review, or publish advertising drafts through connected Google Ads or Meta Ads accounts.] <br>

## Skill Version(s): <br>
0.2.3 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
