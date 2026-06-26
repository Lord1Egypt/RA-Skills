## Description: <br>
Assess data privacy compliance across 20 control areas with 63 controls covering governance, consent, security, breach response, vendor management, and cross-border transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, and privacy teams use this skill to collect privacy-control answers and request a ToolWeb-backed assessment of privacy readiness, audit preparation, GDPR/CCPA checklist coverage, and program maturity. It reports overall compliance, area scores, critical findings, and priority remediation actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privacy-control answers, optional notes, and a session ID are sent to ToolWeb.in under a ToolWeb API key. <br>
Mitigation: Send only information needed for the assessment, avoid unnecessary confidential details, and confirm organizational approval for third-party processing before use. <br>
Risk: Successful API calls may consume billable ToolWeb quota. <br>
Mitigation: Confirm the configured ToolWeb plan and expected call volume before running assessments. <br>
Risk: Partial assessments can produce incomplete or conservative results because unanswered areas may be scored as non-compliant. <br>
Mitigation: Label partial runs clearly and collect answers for all relevant control areas before treating results as a full compliance view. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krishnakumarmahadevan-cmd/data-privacy-checklist) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [Data Privacy Checklist API endpoint](https://portal.toolweb.in/apis/compliance/data-privacy-checklist) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown assessment report with area scores, prioritized findings, and remediation actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may consume ToolWeb quota.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
