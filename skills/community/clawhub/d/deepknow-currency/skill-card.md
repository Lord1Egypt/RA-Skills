## Description: <br>
DeepKnow Currency helps agents query and convert CNY exchange rates for USD, EUR, JPY, and GBP, and can create paid JD clawtip-backed orders for exchange-rate alerts and forecast services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oicqren](https://clawhub.ai/user/oicqren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current CNY exchange rates, convert amounts involving CNY, and request paid alert or forecast services through the InkRate backend and JD clawtip payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The paid-service flow can trigger real JD clawtip charges and may require JD login, payment password, bank verification, or risk checks. <br>
Mitigation: Confirm the charge and intended service before payment, and reuse the same order number while payment is processing instead of creating duplicate orders. <br>
Risk: Payment-linked order data and service questions are sent to the InkRate backend and stored in local order files. <br>
Mitigation: Use the default HTTPS endpoint unless you control the replacement host, avoid unnecessary personal or financial details in paid-service questions, and periodically delete old local order files. <br>


## Reference(s): <br>
- [ClawHub DeepKnow Currency listing](https://clawhub.ai/oicqren/deepknow-currency) <br>
- [InkRate public endpoint](https://rate.feedai.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output, JSON service results, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote and conversion commands return fixed key-value lines; paid fulfillment returns PAY_STATUS lines and may include JSON results.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
