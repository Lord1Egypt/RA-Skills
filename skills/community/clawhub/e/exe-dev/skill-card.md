## Description: <br>
Manage persistent VMs on exe.dev. Create VMs, configure HTTP proxies, share access, and set up custom domains. Use when working with exe.dev VMs for hosting, development, or running persistent services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjesuiter](https://clawhub.ai/user/bjesuiter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a command reference for managing exe.dev VMs used for hosting, development, persistent services, HTTP proxy configuration, sharing, and custom domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can create VMs or change exe.dev resources, which may affect cost or resource state. <br>
Mitigation: Before execution, require the agent to show the exact command and confirm the target VM and expected cost or resource impact. <br>
Risk: Sharing, public access, custom domains, and port changes can expose services to broader audiences. <br>
Mitigation: Confirm the intended audience, target VM, port, and exposure level before running commands that modify access. <br>
Risk: The artifact describes the skill as auto-built from documentation and not yet tested. <br>
Mitigation: Treat outputs as command proposals and verify them against current exe.dev documentation before use. <br>


## Reference(s): <br>
- [exe.dev VM Service Reference](artifact/references/exe-dev-vm-service.md) <br>
- [exe.dev Documentation](https://exe.dev/docs/all.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
