## Description:

Detects the primary emotion in text input for AI agents and returns emotion type, intensity, valence, confidence, and a recommended response strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daisuke134](https://clawhub.ai/user/daisuke134)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to classify the emotional state of English or Japanese user-provided text before choosing an appropriate response strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emotionally sensitive text is sent to an external paid service.

Mitigation: Use only with explicit user consent, and avoid submitting names, secrets, credentials, or unnecessary personal details.

Risk: The skill runs an npm payment client for paid x402 requests.

Mitigation: Run the payment client in a constrained environment with a dedicated low-limit wallet when possible.

Risk: Critical emotional states may require escalation beyond a normal agent response.

Mitigation: When safe_t_flag is true, stop the normal flow and present appropriate emergency support resources.

## Reference(s):

- [Emotion Detector Skill Page](https://clawhub.ai/daisuke134/skills/emotion-detector)
- [Emotion Detector API Endpoint](https://anicca-proxy-production.up.railway.app/api/x402/emotion-detector)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON response with emotion labels, intensity, valence, confidence, response strategy, and safe_t_flag; documentation includes Markdown with a bash invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input text is limited to 2000 characters; optional context is limited to 500 characters; supported language values are en and ja.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
