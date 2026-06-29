## Description: <br>
A Stock Monitor helps agents guide A-share quantitative market monitoring, market sentiment scoring, stock selection, real-time price checks, leaderboard review, web UI setup, and cron-based updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifengwang333-ai](https://clawhub.ai/user/shifengwang333-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and trading-tool operators use this skill to configure and operate an A-share stock monitoring workflow with market sentiment analysis, stock screening guidance, real-time price checks, and scheduled data updates. Outputs should be treated as informational market-analysis support, not professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses trading recommendations and market signals that could be mistaken for professional financial advice. <br>
Mitigation: Treat outputs as informational only and independently verify market data, signals, and decisions before acting. <br>
Risk: The optional cron task can run recurring commands during trading hours. <br>
Mitigation: Review the cron payload, schedule, timezone, and local skill path before enabling automation. <br>
Risk: The published artifact references scripts and a web UI that are not included in the artifact. <br>
Mitigation: Confirm required files are present in the installed environment before relying on setup, monitoring, or web UI instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shifengwang333-ai/skills/a-stock-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/shifengwang333-ai) <br>
- [Author blog](https://www.cnblogs.com/Jame-mei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration examples, and API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock-monitoring setup steps, cron commands, Flask endpoint descriptions, and trading-signal interpretation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact text references 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
