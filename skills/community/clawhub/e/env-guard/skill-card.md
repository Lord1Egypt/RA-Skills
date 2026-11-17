## Description:

Scan repos and workspaces for leaked secrets. API keys in code, passwords in configs, tokens in logs. Catches them before they hit git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scan local repositories and workspaces for leaked API keys, passwords, tokens, private keys, connection strings, and webhook URLs before code reaches Git or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Programmatic reports may contain plaintext secret lines.

Mitigation: Do not serialize, upload, or share reports from this version; review findings locally and redact sensitive values before storage or transmission.

Risk: Scanning untrusted workspaces may follow symlinks outside the intended folder.

Mitigation: Use the CLI only on trusted workspaces unless symlink traversal has been blocked or the target tree has been reviewed.

Risk: The security verdict is suspicious for this release.

Mitigation: Review before installing or using in CI, and prefer trusted local workspaces until the raw finding field is removed or fully redacted.

## Reference(s):

- [Env Guard ClawHub listing](https://clawhub.ai/theshadowrose/skills/env-guard)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [analysis, text, shell commands, code, configuration, guidance]

**Output Format:** [Text and JSON-compatible scan reports with file, line, severity, and secret-type details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output exits nonzero when potential secrets are found; programmatic reports may include findings for downstream handling.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
