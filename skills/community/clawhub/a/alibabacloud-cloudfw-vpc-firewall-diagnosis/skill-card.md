## Description: <br>
Diagnoses Alibaba Cloud Cloud Firewall VPC firewall provisioning failures, route policy configuration failures, and closure pre-check risks using read-only CloudFirewall, CBN, VPC, STS, and ActionTrail APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud firewall, network, and security engineers use this skill to investigate Alibaba Cloud VPC firewall creation failures, route policy failures, stuck configuration states, and closure pre-check risks. It supports read-only evidence gathering and produces remediation guidance for manual application through approved workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may query firewall, network, ACL, identity, and recent ActionTrail data from the selected Alibaba Cloud profile. <br>
Mitigation: Use a least-privilege read-only RAM policy, avoid broad administrator profiles, and limit diagnostics to the required account and region. <br>
Risk: Credential material could be exposed if users paste AccessKey secrets into chat or commands. <br>
Mitigation: Configure credentials through Alibaba Cloud CLI profiles and pass only profile names to diagnostic commands. <br>
Risk: CLI AI-Mode may remain enabled after diagnosis if the workflow is interrupted. <br>
Mitigation: Run the documented AI-Mode disable command after the diagnostic workflow and verify the CLI state before ending the session. <br>
Risk: Diagnostic guidance could be applied incorrectly if treated as an automated remediation. <br>
Mitigation: Apply configuration changes manually through the Alibaba Cloud Console or an approved workflow after reviewing evidence and verification points. <br>


## Reference(s): <br>
- [Closure Pre-check Guide](references/closure_precheck_guide.md) <br>
- [Complete Diagnosis Steps](references/diagnosis_steps.md) <br>
- [Diagnosis Rules](references/diagnosis_rules.md) <br>
- [Diagnosis Scenarios](references/diagnosis_scenarios.md) <br>
- [Full API Reference](references/api_reference.md) <br>
- [CLI Command Reference](references/cli_commands.md) <br>
- [RAM Policy Configuration](references/ram-policies.md) <br>
- [Execution Standards](references/execution_standards.md) <br>
- [Security Rules Reference](references/security_rules.md) <br>
- [CLI Profile Setup Guide](references/profile_setup_guide.md) <br>
- [VPC Firewall Lifecycle](references/firewall_lifecycle.md) <br>
- [VPC Firewall Configuration Guidance](references/configuration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include root cause or risk assessment, concise evidence, recommended manual actions, and verification points.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
