## Description: <br>
Use when the user wants to build, initialize, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, including project-structure refactors or starter skeletons that may separate model setup, prompt config, and orchestration, even if the request also mentions a UI, app shell, or local model service such as Ollama, and it is still unclear whether the solution should stay a single request, add supporting capabilities, or become orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maplemx](https://clawhub.ai/user/Maplemx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn broad business, product, refactor, or model-app requests into Agently-native capability paths and project boundaries before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer broad model-app planning requests toward Agently even when the user did not name a framework. <br>
Mitigation: Ask for framework-neutral guidance or name a different framework when Agently-centered routing is not desired. <br>
Risk: Planning guidance could still produce incorrect project boundaries or unsuitable capability routing for a specific environment. <br>
Mitigation: Review generated plans before implementation and validate settings, prompts, workflow boundaries, and tests against the target project requirements. <br>


## Reference(s): <br>
- [Agently Playbook release page](https://clawhub.ai/Maplemx/agently-playbook) <br>
- [Capability Map](references/capability-map.md) <br>
- [Project Framework](references/project-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell command, and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code execution, persistence, credentials, or hidden actions are included in the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
