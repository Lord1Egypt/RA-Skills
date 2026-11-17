## Description:

Manage and monitor a personal stock watchlist with support for adding, removing, listing stocks, and summarizing their recent performance using data from 10jqka.com.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a personal Chinese A-share watchlist, retrieve concise performance summaries, and manage stored stock entries by code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local watchlist under ~/.clawdbot/stock_watcher and clear or uninstall actions can remove watchlist data.

Mitigation: Back up the watchlist before using clear or uninstall operations.

Risk: Performance summaries depend on network access to 10jqka.com.cn and may be unavailable or delayed.

Mitigation: Treat returned market summaries as informational and verify important financial decisions against authoritative market data.

Risk: Python dependencies are installed outside the skill by the user environment.

Mitigation: Install requests and beautifulsoup4 in a virtual environment with pinned versions when deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-stock-watcher-pro)
- [10jqka stock pages](https://stockpage.10jqka.com.cn/{stock_code}/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update a local watchlist file and may fetch stock pages from 10jqka.com.cn.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
