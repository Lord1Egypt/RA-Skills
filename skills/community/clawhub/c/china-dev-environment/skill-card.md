## Description: <br>
Configure development environments for Chinese developers by guiding agents to set up mirrors, proxies, and alternative services for npm, pip, Docker, GitHub, Google services, and China-friendly project templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to ask an agent for China-compatible development environment setup guidance, including package-manager mirrors, Docker registry configuration, GitHub acceleration, proxy patterns, and alternative cloud or web services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global Docker and package-manager configuration commands can change developer machines beyond a single project. <br>
Mitigation: Back up existing Docker and package-manager settings, prefer project-local configuration where possible, and manually review any sudo Docker daemon changes before applying them. <br>
Risk: Unknown or untrusted mirrors may expose users to stale, unavailable, or tampered dependencies. <br>
Mitigation: Verify each mirror is trusted for the environment and fall back to official registries when freshness or integrity is required. <br>
Risk: Proxy and acceleration examples can involve credentials or network-routing choices that are environment-specific. <br>
Mitigation: Keep proxy credentials in environment variables or secret stores and review generated proxy settings before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-dev-environment) <br>
- [Publisher profile](https://clawhub.ai/user/lm203688) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, YAML, XML, TOML, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include commands that modify user-level package manager settings, Git configuration, or system Docker daemon configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
