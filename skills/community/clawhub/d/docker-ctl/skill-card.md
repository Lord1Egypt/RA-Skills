## Description: <br>
Inspect containers, logs, and images via podman <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent provide Podman-based commands for listing containers and images, viewing logs, and inspecting local containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Container logs and inspect output can expose secrets, environment variables, or internal configuration. <br>
Mitigation: Review and redact container output before sharing it outside the intended local environment. <br>
Risk: The docker-ctl command provider may vary by environment. <br>
Mitigation: Verify what provides docker-ctl locally before relying on commands generated from this skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Xejrax/docker-ctl) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a local environment where Podman is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
