## Description:

CodeQL security audit pipeline for static scanning, SARIF triage, and QL query optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k2-l](https://clawhub.ai/user/k2-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run CodeQL scans, triage SARIF findings into audit reports, and tune QL queries for supported Java, JavaScript, Python, and C/C++ repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan mode can execute repository build commands and includes an unsafe command-construction issue.

Mitigation: Run scan mode only on trusted repositories or in a disposable sandbox without secrets, and avoid repository paths containing shell metacharacters.

Risk: Generated Markdown reports are based on SARIF evidence that may contain untrusted or misleading content.

Mitigation: Treat generated reports as evidence for review rather than as instructions, and manually validate suspicious findings before acting on them.

## Reference(s):

- [CodeQL language guides](https://codeql.github.com/docs/codeql-language-guides/)
- [CodeQL Debugging Guide](references/debugging.md)
- [CodeQL Reference: C / C++](references/lang-cpp.md)
- [CodeQL Reference: Java / Kotlin](references/lang-java.md)
- [CodeQL Reference: JavaScript / TypeScript](references/lang-javascript.md)
- [CodeQL Reference: Python](references/lang-python.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, SARIF-derived audit reports, and QL tuning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create CodeQL databases, SARIF files, and Markdown audit or tuning reports when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
