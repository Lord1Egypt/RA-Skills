## Description: <br>
This skill monitors Binance official announcements and @binance/@binancezh X activity, then queues Feishu notifications when new items are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xuhaoting](https://clawhub.ai/user/Xuhaoting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can run this skill to track Binance listing, delisting, trading rule, maintenance, campaign, and official X updates and route timely alerts to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release hardcodes a Feishu open_id in scripts and configuration examples, which can route notifications to an unintended recipient. <br>
Mitigation: Replace the hardcoded recipient and verify the runtime code loads the intended config.json before running the monitors. <br>
Risk: X account monitoring depends on r.jina.ai, sending monitoring requests through a third-party reader service. <br>
Mitigation: Confirm this dependency is acceptable for the deployment environment, or disable or replace the X monitor before use. <br>
Risk: The background monitors write local state and notification queue files. <br>
Mitigation: Run the skill from a controlled directory with appropriate file permissions and include state files in operational cleanup or backup procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xuhaoting/binance-announce-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/Xuhaoting) <br>
- [Binance announcement API](https://www.binance.com/bapi/composite/v1/public/cms/article/list/query) <br>
- [Jina AI Reader for @binance](https://r.jina.ai/twitter/binance) <br>
- [Jina AI Reader for @binancezh](https://r.jina.ai/twitter/binancezh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitor setup and operation guidance; runtime scripts write local state and notification queue files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
