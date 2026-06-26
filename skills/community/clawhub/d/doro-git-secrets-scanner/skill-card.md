## Description: <br>
Git security scanner guidance for checking commits for leaked sensitive information such as API keys, passwords, and tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2mus](https://clawhub.ai/user/a2mus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to choose and run Git secret-scanning tools, set up pre-commit or CI checks, and respond to leaked credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret scan results may expose live credentials or sensitive repository details. <br>
Mitigation: Treat scan output as confidential, restrict access to results, and rotate leaked credentials before sharing or storing findings. <br>
Risk: History-rewrite remediation steps such as BFG cleanup and force-push can disrupt collaborators or lose work if used carelessly. <br>
Mitigation: Back up the repository, coordinate with collaborators, and confirm local clone recovery steps before rewriting history or force-pushing. <br>
Risk: Referenced secret-scanning tools may produce false positives or require human judgment. <br>
Mitigation: Review findings in context and verify suspected secrets before taking destructive remediation actions. <br>


## Reference(s): <br>
- [Doro Git Secrets Scanner on ClawHub](https://clawhub.ai/a2mus/doro-git-secrets-scanner) <br>
- [Gitleaks Releases](https://github.com/gitleaks/gitleaks/releases) <br>
- [TruffleHog Releases](https://github.com/trufflesecurity/trufflehog/releases) <br>
- [git-secrets Repository](https://github.com/awslabs/git-secrets.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash, YAML, and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tool installation commands, scanning examples, CI configuration, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
