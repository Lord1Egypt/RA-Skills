## Description: <br>
Structured multi-agent collaboration for backend + frontend builds. Use when an orchestrator needs to coordinate a backend engineer and frontend engineer on the same feature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nightknight64](https://clawhub.ai/user/nightknight64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical leads use this skill to coordinate backend and frontend agents on full-stack features through a shared contract, separate work areas, progress logs, recovery steps, and integration verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes deployment activation steps such as copying files, changing symlinks or server configuration, and restarting services. <br>
Mitigation: Treat deployment steps as manual guidance: review diffs, run tests, confirm paths and target environment, and require explicit approval before copy, symlink, configuration, or restart actions. <br>
Risk: Shared specs and logs could expose credentials or production secrets if agents or users paste them into collaboration files. <br>
Mitigation: Do not place real credentials or secrets in shared specs or logs; reference environment variables or approved secret stores instead. <br>
Risk: Incremental builds can break a live deployment if the active target is switched to a directory that only contains changed files. <br>
Mitigation: Confirm whether the build is full or incremental, integrate changed files into the live tree before switching targets, verify key endpoints, and keep the previous deployment available for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nightknight64/agent-collaboration-protocol) <br>
- [Spec Template](references/spec-template.md) <br>
- [Integration Log](references/integration-log.md) <br>
- [Handoff Message Format](references/handoff-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a shared collaboration workspace and template files when the optional initialization script is run.] <br>

## Skill Version(s): <br>
1.5.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
