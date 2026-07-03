## Description: <br>
Guides agents through downloading, verifying, training, adapting, and running inference with a ModelScope Fourier Neural Operator workflow for CFD and PDE surrogate modeling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onescience-ai](https://clawhub.ai/user/onescience-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap the OneScience/FNO_B ModelScope codebase, check runtime readiness, adapt structured CFD/PDE datasets, and run training or inference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to download and run external ModelScope model code, which may change outside this artifact. <br>
Mitigation: Resolve the downloaded path, inspect the codebase and entry points, and review the code before training on sensitive data. <br>
Risk: Authenticated ModelScope access may require MODELSCOPE_API_TOKEN. <br>
Mitigation: Provide credentials only when intentional, avoid exposing tokens in logs, and prefer unauthenticated access when sufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onescience-ai/skills/cfd-model-run) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to download external ModelScope code, inspect files, and adapt training configuration for user-provided datasets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
