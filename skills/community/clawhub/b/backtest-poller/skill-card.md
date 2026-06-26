## Description: <br>
Background daemon that monitors QuantConnect backtests with adaptive polling, real-time equity tracking, drawdown early-stop, auto-download, and auto-diagnosis while surviving terminal disconnection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to register QuantConnect backtests for background monitoring, progress checks, result download, and optional diagnosis without keeping a terminal session open. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports an unsafe macOS notification command path that could run local shell commands from crafted backtest text. <br>
Mitigation: Review and fix notification escaping before using with untrusted backtest names; avoid shell-like characters in names until patched. <br>
Risk: Early-stop permanently deletes QuantConnect backtests when the drawdown threshold is exceeded. <br>
Mitigation: Choose drawdown thresholds carefully and use early-stop only when deleting the backtest is acceptable. <br>
Risk: The skill uses real QuantConnect credentials from environment variables. <br>
Mitigation: Use a limited token if possible, keep credentials out of shared logs and files, and rotate tokens after testing or suspected exposure. <br>
Risk: Optional auto-diagnosis imports an external forensics module when available. <br>
Mitigation: Disable auto-diagnosis unless the imported forensics module is trusted. <br>


## Reference(s): <br>
- [Backtest Poller ClawHub release](https://clawhub.ai/tltby12341/backtest-poller) <br>
- [tltby12341 publisher profile](https://clawhub.ai/user/tltby12341) <br>
- [QuantConnect API v2 endpoint](https://www.quantconnect.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands plus local state, log, JSON, CSV, and diagnosis text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and QuantConnect environment variables QC_USER_ID, QC_API_TOKEN, and QC_PROJECT_ID; intended for macOS and Linux.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
