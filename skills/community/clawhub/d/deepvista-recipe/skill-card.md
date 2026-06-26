## Description: <br>
DeepVista Recipe manages structured executable workflows called Recipes and runs them through an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to discover, list, inspect, run, export, and install DeepVista Recipe workflows from the DeepVista CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the DeepVista CLI package and the `deepvista-shared` skill for authentication and profiles. <br>
Mitigation: Install only after trusting DeepVista and review `deepvista-shared` before use. <br>
Risk: `recipe run` and `recipe install` are write actions that can create DeepVista content or start agent workflows. <br>
Mitigation: Confirm with the user before running write commands and present resulting DeepVista recipe URLs after write operations. <br>


## Reference(s): <br>
- [DeepVista CLI](https://cli.deepvista.ai) <br>
- [Deepvista Recipe on ClawHub](https://clawhub.ai/jingconan/deepvista-recipe) <br>
- [jingconan publisher profile](https://clawhub.ai/user/jingconan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and DeepVista CLI output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recipe run output may stream as NDJSON from the DeepVista CLI.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
