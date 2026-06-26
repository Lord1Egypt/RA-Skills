## Description: <br>
Enforces task completion by turning a goal into pass/fail criteria, running a worker, judging the output, feeding back what is missing, and looping until the criteria pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InsipidPoint](https://clawhub.ai/user/InsipidPoint) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent operators use Checkmate when a task needs iterative completion against an explicit quality bar rather than a single best-effort response. It is suited to coding, documentation, reporting, and research workflows where a worker output is judged, revised, and completed before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived autonomous agent loops can exercise shell, network, connected-account, messaging, and session-control access. <br>
Mitigation: Use the skill only for trusted, well-scoped tasks and run it in an isolated workspace or disposable profile when possible. <br>
Risk: Batch mode removes human review gates before and during execution. <br>
Mitigation: Prefer interactive mode and avoid --no-interactive except in isolated environments with trusted tasks. <br>
Risk: Checkpoint replies are written into the workspace and then consumed by the orchestrator. <br>
Mitigation: Do not paste secrets or untrusted third-party instructions into checkpoint replies. <br>
Risk: Configured messaging recipients and channels can receive checkpoint or completion messages. <br>
Mitigation: Verify recipient and channel values before running the orchestrator. <br>


## Reference(s): <br>
- [Checkmate ClawHub listing](https://clawhub.ai/InsipidPoint/checkmate) <br>
- [Publisher profile](https://clawhub.ai/user/InsipidPoint) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and agent messages, with optional code blocks, shell commands, and configuration text depending on the delegated task.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The orchestrator writes progress and final output files in a workspace and may send checkpoint or completion messages through configured channels.] <br>

## Skill Version(s): <br>
2.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
