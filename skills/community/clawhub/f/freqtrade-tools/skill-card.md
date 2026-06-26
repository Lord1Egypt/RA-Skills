## Description: <br>
Provides shell aliases and helper commands for Freqtrade workflows such as downloading market data, running backtests, monitoring logs, and controlling Docker Compose services across Linux, macOS, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and Freqtrade operators use this skill to set up reusable command shortcuts for market-data downloads, backtesting, service control, logs, status checks, and UI access. It is intended for agents helping users operate Docker Compose based Freqtrade environments while preserving explicit confirmation for live-trading control commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot-control commands can start, stop, or restart Freqtrade services that may be connected to live trading. <br>
Mitigation: Confirm whether the bot is in dry-run or live-trading mode and require explicit human approval before controlling live-trading services. <br>
Risk: The --erase option can delete locally downloaded market data before fetching a new range. <br>
Mitigation: Use --erase only when intentionally replacing local data, such as extending a download window that requires a clean range. <br>
Risk: Command Prompt batch templates are less robust around input validation and can be risky with untrusted inputs. <br>
Mitigation: Prefer the Bash/Zsh or PowerShell functions with validation, and avoid using cmd.exe batch templates with untrusted pair, strategy, timeframe, or erase values. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/djc00p/freqtrade-tools) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Bash/Zsh aliases](artifact/references/bash-zsh-aliases.md) <br>
- [Windows PowerShell and Command Prompt equivalents](artifact/references/windows-equivalents.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, PowerShell, and batch command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and Docker Compose; bot-control commands should be confirmed before use against live-trading configurations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
