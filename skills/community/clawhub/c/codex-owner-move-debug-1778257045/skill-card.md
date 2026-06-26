## Description: <br>
Validates owner migration by creating a skill under a personal owner and moving it to OpenClaw while documenting cleanup steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release reviewers use this skill to validate a controlled ClawHub owner-migration workflow for a disposable skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to create and transfer a skill into OpenClaw without enough boundaries or cleanup detail. <br>
Mitigation: Use only in a controlled OpenClaw migration test with a disposable skill, authorized account, destination owner, confirmation step, audit checks, and cleanup or rollback process. <br>
Risk: Owner-migration validation can affect skill ownership state if run against a non-disposable release. <br>
Mitigation: Define the exact test skill and verify ownership changes before and after the migration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-debug-1778257045) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown procedure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only procedure; no executable files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
