## Description: <br>
CodeQL security audit pipeline for static scanning, SARIF triage, and QL query optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k2-l](https://clawhub.ai/user/k2-l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run CodeQL scans, triage SARIF findings into reviewable Markdown reports, and tune custom QL queries across Java, JavaScript, Python, and C/C++ projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SCAN mode can run local repository scans and project build commands. <br>
Mitigation: Run scans only on trusted repositories or inside a sandbox or container, and confirm the target path and language before execution. <br>
Risk: Broad trigger phrases may activate scan behavior before the intended mode is clear. <br>
Mitigation: Confirm whether the user wants SCAN, AUDIT, or TUNE mode before running scripts or suggesting commands. <br>
Risk: SARIF findings without complete data flow can be suspicious rather than confirmed vulnerabilities. <br>
Mitigation: Require manual review of source-to-sink evidence before treating findings as exploitable or requesting proof-of-concept details. <br>


## Reference(s): <br>
- [CodeQL language guides](https://codeql.github.com/docs/codeql-language-guides/) <br>
- [Debugging Guide](references/debugging.md) <br>
- [Java / Kotlin Reference](references/lang-java.md) <br>
- [JavaScript / TypeScript Reference](references/lang-javascript.md) <br>
- [Python Reference](references/lang-python.md) <br>
- [C / C++ Reference](references/lang-cpp.md) <br>
- [ClawHub release page](https://clawhub.ai/k2-l/codeql-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, code, guidance] <br>
**Output Format:** [Markdown reports, SARIF files, terminal output, and QL tuning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SCAN mode can create a local CodeQL database and SARIF output; AUDIT mode can write an exp.md report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
