## Description: <br>
Scans Swift projects for force unwraps (`!`) and `try!` usage and reports potential runtime crash risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Swift projects for force unwrap and `try!` patterns, categorize findings by risk, and generate remediation guidance before runtime crashes reach users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced runner may execute local shell behavior when used outside the provided artifact. <br>
Mitigation: Verify RunSkill.sh comes from the expected source before running it. <br>
Risk: Interactive fix mode may edit project files. <br>
Mitigation: Use version control or backups and review generated changes before keeping them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soponcd/force-unwrap-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown scan reports with file paths, line numbers, risk levels, and remediation suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive fix guidance; review changes with version control before applying fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
