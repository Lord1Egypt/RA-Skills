## Description: <br>
Detect 500+ types of hardcoded secrets, including API keys, credentials, and tokens, before they leak into git by wrapping GitGuardian's ggshield CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amascia-gg](https://clawhub.ai/user/amascia-gg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to ask an agent to scan repositories, files, staged changes, and Docker images for hardcoded secrets before code is committed or released. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected code or Docker image content through a third-party scanner and the security summary says its privacy guarantees are overstated. <br>
Mitigation: Use it only for repositories whose contents and paths may be shared with GitGuardian, and verify data handling expectations against GitGuardian documentation before scanning sensitive code. <br>
Risk: The skill requires a GitGuardian API key for scanning. <br>
Mitigation: Use a revocable API key with the minimum needed scope and rotate or revoke it if it is exposed. <br>
Risk: The skill depends on the local ggshield binary and package source. <br>
Mitigation: Install ggshield from a trusted source and verify the binary or package before granting it access to repositories or Docker images. <br>
Risk: The skill can install git hooks that affect future commit or push workflows. <br>
Mitigation: Require explicit approval before installing pre-commit or pre-push hooks, and review the resulting hook configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amascia-gg/ggshield-scanner) <br>
- [ggshield documentation](https://docs.gitguardian.com/ggshield-docs/) <br>
- [GitGuardian dashboard](https://dashboard.gitguardian.com) <br>
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like status messages with command guidance and ggshield scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ggshield binary and GITGUARDIAN_API_KEY environment variable; Docker image scanning also depends on local Docker availability.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
