## Description: <br>
Install and use ClawPolicy, an explainable autonomous execution policy engine for low-touch, auditable agent execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DZMing](https://clawhub.ai/user/DZMing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install ClawPolicy, initialize project-local policy storage, inspect policy state, review risky or suspended policies, and call the package's Python API for confirmation and policy export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses the upstream clawpolicy package from PyPI, so users depend on the trustworthiness of that package release. <br>
Mitigation: Install only when the upstream package is trusted; in stricter environments, pin the package version before use. <br>
Risk: Initialization creates or updates project-local .clawpolicy files that can affect later policy-supervised agent behavior. <br>
Mitigation: Review generated .clawpolicy contents after initialization and before relying on policy supervision. <br>


## Reference(s): <br>
- [ClawPolicy upstream repository](https://github.com/DZMing/clawpolicy) <br>
- [Upstream README](references/upstream-README.md) <br>
- [Upstream README (Chinese)](references/upstream-README.zh-CN.md) <br>
- [Upstream changelog](references/upstream-CHANGELOG.md) <br>
- [Upstream security policy](references/upstream-SECURITY.md) <br>
- [ClawHub skill page](https://clawhub.ai/DZMing/clawpolicy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and Python API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3, pip3, the clawpolicy CLI, and project-local .clawpolicy policy files.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
