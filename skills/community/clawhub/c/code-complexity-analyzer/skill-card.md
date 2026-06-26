## Description: <br>
Measure cyclomatic complexity, cognitive complexity, and structural metrics for Python, JavaScript/TypeScript, and Go code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze code quality, identify complex functions, find refactoring candidates, and generate reports for review or CI quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local analyzer reads source files from paths supplied by the user. <br>
Mitigation: Point it at specific project directories rather than broad personal folders. <br>
Risk: Threshold violations return a non-zero exit code and can fail automated checks. <br>
Mitigation: Review the configured thresholds and exit-code behavior before using it as a CI gate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with per-function complexity metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configurable thresholds for cyclomatic complexity, cognitive complexity, function length, parameter count, and nesting depth; exit codes distinguish no violations, threshold violations, and no analyzable files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
