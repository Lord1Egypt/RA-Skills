## Description: <br>
Automates FortiGate firewall configuration, including basic policy management and security configuration for industrial protocols such as Modbus, IEC104, and S7. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiansiting](https://clawhub.ai/user/jiansiting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network, security, and industrial operations engineers use this skill to list and change FortiGate firewall policies, address objects, industrial protocol service objects, IPS profiles, and related ICS policy configuration through the FortiGate REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent production firewall changes through privileged FortiGate API access. <br>
Mitigation: Review every write action before execution, test first against a non-production device, and use a least-privilege FortiGate API token. <br>
Risk: The artifact defaults FORTIGATE_VERIFY_SSL to false, which can expose FortiGate API traffic to interception when used unchanged. <br>
Mitigation: Set FORTIGATE_VERIFY_SSL=true and configure a valid certificate before using the skill outside a controlled test environment. <br>
Risk: The skill requires a FortiGate API token that could grant sensitive network administration capability. <br>
Mitigation: Store the token in protected secret storage and scope it only to the operations required for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiansiting/fortigate-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages, tabular policy listings when tabulate is available, and CLI guidance for unsupported Industrial Connectivity API paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON command parameters and reads FortiGate connection settings from environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
