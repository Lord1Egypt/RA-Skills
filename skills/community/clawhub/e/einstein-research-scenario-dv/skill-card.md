## Description: <br>
Analyzes news headlines into 18-month investment scenario reports with primary analysis, reviewer critique, sector impacts, stock ideas, and strategic positioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to turn a manually supplied market, policy, technology, commodity, or geopolitical headline into a structured Japanese investment scenario report. The report focuses on an 18-month horizon, sector sensitivity, stock ideas, alternative scenarios, and risk review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates stock suggestions and market scenarios that may be inaccurate, incomplete, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational analysis, not financial advice; independently verify prices, filings, assumptions, and risks before acting. <br>
Risk: The analysis depends on configured scenario-analyst and strategy-reviewer agents, so untrusted or misconfigured agents can affect report quality. <br>
Mitigation: Use explicit commands and verify that the configured analysis and review agents are trusted before running the skill. <br>
Risk: Market headlines and investment context may include confidential or nonpublic information. <br>
Mitigation: Avoid submitting confidential or nonpublic market information unless the runtime and configured agents are approved for that data. <br>


## Reference(s): <br>
- [Headline Event Patterns](references/headline_event_patterns.md) <br>
- [Scenario Playbooks](references/scenario_playbooks.md) <br>
- [Sector Sensitivity Matrix](references/sector_sensitivity_matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style Japanese scenario analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes headline analysis, first-, second-, and third-order effects, sector mapping, stock recommendations, reviewer critique, and an integrated action plan.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
