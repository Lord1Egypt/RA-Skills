## Description: <br>
Runs a full Dev Team pipeline from planning to release for any coding task, producing plans, code, tests, fixes, and release notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunlearnDev](https://clawhub.ai/user/SunlearnDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate a coding task through a staged planning, implementation, testing, fixing, and reporting workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate broad coding work to multiple autonomous subagents without clear scope limits or approval checkpoints. <br>
Mitigation: Run it in a disposable branch or sandboxed repository, review PLAN.md and TASKS.md before implementation, and monitor for overlapping runs or unexpected file changes. <br>
Risk: Use on sensitive or production repositories can expose higher-impact changes to autonomous execution. <br>
Mitigation: Avoid sensitive or production repositories unless the run is isolated and all generated changes are reviewed before merge or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SunlearnDev/devteam-command) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown documents, code changes, shell command guidance, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PLAN.md, TASKS.md, BUGS.md, RELEASE.md, and implementation changes through autonomous subagent runs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
