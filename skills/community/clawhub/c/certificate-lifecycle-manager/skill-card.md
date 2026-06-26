## Description: <br>
Manage TLS/SSL certificate lifecycle through discovery, monitoring, renewal planning, rotation, ACME automation, and post-rotation verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operations teams use this skill to inventory certificates, monitor expiry, plan renewals, automate ACME/Let's Encrypt workflows, and verify certificate deployment after rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate discovery and renewal-hook inspection can expose sensitive host, namespace, path, and script details. <br>
Mitigation: Restrict host lists, Kubernetes namespaces, and local paths before use, and review or redact hook script contents before sharing output. <br>
Risk: Live renewal commands and service deployment steps can change production certificate state. <br>
Mitigation: Run renewal dry-runs first and require backups, change approval, verification, and rollback steps before production changes or restarts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, inventory tables, and operational runbook steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes certificate inventory summaries, renewal and verification commands, alerting configuration, and manual renewal steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
