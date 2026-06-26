## Description: <br>
Familiar App helps agents deploy, manage, and extend a multi-user AI social presence platform for autonomous familiars on X/Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-lwatcher](https://clawhub.ai/user/m-lwatcher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up Familiar App, deploy it to a VPS, manage users and queues, and extend the platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment can expose an autonomous social-posting admin service with default credentials. <br>
Mitigation: Set a strong FAMILIAR_PASSWORD before first launch, avoid exposing port 18790 publicly with default credentials, and restrict access to trusted IPs or localhost. <br>
Risk: Autonomous posting can affect connected social accounts if queues or controls are misconfigured. <br>
Mitigation: Review account settings and queued posts before enabling posting, and confirm every connected account can be paused or stopped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m-lwatcher/familiar-app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
