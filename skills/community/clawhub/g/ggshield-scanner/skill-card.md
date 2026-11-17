## Description:

Detect 500+ types of hardcoded secrets (API keys, credentials, tokens) before they leak into git. Wraps GitGuardian's ggshield CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amascia-gg](https://clawhub.ai/user/amascia-gg)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to have an AI agent run ggshield secret scans on repositories, individual files, staged changes, and Docker images before code is committed or shipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unsafe installer guidance in the documentation.

Mitigation: Review before installing and prefer a pinned, verified installation path for dependencies and agent tooling.

Risk: The release evidence flags overconfident privacy claims for a cloud-backed secret scanner.

Mitigation: Confirm GitGuardian and ggshield data handling requirements for the deployment before scanning sensitive private repositories or files.

Risk: The skill can install ggshield git hooks that block commits or pushes when secrets are detected.

Mitigation: Only ask the agent to install hooks when pre-commit or pre-push enforcement is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amascia-gg/skills/ggshield-scanner)
- [ggshield documentation](https://docs.gitguardian.com/ggshield-docs/)
- [ggshield project](https://github.com/GitGuardian/ggshield)
- [GitGuardian dashboard](https://dashboard.gitguardian.com)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with command output summaries and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ggshield CLI and GITGUARDIAN_API_KEY environment variable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
