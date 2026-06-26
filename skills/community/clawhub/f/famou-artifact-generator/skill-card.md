## Description: <br>
Guides an agent through defining FaMou evolutionary tasks, clarifying requirements, and producing the required `problem.md`, `init.py`, `evaluator.py`, and `prompt.md` materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoM0](https://clawhub.ai/user/zhaoM0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams preparing FaMou experiments use this skill to turn an initial optimization, ML, or search task idea into a clear task definition and validated experiment materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local project files and overwrite named task files such as `problem.md`, `init.py`, `evaluator.py`, and `prompt.md`. <br>
Mitigation: Use it in a clean or version-controlled workspace and review file diffs before relying on the generated materials. <br>
Risk: The validation workflow may run generated Python code. <br>
Mitigation: Inspect generated code first and run validation in a restricted environment without unnecessary secrets or write access. <br>
Risk: Generated task materials can reflect incomplete requirements or incorrect assumptions if the clarification phase misses important constraints. <br>
Mitigation: Review `problem.md` and confirm the task definition, data assumptions, constraints, and scoring logic before implementation or evaluation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoM0/famou-artifact-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown task definitions, Python files, prompt text, and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces `problem.md`, `init.py`, `evaluator.py`, and `prompt.md`; the skill requires validation of `init.py` with `evaluator.py`.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
