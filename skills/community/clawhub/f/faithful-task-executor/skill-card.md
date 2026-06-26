## Description: <br>
A task orchestration skill that helps agents preserve user requirements across multi-step work, subagent coordination, rule checks, and final delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run complex tasks with an explicit rules file, staged planning, subagent handoff checks, and rule-compliance review before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores task requirements locally, and users may accidentally include secrets or sensitive context in those rules. <br>
Mitigation: Review generated task rules before confirming them and avoid placing credentials, tokens, or other secrets in the rules file. <br>
Risk: Broad task-execution trigger phrases may activate the workflow when a lighter response would be enough. <br>
Mitigation: Confirm that the generated rules and plan match the intended scope before allowing execution to continue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/endcy/faithful-task-executor) <br>
- [Publisher profile](https://clawhub.ai/user/endcy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown plans, rule files, checklists, subagent task prompts, and final task summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local task-rule artifacts such as .task-rules/rules.md when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
