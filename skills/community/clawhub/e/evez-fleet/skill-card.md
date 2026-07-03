## Description: <br>
Deploy and manage the EVEZ OpenClaw mesh across GCP and Vultr with scripts for provider integration, infrastructure setup, and health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw provider access, provision GCP resources, and monitor an OpenClaw gateway in a small fleet that includes Vultr and planned GCP nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud setup commands can create persistent GCP resources and may lead to billing despite free-tier language. <br>
Mitigation: Run only in a GCP project prepared for possible charges, review quotas and billing settings first, and remove created resources when they are no longer needed. <br>
Risk: Provider API keys are passed as shell arguments and written into local OpenClaw configuration. <br>
Mitigation: Treat provider keys as secrets, avoid leaving them in shell history or logs, restrict local config access, and rotate keys after testing. <br>
Risk: The GCP setup script runs a remote OpenClaw installer. <br>
Mitigation: Audit or pin the installer before execution and run the setup in an isolated project or test environment first. <br>
Risk: The watchdog can kill and restart a local gateway process. <br>
Mitigation: Review the process match, paths, and service user before enabling it on a shared or production host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-fleet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents toward cloud provisioning commands, OpenClaw CLI configuration, and local watchdog setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
