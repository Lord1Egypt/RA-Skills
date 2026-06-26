## Description: <br>
Configures China-friendly mirror sources for common development tools including npm, yarn, pnpm, pip, Go, Docker, Cargo, Maven, Gradle, Homebrew, and Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironmanc2014](https://clawhub.ai/user/ironmanc2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and configure package registry, proxy, and mirror settings for development tools when network access to default upstream sources is slow or unreliable. It supports status checks, per-tool mirror changes, reset commands, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently redirect package and registry sources for development tools. <br>
Mitigation: Run status first, configure only named tools instead of using all-tool setup by default, and use reset commands when changes are no longer desired. <br>
Risk: Some settings can weaken dependency trust, including global pip trusted-host configuration and broad Go GONOSUMDB settings. <br>
Mitigation: Avoid those settings unless the user understands the trust tradeoff, and review the resulting configuration before continuing dependency installation. <br>
Risk: Docker mirror setup may require root or administrator changes to daemon configuration. <br>
Mitigation: Review Docker daemon JSON edits before applying elevated changes and restart Docker only after the configuration is confirmed. <br>


## Reference(s): <br>
- [Mirror Source Reference](references/mirrors.md) <br>
- [ClawHub Release Page](https://clawhub.ai/ironmanc2014/cn-dev-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent development-tool configuration changes and reset commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
