## Description: <br>
Calculates arithmetic, powers and roots, percentages, trigonometric and logarithmic expressions, and other math expressions with a bundled Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yukin1218](https://clawhub.ai/user/Yukin1218) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to compute mathematical expressions from the shell when a task needs deterministic numeric output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calculator input can execute arbitrary Python code when expressions are evaluated. <br>
Mitigation: Review before installing, avoid untrusted expressions, and replace expression evaluation with a strict math parser or AST allowlist before broader use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text calculation results with Markdown usage guidance and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Float results are rounded to 10 decimal places by the calculator script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
