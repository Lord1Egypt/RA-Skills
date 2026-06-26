## Description: <br>
Monitors Cainiao logistics orders for delivery exceptions, alert severity, compensation estimates, and recommended handling steps based on the skill's stated platform rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal control and logistics operations users use this skill to review single or batch shipment records, classify logistics exceptions, estimate compensation exposure, and prepare advisory next steps for follow-up. <br>

### Deployment Geography for Use: <br>
Global, with platform-rule verification for each operating region. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend supplier scoring, violation records, inter-skill handoffs, customer or carrier outreach, limit assessments, compensation execution, or pausing new orders. <br>
Mitigation: Require human approval before any supplier scoring, violation recording, outreach, compensation action, order pause, or operational handoff. <br>
Risk: Logistics rules and compensation estimates may be stale, incomplete, or unsuitable for a real case. <br>
Mitigation: Verify the cited platform rules, compensation caps, and case facts before using the report for decisions involving customers, carriers, or suppliers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/03-logistics-alert) <br>
- [Continuation examples](references/continuation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown logistics alert reports with optional structured JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes exception codes, alert severity, compensation estimates, risk summaries, and recommended handling steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
