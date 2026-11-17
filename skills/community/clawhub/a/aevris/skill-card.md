## Description:

Scan every prompt for injection attacks, verify AI outputs for manipulation, intercept agent actions before execution, and detect MCP tool poisoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aevris-ai](https://clawhub.ai/user/aevris-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Aevris to add security scanning around user prompts, AI outputs, planned agent actions, MCP tool definitions, and documents before they affect an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, responses, documents, tool metadata, and planned actions may be sent to an external service.

Mitigation: Enable the skill only where users and administrators knowingly accept third-party scanning, and avoid confidential, regulated, proprietary, or secret-bearing work unless contractual, retention, redaction, and scoping controls are in place.

Risk: Remote security verdicts can control whether agent inputs, outputs, tool definitions, and actions proceed.

Mitigation: Review the skill carefully before installation and define human review or fallback handling for blocked, compromised, poisoned, or approval-pending verdicts.

Risk: The skill requires an AEVRIS_API_KEY credential.

Mitigation: Provide the key through environment or managed configuration and avoid embedding it in prompts, source files, or shared logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aevris-ai/skills/aevris)
- [Aevris Homepage](https://aevris.ai)
- [Aevris API Docs](https://aevris.ai/docs)
- [Aevris Comparison](https://aevris.ai/compare)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with bash and JSON examples; Aevris API responses are JSON verdicts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEVRIS_API_KEY and sends scanned content to https://api.aevris.ai.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
