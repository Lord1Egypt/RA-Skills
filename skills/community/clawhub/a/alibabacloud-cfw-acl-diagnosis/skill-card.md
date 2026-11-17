## Description: <br>
A read-only assistant for diagnosing Alibaba Cloud Cloud Firewall ACL rule behavior across Internet, NAT boundary, and VPC boundary firewalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and developers use this skill to investigate why Alibaba Cloud Cloud Firewall ACL rules are not taking effect, inspect read-only rule and traffic-log data, and receive console-only remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run live Alibaba Cloud firewall, traffic-log, SLS, and ActionTrail queries with the user's configured credentials. <br>
Mitigation: Use least-privilege RAM permissions and avoid broad production credentials where possible. <br>
Risk: Plugin installation or curl/wget validation steps could affect the user's local environment if treated as automatic actions. <br>
Mitigation: Treat installation and validation steps as user-approved setup or testing actions. <br>
Risk: Firewall diagnosis can produce incorrect or misleading guidance if based on incomplete query results or missing permissions. <br>
Mitigation: Review the diagnosis, confirm permission-denied checks, and scan the skill before deployment. <br>


## Reference(s): <br>
- [Cloud Firewall ACL Rule Knowledge Base](references/cfw_acl_knowledge.md) <br>
- [Cloud Firewall CLI Command Reference](references/cli_commands.md) <br>
- [Alibaba Cloud Cloud Firewall CLI Pitfalls and Notes](references/cli_traps.md) <br>
- [Cloud Firewall ACL Configuration Guide](references/configuration_guide.md) <br>
- [Cloud Firewall ACL Diagnosis Framework](references/diagnosis.md) <br>
- [Execution Standards for Cloud Firewall ACL Diagnosis](references/execution_standards.md) <br>
- [RAM Permission List](references/ram-policies.md) <br>
- [Security Rules - Complete Prohibitions](references/security_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-acl-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, analysis] <br>
**Output Format:** [Markdown text with read-only CLI command snippets and concise diagnosis tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Console guidance only; no configuration-change commands or file outputs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
