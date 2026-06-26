## Description: <br>
Axiomata Skill Evaluator Zh evaluates OpenClaw agent skills with a five-dimension Axioma rubric and ISO 25010 structural checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit skill directories before release, review quality scores, and identify improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evaluation tools read local skill files and can scan sibling skill folders when run with broad options such as --all. <br>
Mitigation: Run the tools on specific intended skill directories by default and use broad scans only when reviewing sibling folders is intentional. <br>
Risk: Providing credentials is unnecessary for this local evaluator and could expose sensitive material in scanned files or reports. <br>
Mitigation: Do not provide credentials or secrets when using the skill, and review generated reports before sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text, Markdown guidance, and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local skill directories and does not require credentials.] <br>

## Skill Version(s): <br>
3.0.1 (source: ClawHub release evidence; artifact documentation mentions 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
