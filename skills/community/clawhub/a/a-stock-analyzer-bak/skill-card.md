## Description: <br>
Analyzes and screens A-share stocks using seven technical and financial conditions, then produces market summaries, candidate stock picks, and buy/sell guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nowly-echo](https://clawhub.ai/user/nowly-echo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to run A-share market scans, generate daily Markdown reports, and review suggested entries, targets, stops, and position sizing. It is intended as screening and analysis support, not as a substitute for independent financial review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can be sent to Feishu or DingTalk webhooks when push settings are enabled. <br>
Mitigation: Disable or remove webhook settings unless outbound report delivery is intentional and the configured destination has been reviewed. <br>
Risk: Stock recommendations may rely on defaulted or simulated financial values when source data is unavailable. <br>
Mitigation: Treat generated stock picks as unverified analysis and confirm financial data, assumptions, and suitability before acting on any recommendation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nowly-echo/a-stock-analyzer-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal text, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped Markdown reports and can send report summaries to configured Feishu or DingTalk webhooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
