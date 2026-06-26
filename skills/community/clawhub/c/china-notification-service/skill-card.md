## Description: <br>
Implement multi-channel notification services for Chinese applications using WeChat Template Messages, WeChat Subscription Messages, SMS (Alibaba Cloud/Tencent Cloud), DingTalk Bot, Feishu Bot, and Email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design multi-channel notification dispatch for China-oriented applications, including WeChat messages, SMS through Chinese cloud providers, DingTalk and Feishu bots, email, priority routing, rate limits, and compliance controls. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Notification integrations may expose SMS keys, WeChat tokens, cloud credentials, or bot webhooks if copied into source or logs. <br>
Mitigation: Store credentials in secret management, avoid logging tokens and webhook URLs, and rotate any credential that may have been exposed. <br>
Risk: Production sends can violate consent, unsubscribe, template approval, or rate-limit requirements. <br>
Mitigation: Record user consent, support unsubscribe flows where required, use approved templates, enforce per-channel rate limits, and audit delivery status before production use. <br>
Risk: Provider APIs, template rules, and platform limits may change after the skill release. <br>
Mitigation: Validate generated implementation guidance against current WeChat, Alibaba Cloud, Tencent Cloud, DingTalk, and Feishu documentation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-notification-service) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript examples, checklists, and channel comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated implementation details should be reviewed against current provider policies before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
