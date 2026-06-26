## Description: <br>
Free AI Bot routes prompts across local Ollama models and configured free cloud AI providers with fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bo-Aibot](https://clawhub.ai/user/bo-Aibot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to ask questions through a local-first AI router and fall back to configured free cloud providers when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to Cloudflare or Groq when those providers are selected or automatic fallback reaches them. <br>
Mitigation: Use the Ollama provider for local-only prompts and avoid sending confidential data to cloud providers unless that use is acceptable. <br>
Risk: Cloud provider API tokens can be exposed through shared logs, shell history, or repositories. <br>
Mitigation: Keep Cloudflare and Groq tokens scoped, store them outside source control, and avoid printing them in shared logs. <br>


## Reference(s): <br>
- [Free AI Bot on ClawHub](https://clawhub.ai/bo-Aibot/free-ai-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local Ollama or configured cloud AI providers depending on provider selection and fallback behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
