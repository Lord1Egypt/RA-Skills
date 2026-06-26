## Description: <br>
Axioma Skill Evaluator Strict 90% evaluates ClawHub skills with a documented 90% quality threshold, producing scores, reports, pass/fail guidance, and improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill publishers, and skill reviewers use this skill to run local structural and heuristic checks against a skill directory and receive quality scores, reports, and remediation guidance. Based on the security evidence, it should be treated as an advisory checker rather than an authoritative publishing gate until the 90% threshold behavior is fixed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present an APPROVED result for scores below the advertised strict 90% gate. <br>
Mitigation: Treat results as advisory and manually verify score thresholds before using the output for publishing or security decisions. <br>
Risk: Report text, exit behavior, and claimed auto-improvement behavior may not match the strict workflow described in the skill documentation. <br>
Mitigation: Review the generated report and script behavior directly, and do not rely on --improve or approval status until those mismatches are fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiomata-skill-evaluator-strict) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Terminal text and Markdown-style quality reports with Python command examples and local report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include dimension scores, structural check results, approval or rejection status, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
