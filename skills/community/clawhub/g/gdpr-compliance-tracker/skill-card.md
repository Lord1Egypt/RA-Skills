## Description: <br>
Assesses GDPR compliance readiness and generates gap analysis with remediation guidance for privacy, data subject rights, consent, DPIA, and international transfer reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security teams, privacy teams, and compliance reviewers use this skill to collect GDPR posture inputs, call ToolWeb's GDPR tracker API, and present a compliance score, gaps, and prioritized remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GDPR assessment inputs are sent to ToolWeb as third-party data sharing. <br>
Mitigation: Do not submit actual personal data, customer records, secrets, or unnecessarily detailed internal evidence; review ToolWeb privacy and billing terms before use. <br>
Risk: The skill requires a ToolWeb API key and successful API calls may be billed or rate limited. <br>
Mitigation: Store TOOLWEB_API_KEY securely, monitor usage, and handle 401, 422, and 429 responses before relying on the assessment output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/gdpr-compliance-tracker) <br>
- [ToolWeb API Portal](https://portal.toolweb.in) <br>
- [GDPR Tracker API Endpoint](https://portal.toolweb.in/apis/compliance/gdpr-tracker) <br>
- [ToolWeb Platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured assessment sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; API responses are summarized as compliance score, gaps, and priority actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
