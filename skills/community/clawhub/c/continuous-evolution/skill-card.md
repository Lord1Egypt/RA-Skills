## Description: <br>
Automatically records task experience, analyzes skill gaps, updates capability scores, and generates priority evolution tasks after agent task execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to persist post-task experience, track capability assessments, and queue follow-up improvement work when audit scores indicate gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists task details and results, which can expose sensitive prompts, credentials, proprietary data, or private user content if used without controls. <br>
Mitigation: Use it only with appropriate redaction and retention controls, and avoid running it on sensitive task content unless those controls are in place. <br>
Risk: The skill automatically creates P1 follow-up evolution tasks from low audit scores. <br>
Mitigation: Manually review generated evolution tasks before execution so proposed changes do not introduce incorrect guidance or unsafe behavior. <br>


## Reference(s): <br>
- [Continuous Evolution ClawHub listing](https://clawhub.ai/zenmejiang-commits/continuous-evolution) <br>
- [Publisher profile](https://clawhub.ai/user/zenmejiang-commits) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown logs, JSON task and assessment files, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes experience logs, gap lists, capability assessments, and P1 evolution task queue entries under the agent workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.yaml, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
