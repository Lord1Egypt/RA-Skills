## Description: <br>
Finds, compares, and configures free or low-cost AI models across OpenRouter, Hugging Face, Groq, Google AI Studio, and Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to discover low-cost model options, compare providers, and update OpenClaw primary and fallback model settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auto and switch commands can change OpenClaw default and fallback model settings. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running configuration-changing commands and review the file afterward. <br>
Risk: Selected external providers may handle prompts and require API keys. <br>
Mitigation: Treat provider API keys and cloud model use as sensitive, and choose local Ollama models when prompts should stay local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SuCriss/free-model-finder) <br>
- [Platform details](references/platforms.md) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Groq](https://groq.com) <br>
- [Google AI Studio](https://aistudio.google.com) <br>
- [Hugging Face](https://huggingface.co) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with OpenClaw JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The auto and switch commands can update ~/.openclaw/openclaw.json; provider API keys are read from environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
