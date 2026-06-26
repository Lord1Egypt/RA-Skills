## Description: <br>
Automates setup of an Ubuntu algorithm development environment with China-optimized network mirrors, guided tool installation, environment configuration, and optional GPU development setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize or reset Ubuntu machines for algorithm and deep learning development. It guides system checks, optional proxy and mirror configuration, package installation, Docker, conda, CUDA/cuDNN, and terminal setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad persistent system changes to apt, Docker, shell, conda, CUDA, and network configuration. <br>
Mitigation: Install only on a personal Ubuntu machine where these changes are intended, review each step before execution, and back up relevant configuration files first. <br>
Risk: Global Git and HuggingFace proxy or mirror settings can route private repositories, models, or tokens through third-party services. <br>
Mitigation: Avoid global proxy settings for private code or credentials, prefer temporary per-session settings when possible, and remove proxy configuration after setup if it is no longer needed. <br>
Risk: Sudo operations, CUDA driver changes, and Docker group membership can have long-term security or system stability effects. <br>
Mitigation: Approve sudo commands only after reading them, skip CUDA removal or Docker group changes unless they are intentional, and plan for reboot and rollback before GPU driver installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jessy-huang/eai-dev-setup) <br>
- [Publisher Profile](https://clawhub.ai/user/jessy-huang) <br>
- [Tools Guide](references/tools_guide.md) <br>
- [CUDA Guide](references/cuda_guide.md) <br>
- [Configuration Templates](references/config_templates.md) <br>
- [CUDA Toolkit Downloads](https://developer.nvidia.com/cuda-downloads) <br>
- [CUDA Compatibility Documentation](https://docs.nvidia.com/deploy/cuda-compatibility/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed and run step by step with explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
