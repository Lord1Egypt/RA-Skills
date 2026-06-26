## Description: <br>
BSC Dev Wallet Monitor watches specified BSC addresses for token-transfer activity and returns alerts, webhook notification payloads, history, and monitor-management responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mybusd](https://clawhub.ai/user/mybusd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor BSC wallet addresses associated with token launches or trading signals, receive webhook alerts, query monitor history, and stop active monitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes payment and platform credentials and includes deployment or publishing actions that are not necessary for normal monitoring use. <br>
Mitigation: Do not install or run deployment scripts until the publisher removes and rotates exposed credentials and separates deployment actions from end-user monitoring. <br>
Risk: Long-running wallet monitoring and webhook delivery can continue beyond the user's intended scope if duration and webhook ownership are not controlled. <br>
Mitigation: Use finite monitor durations and provide only webhook URLs you control. <br>
Risk: The documentation and implementation need clearer alignment on price, billing mode, and implemented safety checks. <br>
Mitigation: Confirm price, billing mode, and safety-check behavior before relying on alerts or payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mybusd/bsc-dev-monitor-v2) <br>
- [Publisher profile](https://clawhub.ai/user/mybusd) <br>
- [SkillPay](https://skillpay.me) <br>
- [BNB Smart Chain](https://www.binance.org/en/smart-chain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [JSON responses and Markdown documentation with JavaScript and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes monitor setup, history, stop, webhook notification, billing, and deployment-related examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json state 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
