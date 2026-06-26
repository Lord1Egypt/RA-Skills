## Description: <br>
360Guard provides a comprehensive security review workflow for evaluating agent skills before installation, including static checks, behavior detection, dependency auditing, and automated scan scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinc913](https://clawhub.ai/user/robinc913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review ClawHub, GitHub, or other third-party skills before installation and to produce advisory security findings for manual approval decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern-based scans can miss malicious behavior or produce incomplete findings. <br>
Mitigation: Manually inspect important files and treat automated results as advisory rather than a final security decision. <br>
Risk: Scan reports may include local paths, code snippets, or findings from the target skill directory. <br>
Mitigation: Run scans against a copied or clearly scoped skill directory and review generated reports before sharing them. <br>
Risk: The full scan writes a report file into the scanned skill directory. <br>
Mitigation: Use a disposable copy of the target skill when preserving the original directory matters. <br>


## Reference(s): <br>
- [360Guard ClawHub page](https://clawhub.ai/robinc913/360guard-skillvetter-upgrade-version) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and terminal scan reports with risk levels, file locations, snippets, and recommended actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner scripts are advisory and may return process exit codes to distinguish critical, high, medium, and no-obvious-risk findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
