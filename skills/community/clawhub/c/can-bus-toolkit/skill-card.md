## Description: <br>
Can Bus Toolkit helps agents prepare CAN bus data provenance workflows with OpenTimestamps synchronization, parallel indexing, tamper alerts, protocol adapters, and audit report exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation teams, and audit teams use this skill to configure data provenance workflows, verify timestamped records, monitor tamper signals, and export audit reports for CAN bus or CAN-style records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automated data handling and external alerting could expose logs, traffic, or audit records to unintended destinations. <br>
Mitigation: Restrict which logs or traffic the skill may inspect, disable adapters that are not needed, and review webhook and OTS destinations before use. <br>
Risk: Persistent indexing, report generation, snapshots, and rollback behavior can affect sensitive audit data and system state. <br>
Mitigation: Choose report and snapshot directories deliberately, enforce least-privilege file access, and require manual approval before rollback or restoration. <br>
Risk: Configuration examples include network endpoints and alert destinations that may be environment-specific. <br>
Mitigation: Validate endpoints, keep webhook URLs in environment variables, and avoid hardcoding secrets in configuration files. <br>


## Reference(s): <br>
- [Can Bus Toolkit release page](https://clawhub.ai/thcjp/skills/can-bus-toolkit) <br>
- [OpenTimestamps pool A](https://a.pool.opentimestamps.org) <br>
- [OpenTimestamps pool B](https://b.pool.opentimestamps.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, YAML configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include audit workflow guidance, configuration examples, and operational steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
