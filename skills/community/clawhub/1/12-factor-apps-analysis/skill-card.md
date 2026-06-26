## Description: <br>
Performs 12-Factor App compliance analysis on a codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review a codebase against the 12-Factor App methodology, document file-level evidence, identify gaps, and produce prioritized recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read private project files while collecting evidence from a target repository. <br>
Mitigation: Point the skill only at repositories intended for review and handle resulting file references according to the repository's confidentiality requirements. <br>
Risk: The workflow references a separate 12-factor-apps helper skill. <br>
Mitigation: Review that helper skill separately before using it as part of the analysis workflow. <br>


## Reference(s): <br>
- [12-Factor App Methodology](https://12factor.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis report with executive summary tables, detailed findings, file:line evidence, and prioritized recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden execution or persistence; the skill guides repository analysis and may reference the separate 12-factor-apps helper skill.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
