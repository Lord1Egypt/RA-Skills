## Description: <br>
Routes LLM requests to a local model first, validates local response quality, and escalates to a cloud model only when the local result fails or routing rules require it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelnishanth](https://clawhub.ai/user/joelnishanth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route prompts through local LLM providers when appropriate, validate local results, and fall back to cloud models when quality, complexity, or availability checks require escalation. It is also useful for tracking local-vs-cloud outcomes and estimated token cost savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud fallback can send prompts to a third-party model when local routing or validation fails. <br>
Mitigation: Review each cloud escalation before sending sensitive content, and keep the sensitivity routing and redaction behavior enabled when handling private material. <br>
Risk: Routing and savings metrics are stored locally until reset. <br>
Mitigation: Treat the local savings file as usage telemetry and reset or remove it when retention is not desired. <br>
Risk: The provider setup documentation includes an optional curl-pipe-to-shell Ollama install command. <br>
Mitigation: Prefer verified package-manager installation steps or inspect installer scripts before running them. <br>


## Reference(s): <br>
- [Routing & Validation Logic](references/routing-logic.md) <br>
- [Local LLM Provider Setup](references/local-providers.md) <br>
- [Token Estimation & Cloud Cost Reference](references/token-estimation.md) <br>
- [Adaptive Routing ClawHub Release](https://clawhub.ai/joelnishanth/adaptive-routing) <br>
- [llamafile Releases](https://github.com/Mozilla-Ocho/llamafile/releases) <br>
- [LM Studio](https://lmstudio.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces routing decisions, validation results, local provider checks, and a local savings dashboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
