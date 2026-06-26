## Description: <br>
Analyzes email headers to extract authentication, routing, and security metadata for threat detection and email forensics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and email administrators use this skill to submit raw email headers to an external API for authentication, routing, and suspicious-indicator analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email headers can contain personal data, internal routing details, or regulated information and are sent to an external analysis service. <br>
Mitigation: Redact unnecessary sensitive content, confirm authorization and data-handling terms, and avoid submitting real incident or production headers unless approved. <br>


## Reference(s): <br>
- [Email Header Analyser API Docs](https://api.mkkpro.com:8016/docs) <br>
- [Email Header Analyser API Route](https://api.mkkpro.com/security/email-header-analyser) <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/email-header-analyser) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, JSON] <br>
**Output Format:** [JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one raw email header string and returns extracted sender, routing, authentication, and suspicious indicator fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
