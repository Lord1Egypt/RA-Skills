## Description: <br>
Guides an agent through fixed-budget machine-learning experiment cycles by editing training code, running experiments, evaluating metrics, and recording results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML practitioners use this skill to let an agent run structured local research iterations against a training script, compare results under a fixed budget, and keep an experiment log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks an agent to edit and run local ML training code, which can consume CPU or GPU resources and change experiment files. <br>
Mitigation: Use a dedicated project or sandbox, set practical time and GPU limits, and review train.py changes before running them. <br>
Risk: Research goals, prompts, or experiment logs may expose sensitive information if users place secrets or private data in them. <br>
Mitigation: Keep secrets and private data out of program.md and experiment logs, and use sanitized data for experiments. <br>


## Reference(s): <br>
- [Research Program Baseline](artifact/program.md) <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/auto-research-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python code changes and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify train.py and produce experiment notes or logs when the workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
