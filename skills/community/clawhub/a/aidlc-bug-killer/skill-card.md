## Description: <br>
Coordinates a three-agent bug-fix workflow in which a SubAgent reports bugs, the main agent fixes code, and a ReviewAgent confirms the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sydpz](https://clawhub.ai/user/sydpz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate bug discovery, repair, verification, and changelog updates across multiple agents. It is intended for repositories that track bug state through Markdown files under aidlc-docs/bug-reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may create and move bug-tracking Markdown files and update aidlc-docs/aidlc-state.md. <br>
Mitigation: Install it only in repositories where these file changes are acceptable, and review branch changes before merge. <br>
Risk: Agent-proposed fixes or test results may be incomplete or incorrect. <br>
Mitigation: Keep normal code review, test verification, and merge controls in place. <br>


## Reference(s): <br>
- [Bug Report Template](references/bug-template.md) <br>
- [AIDLC Bug Killer on ClawHub](https://clawhub.ai/sydpz/aidlc-bug-killer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown bug reports with code changes, test-verification notes, and changelog entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and move bug-tracking Markdown files across pending, waiting_confirm, and confirmed directories.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
