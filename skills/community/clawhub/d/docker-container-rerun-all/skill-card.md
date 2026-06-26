## Description: <br>
Sequentially check and optionally update all docker run containers that already have fixed recreate commands recorded in long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to batch-check Docker containers whose exact docker run recreate commands are already recorded in MEMORY.md. It supports a default inspection pass and an explicit apply mode for sequential recreation when image IDs change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect Docker containers and read MEMORY.md entries containing fixed recreate commands. <br>
Mitigation: Install it only on machines where this access is acceptable and run the default non-apply check first. <br>
Risk: When explicitly run with --apply, matching containers may be stopped, removed, and recreated. <br>
Mitigation: Review the matched containers and use --apply only when container recreation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugvfpdcuwfnh/docker-container-rerun-all) <br>
- [Publisher profile](https://clawhub.ai/user/ugvfpdcuwfnh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Chinese grouped report with optional JSON execution summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports updated, already up-to-date, and failed containers; apply mode may stop, remove, and recreate matched containers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
