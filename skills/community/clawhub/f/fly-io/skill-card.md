## Description: <br>
Deploy and manage applications on Fly.io using the flyctl CLI and Machines API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwhite-oss](https://clawhub.ai/user/dwhite-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Fly.io deployment, scaling, status, logging, secret, machine, SSH, and Fly Postgres workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact infrastructure operations, including deploys, secret changes, database actions, SSH access, scaling, and machine destruction. <br>
Mitigation: Use a least-privilege Fly.io account and require confirmation before any deploy, secret, database, SSH, scaling, or destroy command. <br>
Risk: Authentication tokens or secrets could be exposed if printed into chat or logs. <br>
Mitigation: Do not allow auth tokens or secrets to be printed into chat or logs, and avoid production credentials unless explicitly needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dwhite-oss/fly-io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require flyctl authentication and user confirmation before changing infrastructure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
