## Description: <br>
Minimal helper to audit skill.md-style instructions for supply-chain risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scan skill.md-style instructions for common supply-chain risk indicators before installing, sharing, or releasing a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report can include snippets from the scanned file. <br>
Mitigation: Review or redact reports before sharing them outside the intended review context. <br>
Risk: The scanner reads local files selected by the user. <br>
Mitigation: Run it only against files intentionally chosen for skill-audit review. <br>
Risk: Heuristic findings may miss issues or flag benign text. <br>
Mitigation: Use the report as a lightweight screening aid and keep manual review in the release process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/agents-skill-security-audit) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with risk level, findings, line references, and suggested action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected local file and prints a report to standard output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
