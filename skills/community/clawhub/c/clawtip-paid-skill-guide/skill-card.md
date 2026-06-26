## Description: <br>
Guides developers through creating ClawTip paid skills, including local order creation, SM4 encryption, required order fields, and local testing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building OpenClaw or Hermes ClawTip paid skills use this guide to configure payment metadata, create encrypted local orders, run payment processing, and generate paid-service outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-payment testing can affect actual payments if the merchant, amount, order number, or skill version is wrong. <br>
Mitigation: Before running payment commands, verify the merchant/payTo value, amount, order number, skill version, and official platform payment status. <br>
Risk: A local payCredential field or payment error message alone may not prove that payment succeeded. <br>
Mitigation: Confirm payment status through the official platform or payment process instead of relying only on local order-file fields or error text. <br>


## Reference(s): <br>
- [ClawTip official developer guide](https://clawtip.jd.com/guide) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides implementation guidance; users should verify payment settings and payment status before running real-payment commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
