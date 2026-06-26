## Description: <br>
Generates China A-share market reports for pre-market briefings, intraday snapshots, and post-market reviews using Tushare, AKShare, and search fallback data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who follow China A-share markets use this skill to generate daily market briefings, intraday checks, post-market recaps, and next-session watchpoints. It is intended for market overview reporting, not individual stock picking or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled outbound report delivery is enabled by default and may send reports to linked messaging accounts. <br>
Mitigation: Review or disable the scheduled auto-push tasks before use, and confirm the intended messaging destination. <br>
Risk: The Tushare token may be stored in a local plaintext file. <br>
Mitigation: Protect the token file with restrictive local permissions, avoid sharing it, and rotate or remove the token if exposure is suspected. <br>
Risk: Generated financial commentary may include hardcoded or synthesized elements that are not fully sourced from live data. <br>
Mitigation: Verify market data and claims against live sources, and treat the report as informational rather than investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/china-a-stocks-daily-review) <br>
- [README.md](artifact/README.md) <br>
- [Tushare Pro API](http://api.tushare.pro) <br>
- [Tushare token page](https://tushare.pro/user/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain-text market reports and Markdown report files, with setup guidance and shell commands where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save local report_YYYYMMDD_*.md files and send reports to linked messaging channels when scheduled automation is enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and changelog mention 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
