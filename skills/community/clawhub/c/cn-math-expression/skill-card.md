## Description: <br>
Evaluates mathematical expressions with common functions and constants through a local Python command-line helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows can use this skill to calculate trusted arithmetic and common math expressions when a lightweight local Python helper is appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evaluator uses Python eval on supplied expressions, which gives it broader execution behavior than a simple calculator should have. <br>
Mitigation: Use only trusted expressions, or replace the evaluator with a restricted parser before broad deployment. <br>
Risk: The security verdict is suspicious even though no malware or persistence evidence was reported. <br>
Mitigation: Review and scan the skill before installation, with specific attention to expression evaluation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-math-expression) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [JSON result objects and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an expression/result pair on success and an error object with exit code 1 on failure.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
