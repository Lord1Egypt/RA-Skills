## Description:

Audit project dependencies for known vulnerabilities across npm, pip, Cargo, and Go, with report-only defaults and confirmation before fix commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to inspect dependency lockfiles, run ecosystem audit tools, aggregate vulnerability findings, and optionally generate a CycloneDX SBOM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a remote Syft installer pattern that can execute unpinned code.

Mitigation: Install Syft through a trusted package manager or a pinned, verified release instead of using curl piped to a shell.

Risk: Go and SBOM workflows may traverse project contents and expose local dependency metadata or file paths.

Mitigation: Run audits only on directories the user intends to inspect and review reports before sharing them outside the local environment.

Risk: SBOM generation writes sbom.cdx.json into the target directory and may be affected by symlink-resolved output paths.

Mitigation: Generate SBOMs only for trusted directories until symlink-safe output handling is reviewed.

## Reference(s):

- [ClawHub dep-audit release page](https://clawhub.ai/tkuehnl/skills/dep-audit)
- [npm audit documentation](https://docs.npmjs.com/cli/commands/npm-audit)
- [pip-audit](https://github.com/pypa/pip-audit)
- [cargo-audit](https://github.com/rustsec/rustsec/tree/main/cargo-audit)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [Syft](https://github.com/anchore/syft)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown vulnerability report, normalized JSON audit results, optional CycloneDX JSON SBOM, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-only by default; fix commands require explicit user confirmation; SBOM generation writes sbom.cdx.json only when requested.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
