## Description: <br>
Consul service deregistration tool that supports batch deregistration by service ID across multiple Consul agents, parsing and replaying raw curl commands, dry-run preview, parallel execution, and ACL token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strongant](https://clawhub.ai/user/strongant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to deregister Consul service instances during maintenance, rollback, migration, or removal workflows. It can preview requests with dry-run mode before live deregistration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove live Consul service registrations in batch without a strong confirmation or scoping requirement. <br>
Mitigation: Use dry-run first, verify every service ID and Consul agent host, require human confirmation before live execution, and use a least-privilege Consul ACL token scoped only to the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/strongant/consul-deregister) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit dry-run previews, per-agent deregistration results, and non-zero exit status on failures.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
