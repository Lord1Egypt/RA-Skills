## Description: <br>
Manage AI agent workflows using concurrent process algebra patterns like parallel tasks, branch-fix loops, fan-out comparisons, and session status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multi-agent coding and review workflows, run tasks in parallel, recover from failures with branch-fix or saga patterns, compare model outputs, and inspect session status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the external cpa-agents npm package. <br>
Mitigation: Review or pin the package before use and install it first in a development workspace. <br>
Risk: Agent-driven orchestration can create branches, write files, merge changes, roll back work, or fan tasks out to multiple models. <br>
Mitigation: Use explicit user approval for branch creation, file writes, merges, rollback, and model fan-out tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jose-compu/cpa-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and TypeScript examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent commands accept task, model, and timeout inputs; status accepts an empty object.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
