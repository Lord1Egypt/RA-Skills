## Description:

Helps developers scan Git repositories for leaked secrets such as API keys, passwords, and tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a2mus](https://clawhub.ai/user/a2mus)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to get practical commands and configuration examples for scanning Git repositories with Gitleaks, TruffleHog, and git-secrets, then responding to exposed secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some tool and CI examples can give third-party scanners or GitHub Actions sensitive repository and token access without enough version pinning or permission limits.

Mitigation: Pin tool versions, Docker digests, and GitHub Actions to reviewed commits; use minimal workflow permissions; provide GITHUB_TOKEN only when it is required.

Risk: The remediation examples include hooks, scheduled scans, sudo installation, BFG history rewriting, and force pushes that can disrupt repositories if run casually.

Mitigation: Require repository-owner approval, backups, team coordination, and a recovery plan before installing privileged tooling or rewriting Git history.

## Reference(s):

- [Gitleaks Releases](https://github.com/gitleaks/gitleaks/releases)
- [TruffleHog Releases](https://github.com/trufflesecurity/trufflehog/releases)
- [git-secrets Repository](https://github.com/awslabs/git-secrets.git)
- [ClawHub Skill Page](https://clawhub.ai/a2mus/skills/doro-git-secrets-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install commands, scan examples, CI configuration, remediation steps, and scanner configuration snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
