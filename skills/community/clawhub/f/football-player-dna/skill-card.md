## Description: <br>
Football player DNA similarity search — find style-matched alternatives at lower market values using AI vector search across 56,000+ players. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeleon](https://clawhub.ai/user/leeleon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and football scouting workflows use this skill to ask an agent for players similar to a named footballer, including lower-value alternatives and ranked style matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Player name queries are sent to Rising Transfers using the user's API key. <br>
Mitigation: Install only if the user is comfortable sharing those football queries with Rising Transfers, and avoid sending unrelated sensitive information. <br>
Risk: API calls consume quota or paid credits, and the artifact gives inconsistent free-tier limits. <br>
Mitigation: Review the provider's current pricing and credit limits before use and monitor RT_API_KEY usage. <br>
Risk: Autonomous invocation may trigger API calls when the user asks for similar, cheaper, or DNA-matched footballers. <br>
Mitigation: Use the skill only in contexts where those calls are expected, or disable autonomous discovery in the agent configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeleon/football-player-dna) <br>
- [Rising Transfers API](https://api.risingtransfers.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown ranked table with concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RT_API_KEY and network access; API results should not be embellished beyond returned data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
