## Description:

A Stock Analyst.Bak helps agents analyze China A-share market quotes, fundamentals, stock screening criteria, watchlists, news, and monitoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaohaixin](https://clawhub.ai/user/zhaohaixin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for A-share market research, stock screening, portfolio watchlist review, news lookup, and alert setup using Eastmoney/DFCF data. Outputs should be treated as informational analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill auto-installs unpinned dependent skills by name.

Mitigation: Review the dependent skills before installation and pin or approve dependency versions where the deployment process allows it.

Risk: Stock queries, screening criteria, news searches, watchlist data, and monitoring commands may be sent to the external Eastmoney/DFCF API using the user's API key.

Mitigation: Use the skill only when that data sharing is acceptable, avoid submitting sensitive portfolio details unless needed, and confirm state-changing watchlist or alert actions manually.

Risk: The skill can provide market analysis and investment ranges that may be incorrect, delayed, or unsuitable for a user's circumstances.

Mitigation: Treat outputs as informational research, verify time-sensitive market data against authoritative trading sources, and avoid relying on the skill as personalized financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaohaixin/skills/a-stock-analyst-bak)
- [Eastmoney/DFCF Claw API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python code, shell commands, and API-backed analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Eastmoney/DFCF API key through MX_API_KEY or MX_SEARCH_API_KEY and depends on related ClawHub skills for data, search, screening, watchlist, and monitoring actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
