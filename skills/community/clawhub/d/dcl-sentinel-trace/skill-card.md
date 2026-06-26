## Description: <br>
Instruction-only PII detector and redactor for AI outputs that screens for emails, phone numbers, national IDs, payment data, crypto wallet addresses, IP addresses, and document identifiers within the agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, privacy reviewers, and compliance-focused agent users use this skill as a local checkpoint to detect and redact potential personal data before AI output is delivered, logged, or passed downstream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PII screening may miss sensitive data or over-flag benign content. <br>
Mitigation: Use the results as a review aid rather than proof of legal compliance or complete detection. <br>
Risk: Scanning real sensitive data may expose it to the agent environment's retention or logging controls. <br>
Mitigation: Avoid pasting unnecessary sensitive data and confirm the agent environment's privacy and logging settings before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daririnch/dcl-sentinel-trace) <br>
- [Fronesis Labs privacy policy](https://fronesislabs.com/#privacy) <br>
- [DCL Security Suite](https://hub.fronesislabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with a JSON-style detection report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports a COMMIT or NO_COMMIT verdict, detected categories, redacted samples, severity, counts, and categories checked.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
