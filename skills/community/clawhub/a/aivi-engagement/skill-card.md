## Description: <br>
AIVI is an AI engagement layer for lead generation, contact centers, and customer re-activation that scores leads, launches voice and SMS outreach, and analyzes conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aivillc](https://clawhub.ai/user/aivillc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, contact center, and customer reactivation teams use this skill to qualify leads, score contactability, launch AI voice and SMS sequences, and review call outcomes. It should be used only where the user is authorized to process lead data and initiate outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles phone-number PII and related lead attributes that may be sent to AIVI. <br>
Mitigation: Use it only when authorized to process the lead data and when the organization has confirmed the required consent, privacy basis, and data-handling controls. <br>
Risk: The skill can launch real AI voice and SMS outreach that may incur charges or violate outreach rules if triggered accidentally or without consent. <br>
Mitigation: Require explicit user confirmation before starting paid outreach, verify opt-in and compliance requirements, and monitor AIVI billing controls. <br>
Risk: Economic indicators and recommendations are propensity signals, not verified facts about an individual. <br>
Mitigation: Treat enrichment and ML recommendations as decision support, review them before action, and avoid using them as sole grounds for sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aivillc/aivi-engagement) <br>
- [Publisher profile](https://clawhub.ai/user/aivillc) <br>
- [AIVI website](https://aivi.io) <br>
- [AIVI MCP endpoint](https://mcp.aivi.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with example prompts, connector setup commands, and structured tool-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include lead scores, phone validity, contactability, recommended actions, sequence status, and call outcome summaries.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
