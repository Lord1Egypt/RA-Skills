## Description: <br>
币安撸毛助手 displays current Binance earning and promotional activity information, including financial products, activity rewards, and airdrop previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckylion68](https://clawhub.ai/user/luckylion68) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch and summarize Binance promotional earning activities, rewards, financial products, and airdrop previews. It is oriented toward Chinese-region activity filtering and deadline-aware summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Promotional, airdrop, and earning activity details can change quickly or be incomplete. <br>
Mitigation: Treat the output as informational and verify offers, eligibility, and deadlines on official Binance pages before acting. <br>
Risk: The skill contacts Binance and alpha123.uk and saves Markdown reports under the OpenClaw workspace. <br>
Mitigation: Install only if this network access and local report persistence are acceptable, and configure OPENCLAW_WORKSPACE or HTTP_PROXY when needed. <br>
Risk: Default filtering favors Chinese-region activities and UTC+8 timing. <br>
Mitigation: Review region eligibility and deadline times against source pages for the user's locale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckylion68/binance-earning-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/luckylion68) <br>
- [Binance announcements](https://www.binance.com/zh-CN/support/announcement) <br>
- [alpha123.uk](https://alpha123.uk/zh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown activity summaries with links, dates, reward or APR fields, and optional local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance and alpha123.uk data; supports optional HTTP_PROXY and OPENCLAW_WORKSPACE environment variables.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata; artifact metadata reports 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
