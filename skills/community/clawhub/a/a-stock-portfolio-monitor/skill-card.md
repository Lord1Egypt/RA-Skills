## Description: <br>
A股持仓监控助手 - 每日自动持仓报告、止损止盈提醒、实时盈亏跟踪。适合个人投资者管理多只股票持仓。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunshinesdff](https://clawhub.ai/user/sunshinesdff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to configure and run local A-share portfolio tracking, end-of-day holdings reports, stop-loss or take-profit checks, and simple stock screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The menu launcher can turn typed stock fields into shell commands on the user's machine. <br>
Mitigation: Review before installing and avoid running scripts/run_monitor.py with copied or untrusted input unless the os.system calls are replaced with safe subprocess argument lists or direct Python calls. <br>
Risk: Holdings and cost basis are saved locally in a hidden file. <br>
Mitigation: Confirm the storage location and protect or delete local portfolio data according to the user's privacy requirements. <br>
Risk: The included package appears to be missing a module needed for portfolio analysis. <br>
Mitigation: Verify the package contents and runtime imports before relying on portfolio analysis output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunshinesdff/a-stock-portfolio-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local portfolio data is stored on the user's machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
