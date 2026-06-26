## Description: <br>
Smart Model Switcher V3 helps an agent select and switch among configured third-party LLM providers and models based on task type, availability, fallback logic, and cost considerations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure intelligent runtime routing across purchased LLM provider plans, including provider key validation, model availability checks, task classification, fallback behavior, and cost-aware model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured task content may be routed to third-party LLM providers. <br>
Mitigation: Use only approved providers, avoid sending sensitive content unless policy permits it, and document which providers are enabled for each deployment. <br>
Risk: Provider API keys and purchased-plan access are required for validation and routing. <br>
Mitigation: Use limited-scope keys where available, set spend limits, rotate credentials regularly, and keep provider allowlists aligned with organizational policy. <br>
Risk: Background monitoring or external scripts referenced by the skill may affect local configuration or provider usage. <br>
Mitigation: Review scripts from the linked repository before execution, run them with least privilege, and test in a non-production workspace first. <br>
Risk: Model availability, cost, and fallback behavior depend on provider account state and purchased plans. <br>
Mitigation: Validate available models before use, monitor provider billing, and define fallback priorities that preserve expected task quality and data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/davidme6-smart-model-switcher-v3) <br>
- [Project homepage from ClawHub metadata](https://github.com/davidme6/openclaw/tree/main/skills/smart-model-switcher-v3) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe provider selection, API key validation, model availability checks, fallback choices, and cost-oriented routing for configured LLM providers.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata, SKILL.md frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
