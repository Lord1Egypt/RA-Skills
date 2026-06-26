## Description: <br>
Documentation coverage and quality analyzer that detects undocumented public functions, missing JSDoc, docstrings, godoc, Javadoc, incomplete parameter descriptions, README gaps, CHANGELOG issues, and documentation quality problems across JavaScript, TypeScript, Python, Go, Java, and Ruby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use DocCoverage to scan repositories for missing or incomplete documentation, generate coverage reports, enforce documentation policies, and optionally block commits with documentation gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pro hook setup changes the current repository's lefthook configuration and can block commits. <br>
Mitigation: Install hooks only in repositories where documentation-gate behavior is intended, review the generated lefthook configuration, and uninstall the hooks when they are no longer desired. <br>
Risk: Paid features use the DOCCOVERAGE_LICENSE_KEY credential. <br>
Mitigation: Store the key only in the documented environment variable or OpenClaw config and avoid committing it to project files. <br>
Risk: Regex-based documentation checks can produce incomplete or incorrect findings. <br>
Mitigation: Review scan results before using them to enforce policy or block releases, especially for languages or patterns that need project-specific interpretation. <br>


## Reference(s): <br>
- [DocCoverage Website](https://doccoverage.pages.dev) <br>
- [DocCoverage ClawHub Page](https://clawhub.ai/suhteevah/doccoverage) <br>
- [DocCoverage README](artifact/README.md) <br>
- [DocCoverage Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, SARIF JSON, shell command invocations, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free scans are limited to 5 files; Pro and Team commands require DOCCOVERAGE_LICENSE_KEY and may create or update lefthook configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
