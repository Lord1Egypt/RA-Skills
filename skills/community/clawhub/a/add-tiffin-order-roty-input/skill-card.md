## Description: <br>
Parse "Roty input" messages from authorized Telegram users to create Roty tiffin orders via HTTPS POST without UI automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horngtan](https://clawhub.ai/user/horngtan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized vendors or operators use this skill in OpenClaw or Telegram to parse Roty tiffin order messages, calculate pricing, build order payloads, and submit orders or request missing address, date, or product details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create live orders by default, so malformed or unintended messages may submit real orders. <br>
Mitigation: Review before installing, use DRY_RUN=1 during validation, and add explicit confirmation before live order submission. <br>
Risk: The security summary reports under-disclosed browser automation and exposed credentials in the package. <br>
Mitigation: Remove or isolate the Playwright automation scripts and rotate any exposed account password before deployment. <br>
Risk: Order payloads and logs may contain personal customer data. <br>
Mitigation: Redact personal data from logs and restrict order, product, and allowlist operations to authorized users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horngtan/add-tiffin-order-roty-input) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Package manifest](artifact/package.json) <br>
- [OpenClaw routing manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [Plain text responses with JSON payloads for dry runs and HTTPS POST results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Triggered by Telegram messages containing "Roty input"; requires a sender ID and full inbound message.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
