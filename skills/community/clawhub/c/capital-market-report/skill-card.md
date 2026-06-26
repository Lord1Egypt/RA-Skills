## Description: <br>
Generates high-signal capital market anomaly and rumor reports from Chinese and global financial media, social scanners, and local price helpers, emphasizing actionable business signals, market isolation, and source URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market analysts, investors, and agent operators use this skill to gather recent financial news, scan rumors and price signals, compare against prior 24-hour reports, and draft concise capital-market reports with source URLs and explicit impact reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public market and news data and calls local finance helper skills, so generated reports can reflect stale, unavailable, or inconsistent upstream data. <br>
Mitigation: Review the cited source URLs, verify time windows and price data with trusted sources, and keep the required helper skills available before using the report. <br>
Risk: The workflow stores report and cache files under ~/.openclaw and includes cleanup behavior that can remove generated report history. <br>
Mitigation: Review or disable the cleanup command before use when report history matters, and back up retained reports outside the cleanup path. <br>
Risk: Network news fetching contacts multiple public finance and media endpoints. <br>
Mitigation: Run the skill only in environments where outbound public news and market-data requests are permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangzhe1991/capital-market-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown market report with source URLs, delta summary, event analysis, key calendar items, and hallucination checks; helper scripts may also write text reports and cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires recent source URLs, isolates market impact by region, and stores report or cache files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
6.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
