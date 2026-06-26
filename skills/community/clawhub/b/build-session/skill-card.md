## Description: <br>
Facilitates focused autonomous sessions to build, create, or produce one concrete deliverable, then log and commit progress efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenartzt](https://clawhub.ai/user/stevenartzt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to structure scheduled or focused build sessions so the agent chooses one concrete task, completes it, records progress, and handles git follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous build sessions can commit or push workspace changes before a human has reviewed the diff. <br>
Mitigation: Use an isolated repository or branch, inspect git status and diffs before committing, avoid broad staging commands unless reviewed, and require explicit approval before git push. <br>
Risk: Session helper scripts can write logs into the configured workspace memory directory. <br>
Mitigation: Set OPENCLAW_WORKSPACE deliberately and review generated memory files as part of the session closeout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenartzt/build-session) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional helper-script output for task selection and session logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
