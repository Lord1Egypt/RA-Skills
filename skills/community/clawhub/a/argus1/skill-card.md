## Description: <br>
Argus scans Python and JavaScript codebases for bugs, security vulnerabilities, code smells, and common anti-patterns, then reports prioritized findings with line numbers, severity ratings, and fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Argus to locally inspect Python or JavaScript projects for common security issues, bugs, and maintainability problems before review or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local Markdown reports by default and can write JSON reports that may contain findings and short code snippets from scanned repositories. <br>
Mitigation: Run it only in a workspace where report files are acceptable, and avoid scanning highly sensitive repositories unless saving those details locally is acceptable. <br>
Risk: The skill installs the Python rich package before scanning. <br>
Mitigation: Review dependency installation expectations before running it in restricted or production-like environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/argus1) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Console report with a local Markdown report file and optional JSON findings file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include file paths, line numbers, severity labels, issue descriptions, and fix suggestions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
