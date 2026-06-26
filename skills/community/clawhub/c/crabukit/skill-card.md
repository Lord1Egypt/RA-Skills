## Description: <br>
Security scanner for OpenClaw skills with Clawdex integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tnbradley](https://clawhub.ai/user/tnbradley) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use Crabukit to scan OpenClaw skill packages before installation, during development, while auditing installed skills, and in CI security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install workflows and shell wrappers can install a named skill after scanning. <br>
Mitigation: Use read-only crabukit scan for review workflows, and run install commands only when installation is intended. <br>
Risk: Optional Clawdex integration may disclose a scanned skill name during private audits. <br>
Mitigation: Disable or avoid Clawdex-backed lookups when skill names or audit targets are confidential. <br>
Risk: Static analysis cannot prove runtime behavior is safe. <br>
Mitigation: Treat scan results as one review layer and manually inspect high-impact skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tnbradley/crabukit) <br>
- [Publisher profile](https://clawhub.ai/user/tnbradley) <br>
- [README](README.md) <br>
- [Security policy](SECURITY.md) <br>
- [Research summary](RESEARCH_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown documentation, JSON/SARIF scan reports when requested, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity thresholds, exit codes for CI, and optional Clawdex lookup results when that integration is available.] <br>

## Skill Version(s): <br>
0.1.3 (source: pyproject.toml, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
