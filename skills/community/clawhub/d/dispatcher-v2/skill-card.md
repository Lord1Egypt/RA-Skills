## Description: <br>
OpenClaw 三层架构分离主调度员，纯调度不执行，所有工作派给子代理，独立验证通过才能汇报完成。解决「声称完成但实际未执行」知行分离问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovenini12344-code](https://clawhub.ai/user/lovenini12344-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route OpenClaw tasks through a dispatcher, specialized subagents, and an independent verifier before reporting completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task state and coordination history may persist in progress, memory, regressions.md, or CURSOR_SYNC.md files. <br>
Mitigation: Clear those files when task history should not be retained, and avoid placing secrets in task descriptions or progress records. <br>
Risk: The dispatcher depends on separate executor and verifier subagents to complete and validate work. <br>
Mitigation: Review the alpha, bravo, charlie, delta, echo, and verifier agents separately before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovenini12344-code/dispatcher-v2) <br>
- [Publisher profile](https://clawhub.ai/user/lovenini12344-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON command examples and status records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates subagent delegation and writes progress, memory, regression, and synchronization records when used in an OpenClaw workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
