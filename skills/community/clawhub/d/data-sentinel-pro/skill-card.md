## Description: <br>
Data Sentinel Pro monitors webpages, product prices, and competitor updates and alerts users when tracked content changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anson125chen](https://clawhub.ai/user/anson125chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track selected webpages, prices, and content changes over time, with optional scheduled checks and alerts for changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert messages may send monitored URL details or change summaries to Telegram when Telegram credentials are configured. <br>
Mitigation: Use dedicated low-privilege Telegram credentials and avoid monitoring confidential or internal URLs unless external alert delivery is acceptable. <br>
Risk: Scheduled cron entries create ongoing outbound webpage checks and local monitor state. <br>
Mitigation: Review cron entries before enabling them and periodically remove stored monitor data that is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anson125chen/data-sentinel-pro) <br>
- [Publisher profile](https://clawhub.ai/user/anson125chen) <br>
- [Project homepage](https://asmartglobal.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; runtime alerts are text or HTML-formatted messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores monitor state locally and can send alert content to Telegram when user credentials are configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
