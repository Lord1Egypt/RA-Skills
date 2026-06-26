## Description: <br>
Conducts rigorous, adversarial code reviews that identify security, correctness, maintainability, performance, accessibility, and testing issues with structured severity tiers and actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziad-hsn](https://clawhub.ai/user/ziad-hsn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to obtain strict code or pull request reviews that surface defects, risky assumptions, weak edge-case handling, and code quality problems before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict review feedback may be too severe or incomplete when the available code context is partial. <br>
Mitigation: Treat findings as review guidance, verify severity against the repository context, and calibrate recommendations to team conventions before acting. <br>
Risk: PR-comment workflows could publish review feedback before the user has accepted the wording. <br>
Mitigation: Confirm before posting generated review feedback to a pull request or other shared review surface. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziad-hsn/critical-code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review with severity sections and actionable recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file and line references when code context is available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
