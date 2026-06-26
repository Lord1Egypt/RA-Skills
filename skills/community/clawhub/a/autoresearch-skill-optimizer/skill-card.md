## Description: <br>
Auto-improves OpenClaw skills by auditing their structure, running score-based test loops, and keeping targeted edits that improve measured output quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngmeyer](https://clawhub.ai/user/ngmeyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit, test, and iteratively improve OpenClaw skills before deploying them broadly or after model and workflow changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can test and edit other skills repeatedly, which may introduce incorrect or misleading guidance. <br>
Mitigation: Run target skills in dry-run or sandboxed mode and manually review diffs before replacing any real SKILL.md or using the optimized skill at scale. <br>
Risk: The skill may use prior memory or session history as test input when representative examples are not provided. <br>
Mitigation: Provide sanitized test cases explicitly and do not allow memory or session history to be used as test input. <br>
Risk: Repeated optimization rounds can invoke target skills multiple times, including skills that call external or costly APIs. <br>
Mitigation: Use rate-limited, sandboxed, or mocked runs for target skills that call external services. <br>


## Reference(s): <br>
- [Autoresearch Skill Optimizer release page](https://clawhub.ai/ngmeyer/autoresearch-skill-optimizer) <br>
- [Self-Optimization Changelog](optimization-changelog.md) <br>
- [Scoring Checklist Examples by Skill Type](references/checklist-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with proposed skill edits, scoring notes, and generated skill files or changelog content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create optimized SKILL.md variants and optimization changelogs for human review.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
