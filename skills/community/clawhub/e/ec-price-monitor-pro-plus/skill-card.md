## Description: <br>
EC Price Monitor Pro compares prices across Taobao, Pinduoduo, JD, and Amazon, supports scheduled monitoring, price-difference alerts, and price history tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[since198905](https://clawhub.ai/user/since198905) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and commerce operators use this skill to monitor product prices across Taobao, Pinduoduo, JD, and Amazon, track 30-day price history, and receive configured price-difference or target-price alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hourly product searches may send monitored keywords to Taobao, Pinduoduo, JD, or Amazon. <br>
Mitigation: Use the skill only for keywords you are comfortable sharing with the listed shopping sites. <br>
Risk: Configured Feishu or Telegram notifications may send alert content to those services. <br>
Mitigation: Leave notification credentials blank unless third-party alert delivery is acceptable. <br>
Risk: Local price history can reveal shopping interests. <br>
Mitigation: Treat the local price history database as sensitive shopping-interest data. <br>


## Reference(s): <br>
- [Configuration reference](references/config.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/since198905/ec-price-monitor-pro-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style text reports with command examples and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local price history records and optionally send configured alert text to Feishu or Telegram.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
