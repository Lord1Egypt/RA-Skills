## Description: <br>
Automatically routes requests between local and cloud AI models based on task complexity and privacy, with auto-detection and context tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuldrone](https://clawhub.ai/user/yuldrone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route agent requests between configured local and cloud models, preferring local handling for sensitive prompts and stronger cloud models for complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact names the package and install command as ai-model-router while the server release is ai-model-router-v2. <br>
Mitigation: Confirm the ClawHub slug and publisher handle before installation or use. <br>
Risk: Regex-based privacy detection may not catch every secret or sensitive prompt. <br>
Mitigation: Force the primary/local model for private work and avoid relying on automatic detection as the only privacy control. <br>
Risk: Context tracking can store truncated conversation content in ~/.model-router/contexts.json. <br>
Mitigation: Review or delete the context file periodically when context tracking is enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuldrone/ai-model-router-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/yuldrone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; the router CLI can return text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write optional local model and context configuration under ~/.model-router when used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
