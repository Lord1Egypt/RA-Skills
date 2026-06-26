## Description: <br>
Audit project dependencies for known vulnerabilities across npm, pip, Cargo, and Go, with report-only defaults and confirmation before fix commands run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to scan project dependency lockfiles, summarize known CVE findings by severity, identify skipped ecosystems, and optionally generate an SBOM on request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit tools may read dependency metadata and, for Go projects, package or source structure beyond lockfiles. <br>
Mitigation: Run the skill only in projects where that local inspection is acceptable, and review tool scope before scanning sensitive repositories. <br>
Risk: Aggregation and SBOM workflows can create or overwrite unified.json, report.md, or sbom.cdx.json in the target project. <br>
Mitigation: Run scans from a clean working tree or dedicated output location, and confirm SBOM generation before allowing file writes. <br>
Risk: Suggested remediation commands may change dependency versions or install packages if executed without review. <br>
Mitigation: Review every generated command, create a branch first, and require explicit confirmation before running fixes. <br>


## Reference(s): <br>
- [npm audit documentation](https://docs.npmjs.com/cli/commands/npm-audit) <br>
- [pip-audit](https://github.com/pypa/pip-audit) <br>
- [cargo-audit](https://github.com/rustsec/rustsec/tree/main/cargo-audit) <br>
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) <br>
- [Syft SBOM generator](https://github.com/anchore/syft) <br>
- [OSV vulnerability database](https://osv.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with normalized JSON reports, shell commands, and optional CycloneDX JSON SBOM files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces report.md and unified.json during aggregation; may write sbom.cdx.json only when SBOM generation is requested.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
