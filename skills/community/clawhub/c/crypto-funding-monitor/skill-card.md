## Description: <br>
Monitors crypto project funding rounds and TGE activity from RootData and X, then sends scheduled or on-demand briefings through Telegram, Discord, or email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhdryanchang](https://clawhub.ai/user/zhdryanchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and crypto market operators use this skill to run a monitoring service that collects funding and token-generation-event signals, verifies paid requests, and delivers briefings to configured notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships a SkillPay API key and should be treated as containing a compromised payment secret. <br>
Mitigation: Rotate the key, remove bundled secrets from the package, and load replacement credentials from a protected environment or secret manager. <br>
Risk: Paid subscription activation and payment callbacks have weak controls. <br>
Mitigation: Restrict the service to trusted callers, add authentication, and verify payment callbacks with the payment provider before marking subscriptions active. <br>
Risk: The skill sends recurring messages through third-party notification channels. <br>
Mitigation: Confirm recipient opt-in, limit delivery to authorized destinations, and provide a reliable unsubscribe path before enabling recurring messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhdryanchang/crypto-funding-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/zhdryanchang) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [RootData](https://www.rootdata.com) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JSON API responses, shell commands, and notification briefings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces funding and TGE summaries for Telegram, Discord, email, and API callers; outbound delivery depends on configured credentials and third-party service availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
