## Description: <br>
Runs a full equity research report for a stock by orchestrating local price, fundamentals, and market-news scripts with uv run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and agents use this skill when they need a unified stock report that combines price action, fundamentals, regional market context, and a concise overall take. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on three companion stock-analysis sub-skills and local Python finance dependencies. <br>
Mitigation: Confirm the companion sub-skills are installed from trusted sources and that uv-managed dependency installation is acceptable before use. <br>
Risk: Market-news collection can fail when a ticker is passed where a market scope is required. <br>
Mitigation: Use the documented market scope values such as US, EUROPE, JAPAN, SOUTH_KOREA, ASIA, GLOBAL, UK, GERMANY, or NETHERLANDS. <br>


## Reference(s): <br>
- [Equity Research Skill Page](https://clawhub.ai/youpele52/equity-research) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown report with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and three trusted companion stock-analysis sub-skills.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
