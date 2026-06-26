## Description: <br>
Code Metrics analyzes code quality metrics including lines of code by language, Python cyclomatic complexity, function and class counts, comment ratios, and largest file rankings across supported source languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnywang2001](https://clawhub.ai/user/johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a codebase for size, language mix, documentation density, function and class counts, and Python complexity hotspots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metrics reports can expose repository file paths, function names, and project structure. <br>
Mitigation: Run the skill only on projects intended for inspection, and review reports before sharing them. <br>
Risk: Broad activation wording may cause the skill to run for general code overview requests. <br>
Mitigation: Confirm the target directory and requested metrics before running repository-wide analysis. <br>


## Reference(s): <br>
- [Code Metrics on ClawHub](https://clawhub.ai/johnnywang2001/code-metrics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable terminal report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports file paths, function names, line counts, comment ratios, largest files, and Python complexity metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
