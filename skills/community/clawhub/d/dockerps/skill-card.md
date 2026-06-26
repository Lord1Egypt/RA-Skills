## Description: <br>
Dockerps helps agents view and manage Docker container processes, stats, logs, and metadata when Docker is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Dockerps to ask an agent to inspect local Docker containers, review process status, stats, logs, and metadata, and run Docker cleanup when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup command can immediately remove stopped containers and pruned images from the local Docker environment. <br>
Mitigation: Use cleanup only in controlled Docker environments after reviewing the expected resources; prefer list, stats, top, logs, and inspect for read-only inspection. <br>
Risk: The skill requires Docker inspection access on the host where the agent runs. <br>
Mitigation: Install only where the agent is permitted to inspect local Docker containers and logs. <br>


## Reference(s): <br>
- [Dockerps on ClawHub](https://clawhub.ai/bytesagain1/dockerps) <br>
- [bytesagain1 publisher profile](https://clawhub.ai/user/bytesagain1) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker access; cleanup can prune stopped containers and images.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
