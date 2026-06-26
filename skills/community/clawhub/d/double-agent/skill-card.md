## Description: <br>
DoubleAgent helps agents design generator-evaluator workflows that separate artifact generation from independent quality evaluation using structured rubrics, iteration loops, and real interaction patterns such as Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up dual-agent quality assurance loops for AI-generated software, content, or workflows. It gives agents a spec contract, generator and evaluator role separation, calibrated scoring rubrics, and iteration-loop patterns for improving outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper use may involve nested agent execution with broad local sandbox access or approval bypasses. <br>
Mitigation: Install only when that execution model is intended; prefer the documented no-yolo mode and review the skill before running helpers. <br>


## Reference(s): <br>
- [DoubleAgent ClawHub page](https://clawhub.ai/zmy1006-sudo/double-agent) <br>
- [Architecture reference](references/architecture.md) <br>
- [Evaluator prompt templates](references/evaluator-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python templates, prompt templates, shell command examples, and structured JSON evaluation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes evaluator calibration guidance, loop-control thresholds, and helper scripts that require adaptation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
