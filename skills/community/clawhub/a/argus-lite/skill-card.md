## Description: <br>
Argus Lite — Code Scanner (Free) scans a single Python file for the top 10 most critical security and bug patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a lightweight local scan of one Python file for common high-impact security and bug patterns before deeper review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install command can affect a system-managed Python environment if run directly. <br>
Mitigation: Install and run the skill in a virtual environment, pipx-style isolation, or a disposable/containerized workspace. <br>
Risk: Scanning a directory selects only the first Python file, so other files may remain unchecked. <br>
Mitigation: Set SOURCE_PATH to the specific Python file that needs review and use broader scanning for full-codebase coverage. <br>
Risk: The scanner uses a small fixed set of pattern rules and can miss vulnerabilities outside those patterns. <br>
Mitigation: Treat results as preliminary guidance and combine them with code review, testing, and additional security scanning. <br>


## Reference(s): <br>
- [Argus Lite ClawHub Page](https://clawhub.ai/occupythemilkyway/argus-lite) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and console scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans one Python file at a time using SOURCE_PATH and reports matched rules, severities, affected lines, and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
