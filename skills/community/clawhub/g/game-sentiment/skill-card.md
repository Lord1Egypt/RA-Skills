## Description: <br>
Automates game sentiment monitoring for mobile and PC games across public channels, classifies issues and severity, assigns likely owners, and generates actionable reports with P1 alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robin9plus1](https://clawhub.ai/user/robin9plus1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game operations, community, product, and QA teams use this skill to monitor player feedback after updates or during daily operations, identify negative sentiment spikes, and produce issue-focused reports with recommended owners and actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store third-party credentials and API keys for authenticated channels. <br>
Mitigation: Prefer public and official-API channels, use restricted or disposable credentials for authenticated channels, and review credential storage before installation. <br>
Risk: The skill automates logged-in forum access, including CAPTCHA handling, which may create account-risk or platform-policy concerns. <br>
Mitigation: Disable NGA CAPTCHA automation unless the account and platform-policy implications are acceptable. <br>
Risk: Reports and Feishu summaries may retain or transmit collected source links, player feedback, and issue summaries. <br>
Mitigation: Confirm what will be sent to Feishu and retained under game-sentiment-data before enabling report delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robin9plus1/game-sentiment) <br>
- [Channel Strategy](references/channel-strategy.md) <br>
- [Config Schema](references/config-schema.md) <br>
- [Report Templates](references/report-template.md) <br>
- [Severity Rules](references/severity-rules.md) <br>
- [Google Cloud Console API Credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and alert summaries, with JSON configuration and cited source links where available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write per-game reports under game-sentiment-data and send Feishu summaries or P1 alerts when configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
