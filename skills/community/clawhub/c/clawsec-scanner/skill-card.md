## Description: <br>
Automated vulnerability scanner for agent platforms. Performs dependency scanning (npm audit, pip-audit), multi-database CVE lookup (OSV, NVD, GitHub Advisory), SAST analysis (Semgrep, Bandit), and agent-specific static hook inspection for OpenClaw hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan agent-platform skills and dependencies for known vulnerabilities, static security findings, CVE enrichment, and OpenClaw hook risk signals. It can also install a persistent OpenClaw hook for periodic scan reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a persistent OpenClaw hook that scans on agent bootstrap and command events. <br>
Mitigation: Review the hook setup before running it, back up any existing clawsec-scanner-hook directory, and keep CLAWSEC_SCANNER_TARGET scoped to intended paths. <br>
Risk: Scanner output may be incomplete or misleading if optional tools, API tokens, lockfiles, or manual review are missing. <br>
Mitigation: Treat DAST and Semgrep severity output as triage input, confirm important findings manually, and verify that required binaries and optional API credentials are configured. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/davida-ps/skills/clawsec-scanner) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawSec scanner documentation](https://clawsec.prompt.security/scanner) <br>
- [OSV API documentation](https://osv.dev/docs/) <br>
- [NVD API documentation](https://nvd.nist.gov/developers/vulnerabilities) <br>
- [Semgrep Registry](https://semgrep.dev/explore) <br>
- [Bandit documentation](https://bandit.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scanner reports in JSON or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include dependency, CVE, SAST, and OpenClaw hook findings with severity summaries and remediation guidance.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
