## Description: <br>
Manage and monitor a personal stock watchlist with support for adding, removing, listing stocks, and summarizing recent performance using data from 10jqka.com.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to maintain a local watchlist of Chinese A-share stocks, review saved symbols, and fetch concise performance summaries from 10jqka.com.cn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchlist is stored in plain text at ~/.clawdbot/stock_watcher/watchlist.txt. <br>
Mitigation: Do not store sensitive notes in the watchlist file and manage local file permissions according to the user environment. <br>
Risk: Clear and uninstall operations can remove saved watchlist entries without confirmation. <br>
Mitigation: Back up the watchlist before running clear_watchlist.py or uninstall.sh. <br>
Risk: Performance summaries depend on network access to 10jqka.com.cn and may fail or return delayed market data. <br>
Mitigation: Treat summaries as informational and verify important trading decisions against authoritative market data sources. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/williamwang-wh/claw-stock-watcher-pro) <br>
- [Publisher profile](https://clawhub.ai/user/williamwang-wh) <br>
- [10jqka stock page pattern](https://stockpage.10jqka.com.cn/{stock_code}/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text summaries and command-line output with stock codes, stock names, performance indicators, and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores watchlist entries as stock_code|stock_name in a local plain-text file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
