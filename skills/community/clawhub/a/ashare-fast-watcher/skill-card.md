## Description: <br>
A-Share millisecond-level market data watcher using Tencent direct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch A-Share market snapshots and monitor volatility, convertible-bond linkage, and ETF premium signals. Outputs are informational market signals and should not be treated as trading instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports underdocumented scanners and continuous polling. <br>
Mitigation: Review polling behavior and run only in an environment where repeated market-data requests are acceptable and stoppable. <br>
Risk: The release evidence reports shell-based local notifications. <br>
Mitigation: Avoid running daemon.py as-is on a workstation until notification behavior is reviewed or replaced with a safer local notification API. <br>
Risk: The skill emits financial-alert signals that may be mistaken for trading instructions. <br>
Mitigation: Treat outputs as informational signals and apply independent financial review before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenswj/ashare-fast-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/kenswj) <br>
- [Tencent quote API endpoint used by the skill](http://qt.gtimg.cn/q={codes}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON responses and console text from Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit local desktop notifications when the daemon is run on macOS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
