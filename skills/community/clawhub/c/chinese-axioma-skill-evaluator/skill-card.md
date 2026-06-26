## Description: <br>
Axioma 技能评估系统 helps OpenClaw agents evaluate and improve skills with a five-dimension Axioma rubric, ISO 25010 checks, bundled evaluator scripts, and report guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill before publishing or revising OpenClaw skills to run structured quality checks, review scores, and identify improvement areas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hard-coded local host paths may make bundled commands fail or point at unintended locations. <br>
Mitigation: Review and adjust paths before running scripts, and execute evaluations only against explicit skill directories. <br>
Risk: Broad local skill discovery can scan more local skill directories than intended. <br>
Mitigation: Avoid broad scan modes such as --all unless that scope is intentional and acceptable. <br>
Risk: Bundled or generated approval statuses may be misleading while scoring logic and report output paths need review. <br>
Mitigation: Treat reports as advisory and manually verify quality gates before publishing or approving a skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-style text reports with inline shell commands and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory skill-quality reports and improvement guidance; results require human review before release decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
