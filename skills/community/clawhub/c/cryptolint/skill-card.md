## Description: <br>
CryptoLint detects cryptography misuse, weak algorithms, hardcoded keys and IVs, ECB mode, weak random generation, timing-vulnerable comparisons, and insecure TLS configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to scan local codebases for cryptographic anti-patterns and generate actionable remediation guidance before commit, push, or release. Paid tiers expand the number of detection patterns and categories available to the scanner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scanner reads source files in the target repository. <br>
Mitigation: Run it only in repositories you intend the skill to inspect, and avoid scanning directories that contain unrelated private material. <br>
Risk: License keys are sensitive credentials. <br>
Mitigation: Set CRYPTOLINT_LICENSE_KEY through a protected environment variable and avoid passing license values in command-line history or shared logs. <br>
Risk: Git hooks can execute the scanner automatically during commit and push workflows. <br>
Mitigation: Review the lefthook configuration before enabling it and keep hook installation limited to repositories where automatic cryptography scans are expected. <br>


## Reference(s): <br>
- [CryptoLint ClawHub Page](https://clawhub.ai/suhteevah/cryptolint) <br>
- [suhteevah Publisher Profile](https://clawhub.ai/user/suhteevah) <br>
- [CryptoLint Homepage](https://cryptolint.pages.dev) <br>
- [CryptoLint Git Hook Documentation](https://cryptolint.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, HTML, and Markdown-style findings with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local source files, report file and line-level findings, calculate a cryptography quality score, and return a pass or fail exit code for CI and git-hook workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
