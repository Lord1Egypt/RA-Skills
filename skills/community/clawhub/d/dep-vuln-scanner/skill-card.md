## Description:

Scans npm, Python/pip, and Go dependency files for known vulnerabilities using the OSV.dev API, with terminal summaries, optional JSON output, ecosystem filtering, and CI-friendly exit status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check npm, Python, and Go project dependencies for known vulnerabilities before deployment, during CI checks, or while investigating third-party library CVEs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency names and versions are shared with OSV.dev during vulnerability checks.

Mitigation: Use the skill only for projects where sending package coordinates to OSV.dev is acceptable.

Risk: Scanner results may be incomplete because network handling fails open and dependency version parsing can be lossy.

Mitigation: Treat results as advisory unless the CI workflow compensates for these limits or hardens the scanner before using it as a release gate.

Risk: Machine-readable output may need validation before automated CI enforcement.

Mitigation: Validate JSON output in the target workflow before relying on it for deployment decisions.

## Reference(s):

- [OSV.dev API query endpoint](https://api.osv.dev/v1/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner output can include severity labels, vulnerability IDs, CVE aliases, summaries, and CI-oriented exit status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
