## Description: <br>
Manage Bohrium compute jobs through the bohr CLI or open.bohrium.com API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational researchers use this skill to submit, list, monitor, inspect logs for, download from, terminate, kill, delete, and group Bohrium compute jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bohrium credentials or file access tokens could be exposed. <br>
Mitigation: Store ACCESS_KEY securely and do not expose returned file tokens. <br>
Risk: Kill, delete, terminate, rename, or batch submission actions can change or remove Bohrium job state. <br>
Mitigation: Require explicit confirmation with exact job or group IDs before running destructive or bulk actions. <br>
Risk: The skill depends on the external bohr CLI installer and Bohrium service endpoints. <br>
Mitigation: Install only when the user uses Bohrium and trusts the bohr CLI installer source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-job) <br>
- [Bohrium web/API host](https://open.bohrium.com) <br>
- [Bohrium OpenAPI v1 endpoint](https://open.bohrium.com/openapi/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bohr CLI commands or Bohrium OpenAPI requests; destructive job actions should be explicitly confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
