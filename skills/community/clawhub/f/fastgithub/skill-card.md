## Description: <br>
Provides a local proxy service that helps accelerate GitHub access for clone, push, and release-download workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yantianlong-01](https://clawhub.ai/user/yantianlong-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, start, stop, and troubleshoot FastGithub as a local proxy for slow GitHub access. It is intended for environments where users can review and manage proxy settings, background processes, and certificate trust changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to make broad system and network trust changes, including proxy configuration and optional custom root CA installation. <br>
Mitigation: Install only when the publisher and binary can be independently trusted, and avoid installing the custom root CA unless the TLS interception implications are understood. <br>
Risk: Proxy environment variables, certificates, and background FastGithub processes may persist beyond the intended session. <br>
Mitigation: Remove proxy settings, trusted certificates, and running background processes when GitHub acceleration is no longer needed. <br>
Risk: The artifact includes troubleshooting guidance that can disable Git SSL verification. <br>
Mitigation: Avoid disabling Git SSL verification except for short-lived diagnostics, and restore normal SSL verification immediately afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yantianlong-01/fastgithub) <br>
- [Publisher profile](https://clawhub.ai/user/yantianlong-01) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for install, start, stop, restart, proxy setup, status checks, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
