## Description: <br>
ClawTip helps agent workflows handle ClawTip payment requests, create payment tokens, show wallet access, and display ClawTip skill information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[117788abc](https://clawhub.ai/user/117788abc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to complete ClawTip payment flows, create payment user tokens, and access wallet or skill information when a valid user or third-party skill request is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real payment and wallet actions may be triggered through third-party skill flows or ambiguous user phrases. <br>
Mitigation: Require visible user confirmation for each payment, including caller, merchant, amount, order number, and limits, before using real funds. <br>
Risk: The workflow depends on a pinned npm CLI package and networked payment services. <br>
Mitigation: Install only when the publisher and pinned CLI package are trusted, and keep the package version pinned to the reviewed release. <br>
Risk: Authorization or wallet flows can expose temporary payment links or QR-code paths to the user. <br>
Mitigation: Present authorization links only for immediate user action and avoid storing or logging tokens, credentials, or payment URLs. <br>


## Reference(s): <br>
- [ClawTip official site](https://clawtip.jd.com) <br>
- [ClawTip wallet entry](https://clawtip.jd.com/qrcode?bizUrl=https://jpay.jd.com/ecnya2a/claw/index) <br>
- [ClawHub skill page](https://clawhub.ai/117788abc/clawtip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and payment or wallet status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment authorization links, wallet links, and MEDIA image paths for QR-code based user actions.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
