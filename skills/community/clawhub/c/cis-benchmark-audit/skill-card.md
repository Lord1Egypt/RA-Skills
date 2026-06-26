## Description: <br>
CIS benchmark compliance assessment for network infrastructure devices that maps device configuration against CIS controls across Management Plane, Control Plane, and Data Plane categories for Cisco IOS, PAN-OS, JunOS, and Check Point platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security, compliance, and infrastructure teams use this skill to collect read-only evidence and map network device configuration against applicable CIS benchmark controls for audits, baselines, post-upgrade checks, and regulatory evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit collection may expose sensitive device configuration, including usernames, SNMP settings, authentication details, firewall policies, routing data, NAT or decryption rules, and session information. <br>
Mitigation: Use read-only accounts scoped to approved devices and treat collected outputs as confidential audit evidence. <br>
Risk: Using the skill outside an authorized audit scope can create access, privacy, or compliance issues. <br>
Mitigation: Install and use it only for authorized network audits, and review commands before running them. <br>


## Reference(s): <br>
- [CIS Benchmark Control Reference](references/control-reference.md) <br>
- [CIS Benchmark Audit CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with read-only CLI commands, audit steps, control mappings, scoring guidance, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compliance assessment guidance and evidence-collection commands; it does not modify device configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
