## Description: <br>
Breaks large, fuzzy, or long-running Codex objectives into smaller goal-mode tasks with clear scope, done conditions, validation steps, and executable /goal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjo92](https://clawhub.ai/user/hanjo92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert broad Codex work requests into a short sequence of reviewable /goal tasks. It is most useful when a project should be split into ordered checkpoints with explicit scope, validation, and stopping conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated /goal commands may ask Codex to read or modify project files depending on the user's original objective. <br>
Mitigation: Review each generated /goal command before running it, especially its scope, file boundaries, validation method, and stopping condition. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanjo92/codex-goal-decomposer) <br>
- [Publisher profile](https://clawhub.ai/user/hanjo92) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline /goal commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ordered sub-goals with rationale, scope, done conditions, validation methods, and exact /goal command text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
