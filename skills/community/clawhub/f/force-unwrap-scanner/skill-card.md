## Description:

Scans Swift projects for force unwraps and try! usage, categorizes potential crash risks, and reports findings with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift, iOS, and macOS projects for force unwrap and try! patterns that may cause runtime crashes. It helps triage findings by risk level and supports report generation and remediation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references a RunSkill.sh command that is not included in the inspected package.

Mitigation: Confirm the scanner implementation is present before relying on scan, report, or fix commands.

Risk: The skill documentation is primarily in Chinese, which may affect review by users who do not read Chinese.

Mitigation: Provide or review a translated version of the instructions and risk categories before operational use.

Risk: Interactive fixes can modify code and high-risk findings require human judgment.

Mitigation: Review proposed changes manually, especially for high-risk findings and crash-prone Swift APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/force-unwrap-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and scan report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe high, medium, and low risk categories with file and line references when scan results are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
