## Description: <br>
Docker Mirror helps agents pull Docker images by trying docker.io first, then configured mirror registries when the official registry times out or fails in network-restricted Linux environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitsudog](https://clawhub.ai/user/kitsudog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when an agent needs to recover from Docker image pull failures by retrying through configured mirror registries. It is suited to trusted Linux environments where Docker and sg-based Docker group access are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad Docker command authority through Docker-group access. <br>
Mitigation: Install and use it only in trusted Linux environments, and review any non-pull Docker command before execution. <br>
Risk: Fallback pulls may retrieve images from third-party mirrors instead of docker.io. <br>
Mitigation: Use mirror fallback only for intentional pull failures and verify image source, tags, or digests when provenance matters. <br>


## Reference(s): <br>
- [Docker Mirror on ClawHub](https://clawhub.ai/kitsudog/docker-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may propose Docker pull commands and mirror fallback usage; command execution should be reviewed in the target environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
