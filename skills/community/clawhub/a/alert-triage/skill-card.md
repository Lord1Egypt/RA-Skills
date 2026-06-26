## Description: <br>
Normalize noisy notifications into a simple triage model: send now, batch later, ignore, suppress as duplicate, or escalate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wroadd](https://clawhub.ai/user/wroadd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and teams use this skill to classify noisy alerts by urgency, trust, actionability, audience, and timing. It helps draft reusable alert policies for paging, batching, suppression, escalation, quiet hours, and digest routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested suppression windows, escalation thresholds, or routing labels may not match a team's incident response process. <br>
Mitigation: Review the generated policy against local response procedures before adopting it. <br>
Risk: Prompts may include sensitive operational details such as secrets, private endpoints, or personal contact information. <br>
Mitigation: Use abstract placeholders and avoid sharing secrets, private endpoints, or personal contact details. <br>


## Reference(s): <br>
- [Policy patterns for alert-triage](references/policies.md) <br>
- [Worked examples for alert-triage](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/wroadd/alert-triage) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance, configuration] <br>
**Output Format:** [Markdown tables or concise bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized alert summaries, severity, outcome, audience, timing, rationale, suppression keys, and digest buckets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
