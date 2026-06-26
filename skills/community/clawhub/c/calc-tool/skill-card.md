## Description: <br>
Perform mathematical calculations from the command line. Arithmetic, trig, and unit conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and command-line users use this skill to ask an agent for calculator commands and examples for arithmetic, trigonometric functions, grouping, and simple unit-conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted calculator expressions may execute arbitrary Python code. <br>
Mitigation: Use only trusted expressions until the evaluator replaces eval() with a constrained math parser or AST allowlist, and review the skill before installation. <br>


## Reference(s): <br>
- [Calc Tool on ClawHub](https://clawhub.ai/dinghaibin/calc-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command-line expressions and formatted numeric output examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
