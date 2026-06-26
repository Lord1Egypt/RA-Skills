## Description: <br>
Detects the primary emotion in text input for AI agents, returning emotion type, intensity, valence, confidence, and a recommended response strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Daisuke134](https://clawhub.ai/user/Daisuke134) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to classify the emotional state of English or Japanese text before choosing a response strategy. It is especially relevant when an agent needs to detect high-intensity emotions and decide whether to escalate to supportive resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzed text is sent to a disclosed third-party endpoint and may include sensitive emotional or crisis-related content. <br>
Mitigation: Use the skill only when the provider's data handling is acceptable, and avoid submitting highly private crisis-related content unless the user has approved that handling. <br>
Risk: Each request uses a paid x402 flow and may incur a $0.01 USDC charge. <br>
Mitigation: Require explicit approval for paid calls or configure spending limits before routine use. <br>
Risk: A critical `safe_t_flag` indicates grief, shame, fear, or despair that may need escalation. <br>
Mitigation: Stop the normal response flow when `safe_t_flag` is true and provide appropriate emergency or crisis-support resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Daisuke134/emotion-detector) <br>
- [Emotion Detector API endpoint](https://anicca-proxy-production.up.railway.app/api/x402/emotion-detector) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response with emotion fields and response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires x402 payment; input text is limited to 2000 characters and optional context is limited to 500 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
