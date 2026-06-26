## Description: <br>
Automatically selects a local or cloud AI model based on prompt complexity to optimize request handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MyMrXu](https://clawhub.ai/user/MyMrXu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to classify prompt complexity and select an appropriate local Ollama or cloud model for the task. It is intended to balance cost, latency, and model capability when routing normal agent requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be evaluated by a configured Ollama service and complex tasks may be routed to cloud models. <br>
Mitigation: Use localhost or another trusted Ollama host, review models.json before use, and avoid sensitive prompts unless cloud routing is explicitly acceptable. <br>
Risk: Automatic model detection can change future routing behavior. <br>
Mitigation: Review model configuration after detection or update commands and pin approved local and cloud models before enabling the skill. <br>
Risk: The server security review flagged the release as suspicious because routing can use a hard-coded private-network Ollama server and cloud models without clear user control. <br>
Mitigation: Require installation review and configure explicit local and cloud routing policy before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MyMrXu/auto-model-selector) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [models.json](artifact/models.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns routing decisions with complexity, recommended model, reason, and cost metadata; model management commands can update local model configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files also reference 1.0.0 and 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
