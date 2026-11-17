## Description:

Ai Model Router automatically routes requests between configured AI models based on task complexity, privacy signals, and user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuldrone](https://clawhub.ai/user/yuldrone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route agent tasks between local and cloud AI models, favoring simpler or sensitive requests for the primary model and complex requests for a secondary model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy mode can route sensitive prompts to the primary model even when the primary model is cloud-configured.

Mitigation: Before entering secrets, verify that primary_model in ~/.model-router/models.json points to a local model.

Risk: Context tracking can store message snippets as local plaintext.

Mitigation: Disable context tracking for sensitive sessions or protect and periodically delete ~/.model-router/contexts.json.

Risk: An unpinned installer command or elevated install can increase supply-chain and local privilege risk.

Mitigation: Use a pinned installer version and run installation without elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuldrone/skills/ai-model-router)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text or JSON routing decision with model id, reason, confidence, and optional configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model, complexity score, privacy detections, and conversation context identifiers.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
