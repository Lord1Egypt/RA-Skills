## Description: <br>
AI-powered Reddit seeding agent for founders that analyzes a product spec, maps relevant subreddits, finds real threads where target users need help, drafts personalized replies and DMs, and posts approved outreach via Reddit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xconal](https://clawhub.ai/user/0xconal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External founders and growth operators use this skill to find Reddit conversations where potential users are already expressing relevant needs, draft value-first outreach, require human approval, and monitor engagement after approved messages are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post replies and send DMs from a real Reddit account. <br>
Mitigation: Require explicit human review and confirmation before every outbound message, and use a dedicated Reddit account where possible. <br>
Risk: Reddit credentials and outreach history may expose account or personal-contact data if stored carelessly. <br>
Mitigation: Store secrets only in environment or secret storage, avoid putting credentials in prompts or files, and periodically delete campaign logs and contacted-user history. <br>
Risk: Outreach can violate subreddit rules or create unwanted unsolicited messages. <br>
Mitigation: Verify subreddit rules and DM norms before outreach, avoid sensitive contexts, respect opt-outs, and pause activity after removals or warnings. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/0xconal/acquire-first-1000-users-on-reddit) <br>
- [Publisher profile](https://clawhub.ai/user/0xconal) <br>
- [Playwright MCP package](https://www.npmjs.com/package/@playwright/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown research reports, ranked queues, drafted Reddit replies and DMs, approval summaries, action logs, and engagement reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval before outbound Reddit replies, DMs, or follow-ups are sent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
