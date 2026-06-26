## Description: <br>
Structured protocol for fixing bugs with AI agents that prevents hallucinations and fix loops by enforcing step-by-step diagnosis before code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borodich](https://clawhub.ai/user/borodich) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to fix bugs through diagnosis, failing-test reproduction, root-cause analysis, minimal code changes, verification, related-pattern review, and test-system improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug-fix workflows can make broad or high-impact local code and test changes if followed without review. <br>
Mitigation: Review proposed code and test changes before execution, keep edits scoped to the reproduced bug, and confirm any privileged maintainer actions carefully. <br>
Risk: Helper workflows may run nested review or automation commands with unrestricted local access. <br>
Mitigation: Use restricted or no-yolo execution options where available, and run the skill in a controlled workspace with the needed repository permissions only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/borodich/bug-fix-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists and bug-fix/test-audit templates; code, tests, and shell commands may be produced when an agent applies the protocol.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a failing reproduction test before fixing, or an explicit explanation when test reproduction is not feasible.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
