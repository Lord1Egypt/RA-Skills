## Description: <br>
Repo-aware questioning protocol for OpenClaw that increases clarification before acting on coding, project-build, architecture, debugging, and implementation tasks when requirements, repo context, constraints, interfaces, success criteria, or execution rigor are ambiguous. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hongyi3](https://clawhub.ai/user/Hongyi3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to make an agent inspect relevant repository context, assess ambiguity, and ask targeted clarification questions or produce a structured high-rigor question report before coding, build, architecture, debugging, or implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured clarification can slow coding or build work, especially with strict profiles. <br>
Mitigation: Choose an appropriate bundled or repo-local profile and review any .asking-until-100.yaml before use. <br>
Risk: Question reports and provisional project structures may reflect incomplete repo signals or unresolved assumptions. <br>
Mitigation: Review the working hypothesis, blocking dimensions, and decision-critical unknowns before acting on the report. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Hongyi3/asking-until-100) <br>
- [Readiness Protocol](references/protocol.md) <br>
- [Configuration Reference](references/config.md) <br>
- [Question Patterns](references/question-patterns.md) <br>
- [Coding Report Format](references/coding-report-format.md) <br>
- [Build Playbook](references/build-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown questions, structured reports, and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block high-rigor coding or build work until decision-critical gaps are answered.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
