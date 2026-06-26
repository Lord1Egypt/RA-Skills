## Description: <br>
Aky Select screens A-share stocks across nine technical and fund-flow dimensions using AkShare market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a command-line A-share stock screener that filters candidates by price movement, market cap, turnover, volume, moving averages, relative strength, VWAP behavior, and three-day fund flow. Its output is intended as a technical screen and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screening results may overstate one of the stated conditions or include stocks that fail or lack the VWAP or average-price condition. <br>
Mitigation: Treat the output as a technical screen, verify the underlying conditions before acting, and do not treat the results as investment advice. <br>
Risk: The skill fetches public market data through AkShare and depends on external data availability and freshness. <br>
Mitigation: Install only if AkShare-based public market data access is acceptable, and rerun or cross-check results when data is delayed or unavailable. <br>
Risk: The optional cron command creates recurring weekday runs. <br>
Mitigation: Add the cron entry only when recurring runs are desired, and remove it from crontab when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangfromchu-ai/aky-select) <br>
- [Aky Select homepage](https://github.com/aky/aky-select) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text tables and Markdown instructions with bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May take about 60-90 seconds across the full A-share universe and depends on live public market data availability.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
