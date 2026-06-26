## Description: <br>
Free cognitive health check for AI agents via Cerebratech CogDx that sends 10-20 recent outputs with confidence scores to return one specific diagnostic finding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send manually selected recent agent outputs, confidence scores, and correctness labels to Cerebratech for a lightweight cognitive health check. The response provides one statistical finding and suggests follow-up diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent prompts and responses are sent to an external diagnostic API, which can expose secrets, personal data, customer data, proprietary code, regulated data, or confidential business information. <br>
Mitigation: Use only intentionally selected and manually curated samples; do not submit sensitive or confidential content. <br>
Risk: The security assessment reports limited consent, redaction, and data-handling safeguards for the external API workflow. <br>
Mitigation: Review before installing, invoke the skill explicitly, and make a separate decision before using any paid follow-up diagnostic. <br>


## Reference(s): <br>
- [CogDx Health Check API Reference](references/api.md) <br>
- [CogDx Health Check API endpoint](https://api.cerebratech.ai/cogdx-health) <br>
- [Project repository metadata](https://github.com/drkavner/cogdx) <br>
- [ClawHub release page](https://clawhub.ai/drkavner/cogdx-health) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Analysis, Guidance] <br>
**Output Format:** [Markdown with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least 10 recent outputs with prompt, response, stated confidence, and correctness fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
