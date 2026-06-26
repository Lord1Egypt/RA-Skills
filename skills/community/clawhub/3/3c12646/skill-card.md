## Description: <br>
Mission Control is an AI-agent task tracking and plan-confirmation skill that guides Moss through task triage, requirement capture, iterative plan analysis, user approval, execution logging, and final reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjk1103](https://clawhub.ai/user/huangjk1103) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Mission Control to require structured planning, approval, execution logging, and delivery reports before an agent performs code, file, terminal, delegation, or research tasks. It is intended for workflows where task state and explicit approval records are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation rules may route routine coding, file, terminal, delegation, or research tasks through the skill even when the user did not expect a planning gate. <br>
Mitigation: Use the skill only where explicit plan confirmation is desired, and ask for user confirmation before activating it on ambiguous or routine tasks. <br>
Risk: Task plans and reports can persist copied local file paths or content in the mission-control data directory. <br>
Mitigation: Avoid including sensitive paths or confidential content in plan text, and periodically review or clean the local mission-control records. <br>


## Reference(s): <br>
- [Mission Control ClawHub release](https://clawhub.ai/huangjk1103/3c12646) <br>
- [Static Specification Conversion Case Study](references/2026-05-19-static-spec-conversion.md) <br>
- [Project Intake Case Studies](references/project-intake-case-studies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task files, plain text progress updates, and Python script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and update local task lifecycle files such as requirements, plans, logs, reports, and project-intake templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
