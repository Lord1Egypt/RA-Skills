## Description: <br>
Infrastructure configuration auditor that scans Dockerfiles, Kubernetes manifests, Terraform, and CI/CD pipelines for security misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security reviewers use ConfigSafe to scan local infrastructure configuration files for misconfigurations, generate security reports, and optionally install pre-commit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted license content can cause code execution during license handling. <br>
Mitigation: Use license keys only from trusted sources and avoid pasting license tokens received through untrusted channels. <br>
Risk: Hook installation persistently changes repository hook configuration and runs on future commits. <br>
Mitigation: Review the hook configuration before installing, install it only in repositories where automatic commit-time scanning is intended, and remove it when no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/suhteevah/configsafe) <br>
- [Publisher profile](https://clawhub.ai/user/suhteevah) <br>
- [ConfigSafe homepage](https://configsafe.pages.dev) <br>
- [ConfigSafe hook documentation](https://configsafe.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, markdown reports, and SARIF-compatible results from local shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify lefthook.yml when hook installation is used; Pro and Team features require CONFIGSAFE_LICENSE_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
