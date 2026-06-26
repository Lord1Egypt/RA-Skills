## Description: <br>
Automatically routes requests between two configured AI models based on task complexity, privacy needs, and user preferences for optimized AI usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuldrone](https://clawhub.ai/user/yuldrone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose between a primary local model and a secondary cloud model for a prompt, with privacy-sensitive prompts routed to the primary model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic routing may recommend a cloud model for work that the user intended to keep local. <br>
Mitigation: For sensitive work, force the primary local model and review the route decision before sending prompts to any external provider. <br>
Risk: Optional context tracking can store truncated prompt history locally. <br>
Mitigation: Review or delete ~/.model-router/contexts.json periodically when context tracking is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuldrone/ai-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text or JSON routing decisions with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model, route reason, confidence, complexity score, privacy indicators, and model configuration status.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
